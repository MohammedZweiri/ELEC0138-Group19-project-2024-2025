import os


class Config:
    """Base configuration that other configurations inherit from."""
    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///collected_data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
