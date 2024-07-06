from datetime import datetime as dt
import typing

from ci3.src.helpers import AbstractClient

class DeploymentAssetHandler:
    def __init__(
        self,
        s3_bucket: str,
        abstract_client: AbstractClient,
    ) -> "DeploymentAssetHandler":
        self._client = abstract_client
        self.s3_bucket = s3_bucket

    @property
    def deploy_hashes(self) -> typing.Generator[typing.Tuple[str, dt], None, None]:
        paginator = self._client.get_paginator("list_objects_v2")
        p_resp = paginator.paginate(
            Bucket=self.s3_bucket,
            Delimiter='/',
        )
        for page in p_resp:
            folders = page.get("CommonPrefixes", [])
            for folder in folders:
                yield folder['Prefix'], next(
                    self._list_deploy_hash_files(folder['Prefix'], recursive_list=True)
                )['LastModified']

    def _list_deploy_hash_files(
        self, prefix: str, recursive_list: bool = False
    ) -> typing.Generator[str, None, None]:
        paginator = self._client.get_paginator("list_objects_v2")
        p_resp = paginator.paginate(
            Bucket=self.s3_bucket,
            Prefix=prefix,
        )
        for page in p_resp:
            # print('page', page)
            for s3_object in page.get('Contents', []):
                yield s3_object
            # If recursive_list is True, recurse to loop through all files under the new prefix
            if recursive_list:
                for next_prefix in page.get("CommonPrefixes", []):
                    yield from self._list_deploy_hash_files(
                        next_prefix, recursive_list=recursive_list
                    )

    def delete_deploy_files(self, deploy_hash: str):
        file_hash_generator = self._list_deploy_hash_files(
            deploy_hash, recursive_list=True
        )
        objects = [{'Key': _hash['Key']} for _hash in file_hash_generator]
        print('objects to delete ', objects)
        return self._client.delete_objects(
            Bucket=self.s3_bucket,
            Delete={
                "Objects": objects,
            },
        )
