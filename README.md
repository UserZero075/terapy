# Terapy

**Terapy es una libreria hecha 100% en python para realizar descargas de archivos provenientes de www.terabox.com**


# Guia

- [**Instalacion**](https://github.com/RockstarDevCuba/terapy#instalacion) 
- [**Documentacion**](https://github.com/RockstarDevCuba/terapy/blob/main/docs/docs_guide.md)
- [**Constribuidores**](https://github.com/RockstarDevCuba/terapy#Constribuciones)


# Instalacion

### Usando pip

- **Run `pip install git+https://github.com/RockstarDevCuba/terapy.git@main`**

---

# Mini Guia 


## Extrayendo Cookies

- **Ir a [www.terabox.app](https://www.terabox.app/) y crearse una cuenta, en caso de tener cuenta presente iniciar sesion**

- **Usando el DevTools de tu navegador dirigirte Aplicación y seleccionar Cookies**

- **Una vez seleccionada extraerlas en formato string siguiendo el [ejemplo](https://github.com/RockstarDevCuba/terapy/blob/main/examples/example_cookies.py)**


---

## Uso en el codigo

```python

from terapy import Terabox,SessionCookies


session_cookies = SessionCookies("YOUR COOKIES")

terabox = Terabox(session_cookies)

terabox.download()

```


## 👥 Constribuciones 

**Gracias por su ayuda: [Constribuidores](https://github.com/RockstarDevCuba/terapy/graphs/contributors)**
