from typing import MutableMapping 
from .const import TERABOX_URL
import re
import yarl
import urllib.parse



def generate_params(query: MutableMapping[str,str]):
    _param = yarl.URL()
    for k,v in query.items():
        if not isinstance(query,str):
            try:
                v.__str__()
            except Exception as ex:
                raise Exception("Valores de los querys deben aceptar conversion a string")
        _param = _param.update_query({k:v})
    return _param.query_string

def extract_url_query(key: str,url: str | yarl.URL):
    if isinstance(url,str):
        _url = yarl.URL(url)
    else: _url = url
    return urllib.parse.parse_qs(_url.query.decode()).get(key,None)[0]
    
    

def extract_info(text: str, pattern: str): 
    return re.search(
        pattern, text
    ).group(1)

def is_valid_url(url: str) -> bool:
    ur = yarl.URL(url)
    return ur.host in TERABOX_URL
    