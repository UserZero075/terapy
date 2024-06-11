from typing import Union,TypeAlias,AsyncIterable,Callable,Any
from yarl import URL
from httpx import Response
from io import BufferedWriter

URLTypes = Union[str,URL]
Function = Callable[...,Any]
Args = tuple[Any]

Buffer: TypeAlias = BufferedWriter 
