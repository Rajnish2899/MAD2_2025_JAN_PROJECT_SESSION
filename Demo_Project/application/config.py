class Config():
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATION = True


class LocalDevelopmentConfig(Config):
    # configuration
    SQLALCHEMY_DATABASE_URI = "sqlite:///lmsv2.sqlite3"
    DEBUG = True


    # config for security

    SECRET_KEY = "this-is-a-secret-key" # hash user credentials in session
    # when we login user credentials get stored in session and credentials when get stored get encrypted , that will happened because of secret key
    SECURITY_PASSWORD_HASH = "bcrypt"  # mechanism for hashing password
    SECURITY_PASSWORD_SALT = "this-is-a-password-salt" # this helps in hashing password 
    WTF_CSRF_ENABLED = False # 
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"