import json
import typing

from datetime import datetime as dt
from datetime import timedelta as td
from tests.mocks import MockClient


def new_fs_dt_dict(
    bucket: str,
    prefix: str,
    files: typing.List[str],
    prefix_dt: dt,
) -> typing.Dict[typing.Dict[typing.Any, dt], dt]:
    kwargs = {
        "Contents": [
            {"Key": f, "LastModified": prefix_dt} for f in files if f.startswith(prefix)
        ]
    }
    return {json.dumps({"Bucket": bucket, "Prefix": prefix}): kwargs}


def generate_mock_client_and_class_attributes(cls):
    cls.bucket = "mock-bucket"
    cls.files = [
        "deploy_old/root.html",
        "deploy_newest/index.js",
        "deploy_new/styles/style.css",
        "deploy_old/style.css",
        "deploy_new/fonts/font.css",
        "deploy_newest/index.html",
    ]
    cls.deploy_newest_dt = dt.now()
    cls.deploy_new_dt = cls.deploy_newest_dt - td(days=1)
    cls.deploy_old_dt = cls.deploy_new_dt - td(days=1)
    client_kwargs = {
        "files": cls.files,
    }
    client_kwargs.update(
        {
            json.dumps({"Bucket": cls.bucket, "Delimiter": "/"}): {
                "CommonPrefixes": [
                    {
                        "Prefix": "deploy_old/",
                    },
                    {
                        "Prefix": "deploy_newest/",
                    },
                    {
                        "Prefix": "deploy_new/",
                    },
                ],
            }
        }
    )
    client_kwargs.update(
        new_fs_dt_dict(
            cls.bucket,
            prefix="deploy_newest/",
            prefix_dt=cls.deploy_newest_dt,
            files=cls.files,
        )
    )
    client_kwargs.update(
        new_fs_dt_dict(
            cls.bucket,
            prefix="deploy_old/",
            prefix_dt=cls.deploy_old_dt,
            files=cls.files,
        )
    )
    client_kwargs.update(
        new_fs_dt_dict(
            cls.bucket,
            prefix="deploy_new/",
            prefix_dt=cls.deploy_new_dt,
            files=cls.files,
        )
    )
    cls.client = MockClient(**client_kwargs)