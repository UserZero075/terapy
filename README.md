# Terapy (en Desarrollo)
Terapy es una libreria hecha 100% en python para realizar descargas de archivos provenientes de www.terabox.com

# Como Usar: 


```python

from terapy import Terabox,SessionCookies


session_cookies = SessionCookies("YOUR COOKIES")

terabox = Terabox(session_cookies)

terabox.download()


```

# Callback Function:

```python

from terapy import Terabox,SessionCookies

def callback(current,total):
    print(current, total)


session_cookies = SessionCookies("YOUR COOKIES")

terabox = Terabox(session_cookies,callback)

terabox.download()


```

