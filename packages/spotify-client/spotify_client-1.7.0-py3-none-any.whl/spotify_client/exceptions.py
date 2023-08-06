from requests.exceptions import HTTPError


class ClientException(Exception):
    """Exception to raise in case of error on our end for request"""


class ImproperlyConfigured(Exception):
    """Exception to raise if client was configured without proper credentials"""


class SpotifyException(HTTPError):
    """Exception to raise in case something bad happens during request"""
    pass
