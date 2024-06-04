from httpx import Cookies
from typing import Dict

class SessionCookies:
    def __init__(self, cookies_token: str) -> None:
        if not isinstance(cookies_token, str):
            raise Exception("cookies_token only accept strings")
        self._cookies_token = cookies_token
        self._cookies = Cookies()
    def _prepare_to_session(self) -> Cookies:
        self._parse_cookies(str)
        return self._cookies

    def _parse_cookies(self,cookies_string: str) -> Dict[str,str]:
        for s in cookies_string.split(";"):
            k,v = s.split("=")
            self._cookies.set(k,v)
        return 

    
