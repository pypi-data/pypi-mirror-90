import abc
from abc import ABC, abstractmethod
from collections import namedtuple
from quickbuild.exceptions import QuickBuildError as QuickBuildError
from typing import Any, Callable

Response = namedtuple('Response', ['status', 'body'])

class QuickBuild(ABC, metaclass=abc.ABCMeta):
    def __init__(self) -> None: ...
    @abstractmethod
    def close(self) -> None: ...
    @abstractmethod
    def request(self, callback: Callable[[Response], str], method: str, path: str, **kwargs: Any) -> str: ...
    def get_version(self) -> str: ...
