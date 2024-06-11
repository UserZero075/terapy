# Callback

**Callback viene siendo la referencia de una funcion que acepta 2 parametros:**

- current -> type int or float
- file_info -> type [TeraboxData]()
- Opcional (*args)

**Al usar el metodo `download()` esta se ejecutara en el momento exacto donde ocurre la descarga del archivo (iteracion de bytes) mostrando la informacion anterior**


# Como usar callback y callback_args?

---

## 1 - Callback

```python 
from terapy import Terabox,SessionCookies


def progress_callback(current, file_info): 
    print("Bytes: " str(current))

session = SessionCookies("YOUR COOKIES STRING")

terabox = Terabox(session)
terabox.callback = progress_callback

```

## OR

```python
from terapy import Terabox,SessionCookies


def progress_callback(current, file_info): 
    print("Bytes: " str(current))

session = SessionCookies("YOUR COOKIES STRING")

terabox = Terabox(session, callback = progress_callback)

```

## 2 - Callback Async

```python 
from terapy import TeraboxAsync,SessionCookies


async def progress_callback(current, file_info): 
    print("Bytes: " str(current))

session = SessionCookies("YOUR COOKIES STRING")

terabox = TeraboxAsync(session)
terabox.callback = progress_callback

```

## OR

```python
from terapy import TeraboxAsync,SessionCookies


async def progress_callback(current, file_info): 
    print("Bytes:" str(current))

session = SessionCookies("YOUR COOKIES STRING")

terabox = TeraboxAsync(session, callback = progress_callback)

```

### ⚠️ Nota: Recomendado usar funciones asincronicas para contextos asincronicos y funciones sincronicos para contextos sincronicos

# ¿Como usar callback_args? :

**callback_args te permite pasar más parametros de los obligados que son pasados al llamado de la función. Ejemplo si queremos pasar informacion extra como fechas, informacion de usuarios, informacion de datos, direcciones etc...** 

## 1 - Contexto Sincronico

```python
from terapy import Terabox,SessionCookies


def progress_callback(current, file_info, text, today): 
    print("Today is": str(today))
    print(text + str(current))

session = SessionCookies("YOUR COOKIES STRING")

text = "Bytes Iterados: "
today = "1/12/24"

terabox = Terabox(session)
terabox.callback = progress_callback
terabox.progress_args = (text, today)

```

## OR

```python
from terapy import Terabox,SessionCookies


def progress_callback(current, file_info, text, today): 
    print("Today is": str(today))
    print(text + str(current))

session = SessionCookies("YOUR COOKIES STRING")

text = "Bytes Iterados: "
today = "1/12/24"

terabox = Terabox(session,
    callback = progress_callback,
    progress_args = (text, today))
```

## 3 - Contexto Asincronico

```python
from terapy import TeraboxAsync,SessionCookies


async def progress_callback(current, file_info, text, today): 
    print("Today is": str(today))
    print(text + str(current))

session = SessionCookies("YOUR COOKIES STRING")

text = "Bytes Iterados: "
today = "1/12/24"


terabox = TeraboxAsync(session)
terabox.callback = progress_callback
terabox.progress_args = (text, today)

```

## OR

```python
from terapy import TeraboxAsync,SessionCookies


async def progress_callback(current, file_info, text, today): 
    print("Today is": str(today))
    print(text + str(current))

session = SessionCookies("YOUR COOKIES STRING")

text = "Bytes Iterados: "
today = "1/12/24"


terabox = TeraboxAsync(session,
    callback = progress_callback,
    progress_args = (text, today)
)
```
