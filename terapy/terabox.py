from typing import (
    Callable,
    Dict
)
from httpx import (
    Client,
    AsyncClient,
    Response,
    Timeout
)

from .utils import (
    is_valid_url, 
    extract_info,
    extract_url_query,
    create_name_hashed,
    fix_filename
)
from .const import (
    TOKEN_PATTERN,
    DP_PATTERN,
    BASE_URL,
    PARENT_DIR
)
from .ext import SessionCookies
from .types import Function, Args
from .errors import *

from typing import Optional
import inspect,functools,os


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
    client_timeout = 60
    download_timeout = Timeout(timeout=10,read=None)
    def __init__(
            self,session: SessionCookies,
            callback: Optional[Function] = None,
            callback_args: Optional[Args] = None
        ) -> None:
        if not isinstance(session,SessionCookies):
            raise Exception()
        self._session = session._prepare_to_session()
        self._callback = callback
        self._callback_args = callback_args
        
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
    def callback(self,value: Function):
        if not inspect.isfunction(value):
            raise Exception("callback debe ser una funcion")
        self._callback = value

    @property
    def callback_args(self):
        return self._callback_args
    
    @callback_args.setter
    def callback_args(self,value: Args):
        if not isinstance(value,(tuple,list)):
            value = (value)
        self._callback_args = value 

    def _get_data(self,url: str): 
        if not is_valid_url(url):
            raise LinkInvalid()
        init_req_redict = self.httpx_client.get(url,params="")
        if not (200 <= init_req_redict.status_code <= 399):
            raise StatusResponseError(init_req_redict.status_code)
        init_req = self.httpx_client.get(init_req_redict.url,params="")
        if not init_req.is_success:
            raise StatusResponseError(init_req_redict.status_code)
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
            raise StatusResponseError(init_req_redict.status_code)
        response_json = dict(rq.json())
        if response_json.get("errno") or not response_json.get("list",None):
            raise ApiResponseErrno(response_json['errno'])
        head_rq = self.httpx_client.get(
            response_json["list"][0]["dlink"],follow_redirects=False
        )
        if not head_rq.has_redirect_location:
            raise DontRedirect()
        return TeraboxData(
            filename=response_json["list"][0]['server_filename'],
            size=response_json["list"][0]['size'],
            dlink=response_json["list"][0]['dlink'],
            icon_url=response_json["list"][0]['thumbs']['url3'],
        )
    def generate_link(self,url: str) -> str:
        if not url and not isinstance(url,str):
            raise LinkInvalid()
        r = self._get_data(url)
        if not r.dlink: 
            raise CookiesError()
        return r.dlink
    

    def get_thumbs(self,url: str):
        if not url and not isinstance(url,str):
            raise TypeError("\"(url) is type str not \"" + type(url))
        r = self._get_data(url)
        if not r.icon_url: 
            raise CookiesError()
        return r.icon_url
    
    def get_size(self,url: str):
        if not url and not isinstance(url,str):
            raise TypeError("\"(url) is type str not \"" + type(url))
        r = self._get_data(url)
        if not r.size: 
            raise CookiesError()
        return r.size
    
    def get_name(self,url: str):
        if not url and not isinstance(url,str):
            raise TypeError("\"(url) is type str not \"" + type(url))
        r = self._get_data(url)
        if not r.filename: 
            raise CookiesError()
        return r.filename
    
    def download(
            self, 
            url: str,
            directory: Optional[str] = PARENT_DIR,
            file_name: Optional[str] = None
            ) -> str:
        if not url and not isinstance(url,str):
            raise TypeError("\"(url) is type str not \"" + type(url))
        r = self._get_data(url)
        if not r.dlink:
            raise CookiesError()
        
        if directory != PARENT_DIR:
            if not os.path.exists(directory): os.mkdir(directory)
        if not file_name and not r.filename:
            file_name = create_name_hashed()
        elif not file_name and r.filename:
            file_name = r.filename
        
        file_name = fix_filename(file_name)
        path = os.path.join(directory,file_name)
        with Client() as download_instance:
            with open(path,"wb") as f:
                resp_redirect = download_instance.get(r.dlink,timeout=self.download_timeout,follow_redirects=False)
                if not resp_redirect.has_redirect_location:
                    raise Exception()
                dl_url = resp_redirect.headers['location']
                download_instance.cookies = resp_redirect.cookies
                with download_instance.stream("GET",dl_url,timeout=self.download_timeout) as resp:
                    for b in self._get_download(
                        respose=resp,
                        callback=self._callback,
                        callback_args=self._callback_args,
                        total_size=r.size
                    ):
                        f.write(b)
            return path


    def _get_download(self,respose: Response, **kwargs):
        callback_function = kwargs.get("callback")
        callback_args = kwargs.get("callback_args")
        total_size = kwargs.get("total_size")
        current = 0

        for chunk in respose.stream:
            yield chunk
            current += len(chunk)
            if callback_function:
                if not inspect.iscoroutinefunction(callback_function):
                    ...
                else:
                    f = functools.partial(
                        callback_function,
                        *(current,total_size),
                        *callback_args
                    )
                    f()
            continue


class TeraboxAsync:
    httpx_client: AsyncClient
    client_timeout = 60
    download_timeout = Timeout(timeout=10,read=None)
    def __init__(
            self,session: SessionCookies,
            callback: Optional[Function] = None,
            callback_args: Optional[Args] = None
        ) -> None:
        if not isinstance(session,SessionCookies):
            raise TypeError("session is required type SessionCookies")
        self._session = session._prepare_to_session()
        self._callback = callback
        self._callback_args = callback_args

        
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
    def callback(self,value: Function):
        if not inspect.isfunction(value):
            raise Exception("callback debe ser una funcion")
        self._callback = value

    @property
    def callback_args(self):
        return self._callback_args
    
    @callback_args.setter
    def callback_args(self,value: Args):
        if not isinstance(value,(tuple,list)):
            value = (value)
        self._callback_args = value 

    async def _get_data(self,url: str): 
        if not is_valid_url(url):
            raise LinkInvalid()
        init_req_redict = await self.httpx_client.get(url)
        if not (200 <= init_req_redict.status_code <= 399):
            raise StatusResponseError(init_req_redict.status_code)
        init_req = await self.httpx_client.get(init_req_redict.url)
        if not init_req.is_success:
            raise StatusResponseError(init_req_redict.status_code)
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
            raise StatusResponseError(init_req_redict.status_code)
        response_json = dict(rq.json())
        if response_json.get("errno") or not response_json.get("list",None):
            raise ApiResponseErrno(response_json['errno'])
        head_rq = await self.httpx_client.get(
            response_json["list"][0]["dlink"],follow_redirects=False
        )
        if not head_rq.has_redirect_location:
            raise DontRedirect()
        return TeraboxData(
            filename=response_json["list"][0]['server_filename'],
            size=response_json["list"][0]['size'],
            dlink=response_json["list"][0]['dlink'],
            icon_url=response_json["list"][0]['thumbs']['url3'],
        )
    async def generate_link(self,url: str) -> str:
        if not url and not isinstance(url,str):
            raise LinkInvalid()
        r = await self._get_data(url)
        if not r.dlink: 
            raise CookiesError()
        return r.dlink

    async def get_thumbs(self,url: str) -> str:
        if not url and not isinstance(url,str):
            raise TypeError("\"(url) is type str not \"" + type(url))
        r = await self._get_data(url)
        if not r.icon_url: 
            raise CookiesError()
        return r.icon_url
    
    async def get_size(self,url: str) -> int:
        if not url and not isinstance(url,str):
            raise TypeError("\"(url) is type str not \"" + type(url))
        r = await self._get_data(url)
        if not r.size: 
            raise CookiesError()
        return r.size
    
    async def get_name(self,url: str) -> str:
        if not url and not isinstance(url,str):
            raise TypeError("\"(url) is type str not \"" + type(url))
        r = await self._get_data(url)
        if not r.filename: 
            raise CookiesError()
        return r.filename
    
    async def download(
            self, 
            url: str,
            directory: Optional[str] = PARENT_DIR,
            file_name: Optional[str] = None
            ) -> str:
        if not url and not isinstance(url,str):
            raise TypeError("\"(url) is type str not \"" + type(url))
        r = await self._get_data(url)
        if not r.dlink:
            raise CookiesError()
        
        if directory != PARENT_DIR:
            if not os.path.exists(directory): os.mkdir(directory)
        if not file_name and not r.filename:
            file_name = create_name_hashed()
        elif not file_name and r.filename:
            file_name = r.filename
        
        file_name = fix_filename(file_name)
        path = os.path.join(directory,file_name)
        async with AsyncClient() as download_instance:
            with open(path,"wb") as f:
                resp_redirect = await download_instance.get(r.dlink,timeout=self.download_timeout,follow_redirects=False)
                if not resp_redirect.has_redirect_location:
                    raise DontRedirect()
                dl_url = resp_redirect.headers['location']
                download_instance.cookies = resp_redirect.cookies
                async with download_instance.stream("GET",dl_url,timeout=self.download_timeout) as resp:
                    async for b in self._get_download(
                        respose=resp,
                        callback=self._callback,
                        callback_args=self._callback_args,
                        total_size=r.size
                    ):
                        f.write(b)
            return path


    async def _get_download(self,respose: Response, **kwargs):
        callback_function = kwargs.get("callback")
        callback_args = kwargs.get("callback_args")
        total_size = kwargs.get("total_size")
        current = 0

        async for chunk in respose.stream:
            yield chunk
            current += len(chunk)
            if callback_function:
                if not inspect.iscoroutinefunction(callback_function):
                    ...
                else:
                    f = functools.partial(
                        callback_function,
                        *(current,total_size),
                        *callback_args
                    )
                    await f()
            continue
            


        
        
    
