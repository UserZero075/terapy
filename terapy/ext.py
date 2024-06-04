from httpx import Cookies
from typing import Dict
import re

class SessionCookies:
    def __init__(self, cookies_token: str) -> None:
        if not isinstance(cookies_token, str):
            raise Exception("cookies_token only accept strings")
        self._cookies_token = cookies_token
        self._cookies = Cookies()
    def _prepare_to_session(self) -> Cookies:
        self._parse_cookies(self._cookies_token)
        return self._cookies

    def _parse_cookies(self,cookies_string: str) -> Dict[str,str]:
        for s in re.finditer(r'(?P<key>[^=;]+)=(?P<value>[^;]*)',cookies_string):
            try:
                k,v = [s.groupdict()['key'],s.groupdict()['value']]
            except KeyError:
                raise Exception("Error parseando las cookies")
            self._cookies.set(k,v)
        return 

    
