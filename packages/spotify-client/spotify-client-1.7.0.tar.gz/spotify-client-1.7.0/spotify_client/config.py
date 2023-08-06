class Config(object):
    """Config module for setting up the client"""

    CLIENT_ID = None
    SECRET_KEY = None

    @classmethod
    def configure(cls, client_id: str, secret_key: str) -> None:
        """
        Configure the library to use the Spotify credentials passed

        :param client_id: (str) Spotify client ID to use in requests
        :param secret_key: (str) Spotify secret key to use in requests
        """
        cls.CLIENT_ID = client_id
        cls.SECRET_KEY = secret_key

    @classmethod
    def clear_config(cls):
        """
        Clear the configuration set for the class
        """
        cls.CLIENT_ID = None
        cls.SECRET_KEY = None
