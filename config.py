from configparser import ConfigParser
import os
from pathlib import Path
import cryptocode

THIS_DIR = Path(__file__)
config_path = THIS_DIR.parent
config_path_file = os.path.join(config_path, 'default_config.ini')
# config_path_file = r'C:\Ananda\default_config.ini'


class ConfigDefault:
    config = ConfigParser()
    config.read(config_path_file)
    DEFAULT_CONFIG = config['MAIN']['DEFAULT_CONFIG']
    MODE = config['MAIN']['MODE']
    if DEFAULT_CONFIG == 'ConfigProd':
        SECRET_KEY = config['SECRET_KEY']['CODE']
        SQLALCHEMY_DATABASE_URI_ENCRYPTED = config['DB']['CON_STRING_PROD']
        SQLALCHEMY_DATABASE_URI = cryptocode.decrypt(SQLALCHEMY_DATABASE_URI_ENCRYPTED, SECRET_KEY)
        MAIL_SERVER = 'smtp.googlemail.com'
        MAIL_PORT = '587'
        MAIL_USE_TLS = True
        MAIL_USERNAME_ENCRYPTED = config['EMAIL']['EMAIL_USER']
        MAIL_PASSWORD_ENCRYPTED = config['EMAIL']['EMAIL_PASS']
        MAIL_USERNAME = cryptocode.decrypt(MAIL_USERNAME_ENCRYPTED, SECRET_KEY)
        MAIL_PASSWORD = cryptocode.decrypt(MAIL_PASSWORD_ENCRYPTED, SECRET_KEY)
        MAIL_MNGT = config['EMAIL']['ML_MNGT']
        MAIL_ARACELI = config['EMAIL']['ML_ARACELI']
        MAIL_LOUIS = config['EMAIL']['ML_LOUIS']
        MAIL_BO = config['EMAIL']['ML_BO']
        MAIL_OLAS = config['EMAIL']['ML_OLAS']
        TRADE_FILE_PATH = config['PATH']['TRADE_FILE_PATH']
        EMSX_PATH = config['PATH']['EMSX_PATH']
    elif DEFAULT_CONFIG == 'ConfigUAT':
        SECRET_KEY = config['SECRET_KEY']['CODE']
        SQLALCHEMY_DATABASE_URI_ENCRYPTED = config['DB']['CON_STRING_UAT']
        SQLALCHEMY_DATABASE_URI = cryptocode.decrypt(SQLALCHEMY_DATABASE_URI_ENCRYPTED, SECRET_KEY)
        MAIL_SERVER = 'smtp.googlemail.com'
        MAIL_PORT = '587'
        MAIL_USE_TLS = True
        MAIL_USERNAME_ENCRYPTED = config['EMAIL']['EMAIL_USER']
        MAIL_PASSWORD_ENCRYPTED = config['EMAIL']['EMAIL_PASS']
        MAIL_USERNAME = cryptocode.decrypt(MAIL_USERNAME_ENCRYPTED, SECRET_KEY)
        MAIL_PASSWORD = cryptocode.decrypt(MAIL_PASSWORD_ENCRYPTED, SECRET_KEY)
        MAIL_MNGT = config['EMAIL']['ML_MNGT']
        MAIL_ARACELI = config['EMAIL']['ML_ARACELI']
        MAIL_LOUIS = config['EMAIL']['ML_LOUIS']
        MAIL_BO = config['EMAIL']['ML_BO']
        TRADE_FILE_PATH = config['PATH']['TRADE_FILE_PATH']
    elif DEFAULT_CONFIG == 'ConfigLocal':
        SECRET_KEY = config['SECRET_KEY']['CODE']
        SQLALCHEMY_DATABASE_URI_ENCRYPTED = config['DB']['CON_STRING_LOCAL']
        SQLALCHEMY_DATABASE_URI = cryptocode.decrypt(SQLALCHEMY_DATABASE_URI_ENCRYPTED, SECRET_KEY)
        MAIL_SERVER = 'smtp.googlemail.com'
        MAIL_PORT = '587'
        MAIL_USE_TLS = True
        MAIL_USERNAME_ENCRYPTED = config['EMAIL']['EMAIL_USER']
        MAIL_PASSWORD_ENCRYPTED = config['EMAIL']['EMAIL_PASS']
        MAIL_USERNAME = cryptocode.decrypt(MAIL_USERNAME_ENCRYPTED, SECRET_KEY)
        MAIL_PASSWORD = cryptocode.decrypt(MAIL_PASSWORD_ENCRYPTED, SECRET_KEY)
        MAIL_MNGT = config['EMAIL']['ML_MNGT']
        MAIL_ARACELI = config['EMAIL']['ML_ARACELI']
        MAIL_LOUIS = config['EMAIL']['ML_LOUIS']
        MAIL_BO = config['EMAIL']['ML_BO']
        TRADE_FILE_PATH = config['PATH']['TRADE_FILE_PATH']




