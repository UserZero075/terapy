from typing import Callable
from ext import SessionCookies
from httpx import Client,AsyncClient

class Terabox:
    
    httpx_client: Client

    def __init__(self,session: SessionCookies,callback: Callable[...,None]) -> None:
        if not isinstance(session,SessionCookies):
            raise Exception()
        self._session = session._prepare_to_session()
        self._callback = callback
    
    def _prepare_headers():
        pass

    def _init_client(self):
        self.httpx_client = Client(
            cookies=self.session
        )

    @property
    def session(self):
        return self.session
    
    @property
    def callback(self):
        return self._callback
    
    @callback.setter
    def callback(self,value: Callable[...,None]):
        if not isinstance(value,callable):
            raise Exception("callback debe ser una funcion")
        self._callback = value

    def generate_link() -> str:
        pass


class TeraboxAsync:
    
    httpx_client: AsyncClient
    
    def __init__(self,session: SessionCookies,callback: Callable[...,None]) -> None:
        if not isinstance(session,SessionCookies):
            raise Exception()
        self._session = session._prepare_to_session()
        self._callback = callback
    
    async def _prepare_headers():
        pass

    async def _init_client(self):
        self.httpx_client = AsyncClient(
            cookies=self.session
        )

    @property
    def session(self):
        return self.session
    
    @property
    def callback(self):
        return self._callback
    
    @callback.setter
    def callback(self,value: Callable[...,None]):
        if not isinstance(value,callable):
            raise Exception("callback debe ser una funcion")
        self._callback = value

    async def generate_link() -> str:
        pass