from app import *

class Config:
    TABLE_PREFIX = 'hrms_'
    LOGGER_PATH = '/log/'
    SQLALCHEMY_DATABASE_URI = 'postgresql://nikhiltelang:1234@localhost/hrms'
    JWT_SECRET_KEY = 'f942444eb27cdb0dfabcfdb5c06e1ef5e49607e98c7a86bb548ab299ee7696a1'