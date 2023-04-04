from os import environ

from dotenv import load_dotenv


class Config():
    def __init__(self) -> None:
        self.POSTGRES_USERNAME = environ.get('POSTGRES_USERNAME', 'postgres')
        self.POSTGRES_PASSWORD = environ.get('POSTGRES_PASSWORD', None)
        self.POSTGRES_DB_NAME = environ.get('POSTGRES_DB_NAME', 'pictures')
        self.POSTGRES_DB_HOST = environ.get('POSTGRES_DB_HOST', 'localhost')
        self.POSTGRES_DB_PORT = environ.get('POSTGRES_DB_PORT', '5432')

        self.MESSAGE_BROKER_HOST = environ.get('MESSAGE_BROKER_HOST', 'localhost')
        self.MESSAGE_BROKER_PORT = environ.get('MESSAGE_BROKER_PORT', '5672')
        self.MESSAGE_BROKER_USER = environ.get('MESSAGE_BROKER_USER', 'admin')
        self.MESSAGE_BROKER_PASSWORD = environ.get('MESSAGE_BROKER_PASSWORD', None)

        self.LOCAL_IMAGES_DIR = environ.get('LOCAL_IMAGES_DIR', None)

load_dotenv()

config = Config()
