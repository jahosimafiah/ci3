from abc import ABC, abstractmethod
import typing

class AbstractClient(ABC):

    @abstractmethod
    def get_paginator(self, pagintor_type: str) -> "AbstractClient":
        raise NotImplementedError

    @abstractmethod
    def paginate(
        self, **kwargs
    ) -> typing.Generator[typing.List[typing.Dict[str, typing.Any]], None, None]:
        raise NotImplementedError

    @abstractmethod
    def delete_objects(
        self, Bucket: str, Objects: typing.List[typing.Dict[str, typing.Any]]
    ):
        raise NotImplementedError