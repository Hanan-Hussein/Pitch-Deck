import os


class Config:
    """
    This are the general configurations for the projects
    """
    # the three /// are the relative path from the current file
    # site.db file should get created in the project directory along side py module
  # SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'


# print(os.environ)
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SECRET_KEY = os.environ.get('SECRET_KEY')

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'apollolibrary99@gmail.com'
    MAIL_PASSWORD =  os.environ.get('MAIL_PASSWORD')

    MAIL_USE_TLS = False
    MAIL_USE_SSL = True


class ProdConfig(Config):
    """
    This are the configurations for the production environment
    Args:
        Config : The main configuration
    """
    pass


class DevConfig(Config):
    """
    This are the configurations for the development environment
    Args:
        Config : The main configuration
    """
    DEBUG = True


config_options = {
    'development': DevConfig,
    'production': ProdConfig
}
