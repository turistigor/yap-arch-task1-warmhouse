from os import environ

TEMPERATURE_API_URL_DEF = 'http://localhost:8081/temperature'
MONO_API_URL_DEF = 'http://localhost:8080'
TM_DB_URL_DEF = 'postgresql+asyncpg://postgres:postgres@localhost:5433/tm-db'
API_URL_DEF = 'http://localhost:8082'

POLLING_INTERVAL_SEC_DEF = 1


class Settings:
    def __init__(self):
        self.devices_url = environ.get('MONO_API_URL', MONO_API_URL_DEF)
        self.temp_api_url = environ.get('TEMPERATURE_API_URL', TEMPERATURE_API_URL_DEF)
        self.tm_db_url = environ.get('TM_DB_URL', TM_DB_URL_DEF)
        self.polling_interval_sec = int(environ.get('POLLING_INTERVAL_SEC', POLLING_INTERVAL_SEC_DEF))
        self.api_url = environ.get('TM_API_URL', API_URL_DEF)

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(Settings, cls).__new__(cls)
        return cls.instance