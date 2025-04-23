import datetime
import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    # General Flask settings
    API_TITLE = "ELEC0138 Forum API"
    API_VERSION = "0.1.0"

    # flask-smorest settings
    OPENAPI_VERSION = "3.1.0"
    OPENAPI_JSON_PATH = "api-spec.json"
    OPENAPI_URL_PREFIX = "/api/docs"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    API_SPEC_OPTIONS = {
        "components": {
            "securitySchemes": {
                "Bearer Auth": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "Authorization",
                    "bearerFormat": "JWT",
                    "description": "Enter: **'Bearer &lt;JWT&gt;'**, where JWT is the access token",
                }
            }
        },
    }

    # flask-mysql settings
    MYSQL_HOST = os.getenv("MYSQL_HOST", "47.122.18.213")
    MYSQL_USER = os.getenv("MYSQL_USER", "user")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "3aRtVyBN17dUbCq9")
    MYSQL_DB = os.getenv("MYSQL_DB", "ELEC0138")
    MYSQL_CURSORCLASS = "DictCursor"

    # flask-jwt-extended settings
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-super-secret")
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=30)

    # reCAPTCHA
    RECAPTCHA_SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY")

    # Ensure RECAPTCHA_SECRET_KEY is set
    if not RECAPTCHA_SECRET_KEY:
        raise ValueError("Please set the RECAPTCHA_SECRET_KEY environment variable")
