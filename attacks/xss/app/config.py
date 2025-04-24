class Config:
    """Base configuration that other configurations inherit from."""
    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = "sqlite:///collected_data.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Logging
    LOG_LEVEL = "INFO"
