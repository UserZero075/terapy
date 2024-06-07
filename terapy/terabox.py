from typing import (
    Callable,
    Dict
)
from httpx import (
    Client,
    AsyncClient
)

from .utils import (
    is_valid_url, 
    extract_info,
    extract_url_query,
    update_many_query
)
from .const import (
    TOKEN_PATTERN,
    DP_PATTERN,
    BASE_URL
)
from .ext import SessionCookies




class TeraboxData:

    def __init__(self,filename: str,size: int,dlink: str, icon_url: str) -> None:
        self._filename = filename
        self._size = size
        self._dlink = dlink
        self._icon_url = icon_url


    @property
    def filename(self):
        return self._filename
    
    @property
    def size(self):
        return self._size
    @property
    def dlink(self):
        return self._dlink
    @property
    def icon_url(self):
        return self._icon_url


class Terabox:
    
    httpx_client: Client

    def __init__(self,session: SessionCookies,callback: Callable[...,None] = None) -> None:
        if not isinstance(session,SessionCookies):
            raise Exception()
        self._session = session._prepare_to_session()
        self._callback = callback

        self._init_client()
    
    def _prepare_headers(self):
        self.__headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,hi;q=0.8",
        "Connection": "keep-alive",
        "Host": "www.terabox.app",
        "DNT": "1",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Site": "none",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        }
        return self.__headers

    def _init_client(self):
        header = self._prepare_headers()
        self.httpx_client = Client(
            cookies=self.session,
            headers=header,
            follow_redirects=True
        )
        return
    

    @property
    def session(self):
        return self._session
    
    @property
    def callback(self):
        return self._callback
    
    @callback.setter
    def callback(self,value: Callable[...,None]):
        if not isinstance(value,callable):
            raise Exception("callback debe ser una funcion")
        self._callback = value

    def _get_data(self,url: str): 
        if not is_valid_url(url):
            raise Exception("Url is Invalid")
        init_req_redict = self.httpx_client.get(url,params="")
        init_req = self.httpx_client.get(init_req_redict.url,params="")
        token = extract_info(init_req.text,TOKEN_PATTERN)
        dp_login = extract_info(init_req.text,DP_PATTERN)
        short_url = extract_url_query(
            "surl",
            init_req_redict.url
        )
        
        rq = self.httpx_client.get(BASE_URL.format(
                token = token,
                log_id = dp_login,
                short_url = short_url
        ))
    

        if not rq.is_success:
            raise Exception()
        response_json = dict(rq.json())
        if response_json.get("errno") or not response_json.get("list",None):
            raise Exception()
        head_rq = self.httpx_client.get(
            response_json["list"][0]["dlink"],follow_redirects=False
        )
        if not head_rq.has_redirect_location:
            Exception("Error in get direct link")
        return TeraboxData(
            filename=response_json["list"][0]['server_filename'],
            size=response_json["list"][0]['size'],
            dlink=response_json["list"][0]['dlink'],
            icon_url=response_json["list"][0]['thumbs']['url3'],
        )
    def generate_link(self,url: str) -> str:
        if not url and not isinstance(url,str):
            raise Exception()
        r = self._get_data(url)
        if not r.dlink: 
            raise Exception("Probablemente sus cookies son invalidas, debe haber iniciado sesion en la web primero") 
        return r.dlink
    
    def get_thumbs(self,url: str):
        if not url and not isinstance(url,str):
            raise Exception()
        r = self._get_data(url)
        if not r.icon_url: 
            raise Exception("Probablemente sus cookies son invalidas, debe haber iniciado sesion en la web primero") 
        return r.icon_url
    
    def get_size(self,url: str):
        if not url and not isinstance(url,str):
            raise Exception()
        r = self._get_data(url)
        if not r.size: 
            raise Exception("Probablemente sus cookies son invalidas, debe haber iniciado sesion en la web primero") 
        return r.size
    
    def get_name(self,url: str):
        if not url and not isinstance(url,str):
            raise Exception()
        r = self._get_data(url)
        if not r.filename: 
            raise Exception("Probablemente sus cookies son invalidas, debe haber iniciado sesion en la web primero") 
        return r.filename


class TeraboxAsync:
    httpx_client: AsyncClient
    client_timeout = 60
    def __init__(
            self,session: SessionCookies,
            callback: Callable[...,None] = None,
            client_timeout = None) -> None:
        if not isinstance(session,SessionCookies):
            raise Exception()
        self._session = session._prepare_to_session()
        self._callback = callback

        self._client_timeout = client_timeout or self.client_timeout
        self._init_client()
    
    def _prepare_headers(self):
        self.__headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,hi;q=0.8",
        "Connection": "keep-alive",
        "Host": "www.terabox.app",
        "DNT": "1",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Site": "none",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        }
        return self.__headers

    def _init_client(self):
        header = self._prepare_headers()

        self.httpx_client = AsyncClient(
            cookies=self.session,
            headers=header,
            follow_redirects=True,
            timeout=self.client_timeout
        )

    @property
    def session(self):
        return self._session
    
    @property
    def callback(self):
        return self._callback
    
    @callback.setter
    def callback(self,value: Callable[...,None]):
        if not isinstance(value,callable):
            raise Exception("callback debe ser una funcion")
        self._callback = value

    async def _get_data(self,url: str): 
        if not is_valid_url(url):
            raise Exception("Url is Invalid")
        init_req_redict = await self.httpx_client.get(url,params="")
        init_req = await self.httpx_client.get(init_req_redict.url,params="")
        token = extract_info(init_req.text,TOKEN_PATTERN)
        dp_login = extract_info(init_req.text,DP_PATTERN)
        short_url = extract_url_query(
            "surl",
            init_req_redict.url
        )
        
        rq = await self.httpx_client.get(BASE_URL.format(
                token = token,
                log_id = dp_login,
                short_url = short_url
        ))

        if not rq.is_success:
            raise Exception()
        response_json = dict(rq.json())
        if response_json.get("errno") or not response_json.get("list",None):
            raise Exception()
        head_rq = await self.httpx_client.get(
            response_json["list"][0]["dlink"],follow_redirects=False
        )
        if not head_rq.has_redirect_location:
            Exception("Error in get direct link")
        return TeraboxData(
            filename=response_json["list"][0]['server_filename'],
            size=response_json["list"][0]['size'],
            dlink=response_json["list"][0]['dlink'],
            icon_url=response_json["list"][0]['thumbs']['url3'],
        )
    async def generate_link(self,url: str) -> str:
        if not url and not isinstance(url,str):
            raise Exception()
        r = await self._get_data(url)
        if not r.dlink: 
            raise Exception("Probablemente sus cookies son invalidas, debe haber iniciado sesion en la web primero") 
        return r.dlink
    
    # async def download(self,url: str):
    #     if not url and not isinstance(url,str):
    #         raise Exception()
        
    #     r = await self._get_data(url)
    #     if not r.dlink:
    #         raise Exception("Probablemente sus cookies son invalidas, debe haber iniciado sesion en la web primero") 
    #     io = open(r.filename,"wb")
    #     d = await self.httpx_client.get(r.dlink)
    #     for _c in d.iter_bytes():
    #         io.write(_c)

    #         if self.callback:
    #             pass
    #     io.close()

    async def get_thumbs(self,url: str):
        if not url and not isinstance(url,str):
            raise Exception()
        r = await self._get_data(url)
        if not r.icon_url: 
            raise Exception("Probablemente sus cookies son invalidas, debe haber iniciado sesion en la web primero") 
        return r.icon_url
    
    async def get_size(self,url: str):
        if not url and not isinstance(url,str):
            raise Exception()
        r = await self._get_data(url)
        if not r.size: 
            raise Exception("Probablemente sus cookies son invalidas, debe haber iniciado sesion en la web primero") 
        return r.size
    
    async def get_name(self,url: str):
        if not url and not isinstance(url,str):
            raise Exception()
        r = await self._get_data(url)
        if not r.filename: 
            raise Exception("Probablemente sus cookies son invalidas, debe haber iniciado sesion en la web primero") 
        return r.filename