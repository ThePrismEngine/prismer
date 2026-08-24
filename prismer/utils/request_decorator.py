from urllib3.exceptions import ConnectTimeoutError, ReadTimeoutError, SSLError, MaxRetryError, HTTPError

from prismer.locales import _
from prismer.log import error


def request_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ConnectTimeoutError:
            error(_("Таймаут при подключении к серверу"))
        except ReadTimeoutError:
            error(_("Таймаут при чтении ответа от сервера"))
        except SSLError as e:
            error(_("Ошибка SSL/TLS: {e}").format(e=e))
        except MaxRetryError as e:
            error(_("Превышено максимальное число попыток: {e}").format(e=e))
        except HTTPError as e:
            error(_("HTTP-ошибка: {e}").format(e=e))
    return wrapper