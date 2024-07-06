import json
import typing

from ci3.src.helpers import AbstractClient


class MockClient(AbstractClient):

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        assert kwargs.get("files"), "Must have files"

    def get_paginator(self, _: str) -> "MockClient":
        return self

    def paginate(self, **kwargs) -> typing.Generator[typing.Any, None, None]:
        results = self.kwargs[json.dumps(kwargs)]
        yield results

    def delete_objects(
        self,
        Bucket: str,
        Delete: typing.List[typing.Dict[str, typing.List[typing.Dict[str, str]]]],
    ):
        for mock_object in Delete["Objects"]:
            files: typing.List[str] = self.kwargs["files"]
            key = mock_object["Key"]
            idx: int = files.index(key)
            del self.kwargs["files"][idx]
