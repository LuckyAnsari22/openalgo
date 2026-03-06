# utils/config.py

import os

from dotenv import load_dotenv

# Load environment variables from .env file with override=True to ensure values are updated
load_dotenv(override=True)


def get_broker_api_key() -> str | None:
    """Retrieve the broker API key from environment variables."""
    return os.getenv("BROKER_API_KEY")


def get_broker_api_secret() -> str | None:
    """Retrieve the broker API secret from environment variables."""
    return os.getenv("BROKER_API_SECRET")


def get_login_rate_limit_min() -> str:
    """Retrieve the per-minute login rate limit from environment variables."""
    return os.getenv("LOGIN_RATE_LIMIT_MIN", "5 per minute")


def get_login_rate_limit_hour() -> str:
    """Retrieve the per-hour login rate limit from environment variables."""
    return os.getenv("LOGIN_RATE_LIMIT_HOUR", "25 per hour")


def get_host_server() -> str:
    """Retrieve the host server URL from environment variables."""
    return os.getenv("HOST_SERVER", "http://127.0.0.1:5000")
