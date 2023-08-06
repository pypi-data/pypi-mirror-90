from spotify_client.config import Config


class TestConfig(object):
    def test_config_setup(self):
        client_id = 'test-client-id'
        secret_key = 'test-secret-key'

        Config.configure(client_id, secret_key)

        assert Config.CLIENT_ID == client_id
        assert Config.SECRET_KEY == secret_key
