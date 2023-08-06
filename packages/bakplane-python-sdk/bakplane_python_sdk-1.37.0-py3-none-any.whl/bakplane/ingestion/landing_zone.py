import gzip
import os
import shutil
import tempfile
from abc import ABC, abstractmethod
from urllib.parse import urlparse

import boto3


class LandingZone(ABC):
    @abstractmethod
    def upload(self, src_path: str, dst_path: str, suffix: str = "", prefix: str = None):
        pass


class FilesystemLandingZone(LandingZone):
    def upload(
        self,
        src_path: str,
        dst_path: str,
        suffix: str = "",
        prefix: str = None,
    ):
        u = urlparse(dst_path)
        with open(src_path, "rb") as f_in:
            with tempfile.NamedTemporaryFile(
                "wb",
                prefix=os.path.basename(src_path),
                delete=False,
                dir="." + u.path,
                suffix=suffix,
            ) as f:
                with gzip.open(f, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)


class AmazonS3LandingZone(LandingZone):
    def __init__(self):
        self.client = boto3.client("s3")

    def upload(self, src_path: str, dst_path: str, suffix: str = "", prefix: str = None):
        u = urlparse(dst_path)

        if u.scheme != "s3":
            raise RuntimeError("Invalid destination path.")

        with open(src_path, "rb") as f_in:
            f = tempfile.NamedTemporaryFile(delete=False, prefix=os.path.basename(src_path))
            final_path = f.name

            with gzip.open(f, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

            f.close()

            self.client.upload_file(
                final_path,
                u.netloc,
                u.path[1:] + os.path.basename(src_path) + suffix,
            )


class LandingZoneFactory(object):
    @staticmethod
    def build_from_uri(uri):
        u = urlparse(uri)

        if u.scheme == "s3":
            return AmazonS3LandingZone()
        elif u.scheme == "file":
            return FilesystemLandingZone()
        raise RuntimeError(
            f"Could not find landing zone matching scheme `{u.scheme}`."
        )
