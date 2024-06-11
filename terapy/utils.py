from typing import MutableMapping
from multidict import MultiDictProxy,MultiDict
from .const import TERABOX_URL
from .types import URLTypes

import re
import yarl
import urllib.parse
import uuid
import datetime



def generate_params(query: MutableMapping[str,str]):
    _param = yarl.URL()
    for k,v in query.items():
        if not isinstance(query,str):
            try:
                v.__str__()
            except Exception as ex:
                raise TypeError("Error to convert value to string")
        _param = _param.update_query({k:v})
    return _param.query_string

def extract_url_query(key: str,url: URLTypes):
    if isinstance(url,str):
        _url = yarl.URL(url)
    else: _url = url
    query = _url.query
    if isinstance(query,(MultiDictProxy,MultiDict)):
        query = _url.query
        return query.get(key,None)
    elif isinstance(query,(str,bytes)):
        return urllib.parse.parse_qs(query.decode()).get(key,None)[0]
    return None
    

def extract_info(text: str, pattern: str): 
    return re.search(
        pattern, text
    ).group(1)

def is_valid_url(url: str) -> bool:
    ur = yarl.URL(url)
    return ur.host in TERABOX_URL
    

def update_many_query(url: URLTypes,mapping: MutableMapping[str,str]) -> str:
    if isinstance(url,str): 
        _url = yarl.URL(url)
    else: _url = url
    for k,v in mapping.items():
        if not k in _url.query.keys():
            raise KeyError(f"error to get {k}")
        _url = _url.update_query({k:v})
    return _url.__str__()


def create_name_hashed():
    return uuid.uuid4().hex + datetime.datetime.now().timestamp().__str__()

def fix_filename(filename: str):
    return urllib.parse.quote(filename,errors="replace")

