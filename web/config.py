from pathlib import Path


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '0492ad89fc9795d0'
    BASE_DIR = Path(__file__).parent.as_posix()
    IMAGE_UPLOADS = f"{BASE_DIR}/input_images"
    ALLOWED_IMAGE_EXTENSIONS = ["PNG", "JPG"]
    MAX_IMAGE_FILESIZE = 5 * 1024 * 1024


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SECRET_KEY = 'devlopment_key',


class TestingConfig(Config):
    TESTING = True
