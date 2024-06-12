class CookiesError(Exception):
    def __init__(self, msg: str = None) -> None:
        super().__init__("Your Cookies are invalid or you don`t log-in, please log-in in terabox.com")

class LinkInvalid(Exception):
    def __init__(self, msg: str = None) -> None:
        super().__init__(f"Link {msg} are invalid\n\nPlease Read: ")

class DontRedirect(Exception):
    def __init__(self, msg: str = None) -> None:
        super().__init__("The Response don`t have a redirect location")

class StatusResponseError(Exception):
    def __init__(self, code: str) -> None:
        super().__init__("Response Code Error: "+ str(code))

class ApiResponseErrno(Exception):
    def __init__(self, error: str) -> None:
        super().__init__("API ERROR: " + error)