import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'synent-super-secret-key-2026')

    # MySQL connection — update .env with your credentials
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+pymysql://root:Patel_2101@localhost/synent_auth'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Gmail SMTP
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')   # your Gmail address
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')   # Gmail App Password
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME')

    # Token expiry for email verification & password reset (seconds)
    TOKEN_EXPIRY = 3600  # 1 hour