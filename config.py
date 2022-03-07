class ConfigDebug():
    # File-based SQL database
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:password@localhost/shop20220128'
    SECRET_KEY = 'SDFA11#'

 # Flask-Mail SMTP server settings
    MAIL_SERVER = '127.0.0.1'
    MAIL_PORT = 1025
    MAIL_USE_SSL = False
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'email@example.com'
    MAIL_PASSWORD = 'password'
    MAIL_DEFAULT_SENDER = '"MyApp" <noreply@example.com>'
    # Flask-User settingsa
    # Shown in and email templates and page footers
    USER_APP_NAME = "Flask-User Basic App"
    USER_ENABLE_EMAIL = True        # Enable email aution
    USER_ENABLE_USERNAME = False    # Disable username authentication
    USER_EMAIL_SENDER_NAME = USER_APP_NAME
    USER_EMAIL_SENDER_EMAIL = "noreply@example.com"
