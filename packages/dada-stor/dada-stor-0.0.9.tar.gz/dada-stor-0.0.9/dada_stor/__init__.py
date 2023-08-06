"""
Utilities for interacting with AWS S3 / Digital Ocean Spaces
"""
import os
from io import BytesIO, StringIO
import tempfile
import logging
import urllib
from typing import Callable, List, Generator, Union, Optional

import boto3
import botocore

import dada_settings
from dada_utils import path
import dada_serde

# ///////////////////
# Logging
# ///////////////////
S3_LOGGER = logging.getLogger()

# ///////////////////
# DOC STRINGS
# ///////////////////

KEY_PARAM = ":param key: An S3 key"
LOCAL_PATH_PARAM = ":param local_path: The local filepath to write to. if it doesn't exist, the file will be written to a tempfile and the path will be outputted."
FOBJ_PARAM = ":param fobj: A file-like object to write to. If not provided, the function will create an `io.BytesIO` object, write the file contents to it, and return it."
PREFIX_PARAM = ":param prefix: A prefix used to identify a list of s3 keys"
KEY_FILTER_PARAM = ":param prefix: A function that accepts a key and returns true if we should include the key in the results"
MIMETYPE_PARAM = ":param mimetype: The mimetype to set for this key"

# ///////////////////
# CLASSES
# ///////////////////

DADA_STOR_DEFAULT_MIMETYPE = "binary/octet-stream"


def get_bucket_name_and_scheme(s3_url):
    """
    Get the bucket name from a s3 url
    """
    p = urllib.parse.urlparse(s3_url)
    if p.netloc == "":
        return p.scheme, p.path.split("/")[0]
    return p.scheme, p.netloc


def parse(s3_url) -> tuple:
    """parse a full s3 url into its bucket name and key"""
    scheme, bucket_name = get_bucket_name(s3_url)
    s3_prefix = f"{scheme}://{bucket_name}"
    if s3_url.startswith(s3_prefix):
        key = s3_url[len(s3_prefix) :]
    elif s3_url.startswith(bucket_name):
        key = s3_url[len(bucket_name) + 1 :]
    else:
        key = s3_url
    if key.startswith("/"):
        key = key[1:]
    return bucket_name, key


class DadaStor(object):
    def __init__(
        self,
        bucket_name: str = dada_settings.S3_BUCKET,
        aws_access_key_id: str = dada_settings.S3_ACCESS_KEY_ID,
        aws_secret_access_key: str = dada_settings.S3_SECRET_ACCESS_KEY,
        endpoint_url: str = dada_settings.S3_ENDPOINT_URL,
        base_url: str = dada_settings.S3_BASE_URL,
        region_name: Optional[str] = dada_settings.S3_REGION_NAME,
        platform: str = dada_settings.S3_PLATFORM,
    ):
        self.scheme, self.bucket_name = get_bucket_name_and_scheme(bucket_name)
        self.access_key = aws_access_key_id
        self.access_secret = aws_secret_access_key
        self.endpoint_url = endpoint_url
        self.base_url = base_url
        self.region_name = region_name
        self.platform = platform
        self.resource = self.connect_resource()
        self.client = self.connect_client()
        self.external_client = self.connect_external_client()
        self.external_conn = self.connect_external_resource()
        self.bucket = self.get_bucket()
        if not self.scheme:
            self.scheme = "dada"
        if self.platform == "s3":
            self.scheme = "s3"
        self.s3_prefix = f"{self.scheme}://{self.bucket_name}/"

    # ////////////////////////
    #  Absolute Key Formatting
    #  (Allow all keys to have full s3:// paths on input and force full paths on output)
    # ///////////////////////

    def _in_key(self, key: str) -> str:
        f"""
        Format input key to accept fullpaths.
        {KEY_PARAM}
        :return str
        """
        if key.startswith(self.s3_prefix):
            key = key.replace(self.s3_prefix, "")
        return key

    def _out_key(self, key: str) -> str:
        f"""
        Format output key to return fullpaths.
        {KEY_PARAM}
        :return str
        """
        if not key.startswith(self.s3_prefix):
            key = f"{self.s3_prefix}{key}"
        return key

    def ensure(self) -> bool:
        """
        Ensure this bucket exists, return True if does, False if we create it
        """
        response = self.client.list_buckets()
        for bucket in response.get("Buckets", []):
            if bucket["Name"] == self.bucket_name:
                return True
        self.client.create_bucket(Bucket=self.bucket_name)
        return False

    # ////////////////////////
    #  Boto Client / Resource Connections
    # ///////////////////////
    @property
    def connection_kwargs(self):
        return dict(
            region_name=self.region_name,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.access_secret,
            endpoint_url=self.endpoint_url,
        )

    def connect_resource(self):
        """
        Connect to boto3 s3 resource
        """
        return boto3.resource("s3", **self.connection_kwargs)

    def connect_client(self):
        """
        Connect to boto3 s3 resource
        """
        return boto3.client("s3", **self.connection_kwargs)

    def connect_external_client(self):
        return boto3.client(
            "s3", config=botocore.client.Config(signature_version=botocore.UNSIGNED),
        )

    def connect_external_resource(self):
        return boto3.resource(
            "s3", config=botocore.client.Config(signature_version=botocore.UNSIGNED),
        )

    def get_bucket(self):
        """
        Get boto3 bucket object
        """
        return self.resource.Bucket(self.bucket_name)

    # ////////////////////////
    #  Core Methods
    # ///////////////////////

    def get_meta(self, key: str) -> dict:
        f"""
        Fetch metadata about this file on S3.
        {KEY_PARAM}
        :return dict
        """
        return self.client.head_object(Bucket=self.bucket_name, Key=self._in_key(key))

    def get_contents(self, key: set):
        f"""
        Fetch the file contents from a key.
        {KEY_PARAM}
        :return dict
        """
        obj = self.resource.Object(self.bucket_name, self._in_key(key))
        return obj.get()["Body"].read()

    def exists(self, key: str) -> bool:
        f"""
        Check whether this key exists
        {KEY_PARAM}
        :return bool
        """
        objs = list(self.bucket.objects.filter(Prefix=self._in_key(key)))
        if len(objs) > 0 and objs[0].key == self._in_key(key):
            return True
        return False

    def download(self, key: str, local_path: Union[None, str] = None) -> str:
        f"""
        Download an s3 key to a local file
        {KEY_PARAM}
        {LOCAL_PATH_PARAM}
        :return str
        """
        if local_path is None:
            local_path = os.path.join(tempfile.mkdtemp(), os.path.basename(key))
        self.bucket.download_file(self._in_key(key), local_path)
        return local_path

    def download_file_obj(self, key: str, fobj: Optional[BytesIO] = None) -> BytesIO:
        f"""
        Download an s3 key to a file-like object
        {KEY_PARAM}
        {FOBJ_PARAM}
        :return BytesIO
        """
        fileobj = BytesIO()
        self.client.download_fileobj(self.bucket_name, self._in_key(key), fileobj)
        return fileobj.erad

    def download_all(
        self,
        prefix: str,
        local_path: Union[None, str] = None,
        key_filter: Callable = lambda x: True,
    ):
        f"""
        Download s3 files under a given prefix to a local directory. Returns the list of local filepaths.
        {PREFIX_PARAM}
        {LOCAL_PATH_PARAM}
        {KEY_FILTER}
        :yield str
        """
        if local_path is None:
            local_path = path.get_tempdir()

        if not path.is_dir(local_path):
            path.make_dir(local_path)

        local_paths = []
        for key in self.list_keys(prefix, key_filter):
            dl_path = path.join(local_path, os.path.basename(key))
            self.bucket.download_file(self._in_key(key), dl_path)
            yield dl_path

    def upload_file_obj(
        self, fobj: BytesIO, key: str, mimetype: Optional[str] = None
    ) -> None:
        f"""
        Upload a file object to s3, optionally setting its mimetype
        {KEY_PARAM}
        {FOBJ_PARAM}
        :return None
        """
        self.bucket.upload_fileobj(
            fobj,
            self._in_key(key),
            ExtraArgs={
                "ContentType": mimetype or DADA_STOR_DEFAULT_MIMETYPE,
                "MetadataDirective": "REPLACE",
            },
        )

    def _upload_file(
        self, local_path: str, key: str, mimetype: Optional[str] = None
    ) -> str:
        f"""
        Upload a file to a s3 bucket, optionally applying a mimetype
        {LOCAL_PATH_PARAM}
        {KEY_PARAM}
        {MIMETYPE_PARAM}
        :return str
        """
        if not mimetype:
            mimetype = path.get_mimetype(local_path)
        self.bucket.upload_file(
            local_path,
            self._in_key(key),
            ExtraArgs={"ContentType": mimetype or DADA_STOR_DEFAULT_MIMETYPE},
        )
        return self._out_key(key)

    def upload(self, local_path: str, key: str, mimetype: Optional[str] = None):
        f"""
        Upload a file to a s3 bucket
        {LOCAL_PATH_PARAM}
        {KEY_PARAM}
        :param infer_mimetype: Whether or not to detect the file's mimetype.
        :return str
        """
        # TODO: replace all these os calls with ``path```
        if path.is_dir(local_path):
            S3_LOGGER.debug(
                "[upload] found directory at {local_path}. The default is to recursively upload from here."
            )
            for filename in path.list_files(local_path):
                sub_path = path.get_relpath(filename, start=local_path)
                file_key = path.join(key, sub_path)
                S3_LOGGER.debug(f" [s3-upload] UPLOADING {file_path} to {file_key}")
                return self._upload_file(file_path, file_key)

        return self._upload_file(local_path, key, mimetype)

    def delete(self, key: str) -> None:
        f"""
        Delete a file from s3.
        {KEY_PARAM}
        :return None
        """
        obj = self.bucket.Object(self._in_key(key))
        obj.delete()

    def move(self, old_key: str, new_key: str, copy_data: bool = False) -> str:
        f"""
        Move a file on s3
        :param old_key: the file's current location
        :param new_key: the file's new location
        :param copy_data: whether or not to leave current file where it is.
        :return str
        """
        new_obj = self.bucket.Object(self._in_key(new_key))
        new_obj.copy(
            {"Bucket": self.bucket_name, "Key": self._in_key(old_key)},
            ExtraArgs={"MetadataDirective": "REPLACE"},
        )

        if not copy_data:
            old_obj = self.bucket.Object(self._in_key(old_key))
            old_obj.delete()
        return self._out_key(old_key)

    def move_all(
        self, old_pfx: str, new_pfx: str, copy_data: bool = False
    ) -> List[str]:
        f"""
        Move files on s3 returning their new paths
        :param old_pfx: the files' current prefix
        :param new_key: the files' new prefix
        :param copy_data: whether or not to leave current files where they are.
        :return list
        """
        new_paths = []
        for old_obj in self.bucket.objects.filter(Prefix=self.in_key(old_pfx)):
            new_key = old_obj.key.replace(old_pfx, new_pfx, 1)
            new_obj = self.bucket.Object(self._in_key(new_key))
            new_obj.copy(
                {"Bucket": self.bucket_name, "Key": old_obj.key},
                ExtraArgs={"MetadataDirective": "REPLACE"},
            )
            # cleanup
            if not copy_data:
                old_obj.delete()
            new_paths.append(self._out_key(new_key))
        return new_paths

    def copy(self, old_key: str, new_key: str) -> None:
        """"""
        return self.move(self._in_key(old_key), self._in_key(new_key), copy_data=True)

    def copy_all(self, old_pfx: str, new_pfx: str) -> List[str]:
        """"""
        return self.move_all(
            self._in_key(old_pfx), self._in_key(new_pfx), copy_data=True
        )

    def list_keys(self, prefix: str, key_filter: Callable = lambda x: True):
        f"""
        List keys in S3 bucket.
        {PREFIX_PARAM}
        {KEY_FILTER_PARAM}
        :yield str
        """
        return (
            self._out_key(obj.key)
            for obj in self.bucket.objects.filter(Prefix=selff._in_key(prefix))
            if key_filter(obj.key)
        )

    # ////////////////////////
    #  Version / Audit-based methods
    # ///////////////////////

    def upload_and_version(
        self,
        local_path,
        latest_key: str,
        version_key: str,
        mimetype: Optional[str] = DADA_STOR_DEFAULT_MIMETYPE,
    ) -> None:
        """
        Upload a file to the "latest" url and copy it to its version path.
        """
        self.upload(local_path, latest_key, mimetype)
        self.copy(latest_key, version_key)

    def upload_file_obj_and_version(
        self,
        fobj: BytesIO,
        latest_key: str,
        version_key: str,
        mimetype: Optional[str] = DADA_STOR_DEFAULT_MIMETYPE,
        **kwargs,
    ) -> None:
        """
        Upload a file to the "latest" url and copy it to its version path.
        """
        self.upload_file_obj(fobj, latest_key, mimetype)
        self.copy(latest_key, version_key)

    def upload_data_and_version(
        self, data, latest_key: str, version_key: str, is_private: bool = True, **kwargs
    ) -> None:
        """
        Upload a json-serializable object as json.gz and record a version
        """
        self.upload_file_obj_and_version(
            dada_serde.obj_to_jsongz_fobj(data), latest_key, mimetype="application/gzip"
        )
        self.copy(latest_key, version_key)

    # ////////////////////////
    #  Public/Private Access
    # ///////////////////////

    def set_acl(self, key: str, acl: str, raise_on_missing: bool = False) -> None:
        f"""
        Set the access control for a s3 key
        {KEY_PARAM}
        :param acl: The ACL string (either ``private`` or ``public-read``)
        :param raise_on_missing: Whether or not to raise an error if the key does not exist
        :return None
        """
        if not self.exists(key):
            if raise_on_missing:
                raise ValueError(f"{key} does not exist in {self.s3_prefix}")
            return
        obj = self.bucket.Object(self._in_key(key))
        obj.Acl().put(ACL=acl)

    def set_private(self, key: str) -> None:
        f"""
        Make this file on s3 private
        {KEY_PARAM}
        :return None
        """
        self.set_acl(key, "private")

    def set_public(self, key: str):
        f"""
        Make this file on s3 private
        {KEY_PARAM}
        :return None
        """
        self.set_acl(key, "public-read")

    def get_presigned_url(self, key: str, expiration: int = 3600) -> str:
        f"""
        Create a presigned url for an s3 asset.
        {KEY_PARAM}
        :param expiration: The number of seconds this url is valid for.
        :return str
        """
        return self.client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket_name, "Key": self._in_key(key)},
            ExpiresIn=expiration,
        )

    def get_public_url(self, key: str) -> str:
        f"""
        Get the public url for an s3 asset.
        {KEY_PARAM}
        :return str
        """
        return "{}/{}/{}".format(
            self.client.meta.endpoint_url, self.bucket_name, self._in_key(key)
        )

    # ////////////////////////
    #  Special Methods
    # ///////////////////////

    def external_download(self, url, local_path: Optional[str] = None,) -> str:
        f"""
        Download a file from a public s3 bucket
        :param url: a full s3 url (eg: ``s3://bucket/key.txt``)
        {LOCAL_PATH_PARAM}
        :return str
        """
        bucket_name, key = parse(url)
        if local_path is None:
            local_path = path.join(path.get_tempdir(), path.get_base_path(key))
        self.external_client.download_file(bucket_name, key, local_path)
        return local_path

    def external_get_contents(self, url: str):
        """
        :param url: a full s3 url (eg: ``s3://bucket/key.txt``)
        """
        bucket_name, key = parse(url)
        obj = self.external_conn.Object(bucket_name, key)
        return obj.get()["Body"].read()

    # ////////////////////////
    #  Website Configuraiton
    # ///////////////////////

    def create_website(
        self,
        index_doc: str = "index.html",
        error_doc: str = "index.html",
        host: Optional[str] = None,
        host_protocal: str = "https",
        routing_rules: list = [],
    ) -> None:
        """
        Configure this S3 bucket to be a website.
        """
        # initial dada_settings
        conf = {
            "ErrorDocument": {"Key": error_doc,},
            "IndexDocument": {"Suffix": index_doc},
        }

        # host setings
        if host is not None:
            conf["RedirectAllRequestsTo"] = {
                "HostName": host,
                "HostProtocol": host_protocol,
            }
        if len(routing_rules) > 0:
            conf["RoutingRules"] = routing_rules

        # create the website
        self.client.put_bucket_website(
            Bucket=self.bucket_name, WebsiteConfiguration=conf
        )

    def delete_website(self):
        """
        Delete the website configurations from this S3 bucket
        """
        self.client.delete_bucket_website(Bucket=self.bucket_name)
