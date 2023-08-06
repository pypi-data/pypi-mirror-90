import concurrent.futures
import os
import tempfile
import typing
from abc import abstractmethod, ABC
from typing import IO

from google.protobuf.internal.encoder import _VarintBytes

from bakplane.bakplane_pb2 import ErrorEntry
from bakplane.ingestion.landing_zone import LandingZoneFactory
from .models import Asset, Entity, Relationship, IngestionSessionContext, Error

from pybloom_live import ScalableBloomFilter


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
    def __init__(self, context: IngestionSessionContext, asset_num_sharding=8, entities_num_sharding=8,
                 rels_num_sharding=8):

        if asset_num_sharding < 1 or entities_num_sharding < 1 or rels_num_sharding < 1:
            raise RuntimeError('Invalid requested number of shards.')

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

        self.entities_bf = ScalableBloomFilter(mode=ScalableBloomFilter.LARGE_SET_GROWTH)
        self.rels_bf = ScalableBloomFilter(mode=ScalableBloomFilter.LARGE_SET_GROWTH)

        self.asset_num_sharding = asset_num_sharding
        self.entities_num_sharding = entities_num_sharding
        self.rels_num_sharding = rels_num_sharding

    def __get_entities_fd(self, entity: Entity) -> IO:
        key = 'entities'

        if self.entities_num_sharding > 1:
            shard = entity.identity.uid % self.entities_num_sharding
            key += f'___{shard}_of_{self.entities_num_sharding}_'

        if key not in self.fd_map:
            self.fd_map[key] = tempfile.NamedTemporaryFile(
                mode="w+b", delete=False, prefix=key
            )
        return self.fd_map[key]

    def __get_errors_fd(self, error: ErrorEntry) -> IO:
        if "errors" not in self.fd_map:
            self.fd_map["errors"] = tempfile.NamedTemporaryFile(
                mode="w+b", delete=False, prefix="errors"
            )
        return self.fd_map["errors"]

    def __get_relationships_fd(self, relationship: Relationship) -> IO:
        key = 'relationships'

        if self.rels_num_sharding > 1:
            shard = relationship.source_identity_uid % self.rels_num_sharding
            key += f'___{shard}_of_{self.rels_num_sharding}_'

        if key not in self.fd_map:
            self.fd_map[key] = tempfile.NamedTemporaryFile(
                mode="w+b", delete=False, prefix=key
            )
        return self.fd_map[key]

    def __get_assets_fd(self, asset: Asset) -> IO:
        key = asset.resource_code

        if self.asset_num_sharding > 1:
            shard = asset.payload_hash % self.asset_num_sharding
            key += f'___{shard}_of_{self.asset_num_sharding}_'

        if key not in self.fd_map:
            self.fd_map[key] = tempfile.NamedTemporaryFile(
                mode="w+", delete=False, prefix=key
            )
        return self.fd_map[key]

    def __write_entity(self, entity: Entity):
        payload_hash = entity.payload_hash

        if payload_hash in self.entities_bf:
            return

        f = self.__get_entities_fd(entity)
        p = entity.to_proto()

        f.write(_VarintBytes(p.ByteSize()))
        f.write(p.SerializeToString())

        self.entities_bf.add(payload_hash)

    def __write_error(self, error: ErrorEntry):
        f = self.__get_errors_fd(error)
        p = error.to_proto()

        f.write(_VarintBytes(p.ByteSize()))
        f.write(p.SerializeToString())

    def __write_relationship(self, relationship: Relationship):
        payload_hash = relationship.payload_hash

        if payload_hash in self.rels_bf:
            return

        f = self.__get_relationships_fd(relationship)
        p = relationship.to_proto()

        f.write(_VarintBytes(p.ByteSize()))
        f.write(p.SerializeToString())

        self.rels_bf.add(payload_hash)

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
        with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() + 1) as executor:
            tasks = []

            for k, v in self.fd_map.items():
                v.close()

                if k.startswith("entities"):
                    tasks.append(executor.submit(self.entities_lz.upload,
                                                 v.name,
                                                 self.ctx.entities_output_location,
                                                 ".proto.gz",
                                                 prefix="entities",
                                                 ))
                elif k.startswith("relationships"):
                    tasks.append(executor.submit(self.relationships_lz.upload,
                                                 v.name,
                                                 self.ctx.relationships_output_location,
                                                 ".proto.gz",
                                                 prefix="relationships",
                                                 ))
                elif k == "errors":
                    self.errors_lz.upload(
                        v.name,
                        self.ctx.errors_output_location,
                        ".proto.gz",
                        prefix="errors",
                    )
                else:
                    asset_code = k
                    if self.asset_num_sharding > 1:
                        asset_code = asset_code.split('___')[0]

                        tasks.append(executor.submit(self.assets_lz.upload,
                                                     v.name,
                                                     self.ctx.assets_output_location + asset_code + "/",
                                                     ".csv.gz",
                                                     ))
                _ = [_.result() for _ in tasks]
