from typing import MutableMapping 

import yarl



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


