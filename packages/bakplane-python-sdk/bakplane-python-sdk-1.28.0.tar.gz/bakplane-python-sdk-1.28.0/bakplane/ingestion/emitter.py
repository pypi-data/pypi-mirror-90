from bakplane.bakplane_pb2 import ErrorEntry
import os
import tempfile
import typing
from abc import abstractmethod, ABC
from typing import IO

from google.protobuf.internal.encoder import _VarintBytes

from bakplane.ingestion.landing_zone import LandingZoneFactory
from .models import Asset, Entity, Relationship, IngestionSessionContext, Error


class Emitter(ABC):
    @abstractmethod
    def emit_assets(self, assets: typing.List[Asset]):
        pass

    @abstractmethod
    def emit_entities(self, entities: typing.List[Entity]):
        pass

    @abstractmethod
    def emit_relationships(self, relationships: typing.List[Relationship]):
        pass

    @abstractmethod
    def emit_errors(self, errors: typing.List[Error]):
        pass


class DefaultEmitter(Emitter):
    def __init__(self, context: IngestionSessionContext):
        self.ctx = context
        self.fd_map: typing.Dict[str, IO] = {}
        self.entities_lz = LandingZoneFactory.build_from_uri(
            context.entities_output_location
        )
        self.assets_lz = LandingZoneFactory.build_from_uri(
            context.assets_output_location
        )
        self.relationships_lz = LandingZoneFactory.build_from_uri(
            context.relationships_output_location
        )
        self.errors_lz = LandingZoneFactory.build_from_uri(
            context.errors_output_location
        )

    def __get_entities_fd(self, entity: Entity) -> IO:
        if "entities" not in self.fd_map:
            self.fd_map["entities"] = tempfile.NamedTemporaryFile(
                mode="w+b", delete=False, prefix="entities"
            )
        return self.fd_map["entities"]

    def __get_errors_fd(self, error: ErrorEntry) -> IO:
        if "errors" not in self.fd_map:
            self.fd_map["errors"] = tempfile.NamedTemporaryFile(
                mode="w+b", delete=False, prefix="errors"
            )
        return self.fd_map["errors"]

    def __get_relationships_fd(self, relationship: Relationship) -> IO:
        if "relationships" not in self.fd_map:
            self.fd_map["relationships"] = tempfile.NamedTemporaryFile(
                mode="w+b", delete=False, prefix="relationships"
            )
        return self.fd_map["relationships"]

    def __get_assets_fd(self, asset: Asset) -> IO:
        if asset.resource_code not in self.fd_map:
            self.fd_map[asset.resource_code] = tempfile.NamedTemporaryFile(
                mode="w+", delete=False, prefix=asset.resource_code
            )
        return self.fd_map[asset.resource_code]

    def __write_entity(self, entity: Entity):
        f = self.__get_entities_fd(entity)
        p = entity.to_proto()

        f.write(_VarintBytes(p.ByteSize()))
        f.write(p.SerializeToString())

    def __write_error(self, error: ErrorEntry):
        f = self.__get_errors_fd(error)
        p = error.to_proto()

        f.write(_VarintBytes(p.ByteSize()))
        f.write(p.SerializeToString())

    def __write_relationship(self, relationship: Relationship):
        f = self.__get_relationships_fd(relationship)
        p = relationship.to_proto()

        f.write(_VarintBytes(p.ByteSize()))
        f.write(p.SerializeToString())

    def __write_asset(self, asset: Asset):
        f = self.__get_assets_fd(asset)
        f.write(asset.to_csv_entry(self.ctx) + "\n")

    def emit_entities(self, entities: typing.List[Entity]):
        if entities is None or len(entities) <= 0:
            raise ValueError("Entities cannot be null or empty.")

        for e in entities:
            self.__write_entity(e)

    def emit_relationships(self, relationships: typing.List[Relationship]):
        if relationships is None or len(relationships) <= 0:
            raise ValueError("Relationships cannot be null or empty.")

        for r in relationships:
            self.__write_relationship(r)

    def emit_errors(self, errors: typing.List[Error]):
        if errors is None or len(errors) <= 0:
            raise ValueError("Errors cannot be null or empty.")

        for e in errors:
            self.__write_error(e)

    def emit_assets(self, assets: typing.List[Asset]):
        if assets is None or len(assets) <= 0:
            raise ValueError("Assets cannot be null or empty.")

        for a in assets:
            self.__write_asset(a)

    def close(self):
        for k, v in self.fd_map.items():
            v.close()

            if k == "entities":
                self.entities_lz.upload(
                    v.name,
                    self.ctx.entities_output_location,
                    ".proto.gz",
                    prefix="entities",
                )
            elif k == "relationships":
                self.relationships_lz.upload(
                    v.name,
                    self.ctx.relationships_output_location,
                    ".proto.gz",
                    prefix="relationships",
                )
            elif k == "errors":
                self.errors_lz.upload(
                    v.name,
                    self.ctx.errors_output_location,
                    ".proto.gz",
                    prefix="errors",
                )
            else:
                self.assets_lz.upload(
                    v.name,
                    self.ctx.assets_output_location + k + "/",
                    ".csv.gz",
                )
