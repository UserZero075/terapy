# Cliente Terabox y TeraboxAsync

---


# Class Terabox

```python

__init__(session: SessionCookies) -> None
"""
Clase Constructora
"""

generate_link(url: str) -> str
"""
Obtiene el link directo para realizar la descarga del archivo
"""

get_name(url: str) -> str
"""
Obtiene el link directo para realizar la descarga del archivo
"""

get_size(url: str) -> str
"""
Obtiene el tamaño del archivo
"""

get_thumbs(url: str) -> str
"""
Obtiene el link directo para realizar la descarga del thumb del archivo
"""

download(
    url: str,
    directory: Optional[str],
    file_name: Optional[str]
) -> str
"""
Crea directorio (si pasa uno como argumento en cambio usa el directorio donde se ejecute el codigo); descarga archivo correspondiente al url pasado como argumento y devuelve la ruta completa del archivo
"""

```

# Class TeraboxAsync

```python

__init__(session: SessionCookies) -> None
"""
Clase Constructora para contexto asincronico
"""

generate_link(url: str) -> str
"""
Obtiene el link directo para realizar la descarga del archivo
"""

get_name(url: str) -> str
"""
Obtiene el link directo para realizar la descarga del archivo
"""

get_size(url: str) -> str
"""
Obtiene el tamaño del archivo
"""

get_thumbs(url: str) -> str
"""
Obtiene el link directo para realizar la descarga del thumb del archivo
"""

download(
    url: str,
    directory: Optional[str],
    file_name: Optional[str]
) -> str
"""
Crea directorio (si pasa uno como argumento en cambio usa el directorio donde se ejecute el codigo); descarga archivo correspondiente al url pasado como argumento y devuelve la ruta completa del archivo
"""

```
