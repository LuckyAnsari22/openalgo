import logging
from functools import wraps
from typing import Any, Callable

from flask import abort, jsonify

from database.traffic_db import IPBan, logs_session
from utils.ip_helper import get_real_ip, get_real_ip_from_environ

logger = logging.getLogger(__name__)


class SecurityMiddleware:
    """
    Middleware to check for banned IPs and handle security.

    This WSGI middleware intercepts all incoming requests to check if the client's
    IP address is in the ban list.
    """

    def __init__(self, app: Any):
        """
        Initialize the SecurityMiddleware.

        Args:
            app (Any): The WSGI application to wrap.
        """
        self.app = app

    def __call__(self, environ: dict[str, Any], start_response: Callable) -> list[bytes]:
        """
        Intersects the request to check for IP bans.

        Args:
            environ (dict[str, Any]): The WSGI environment dictionary.
            start_response (Callable): The WSGI start_response callable.

        Returns:
            list[bytes]: The WSGI response (Access Denied for banned IPs).
        """
        # Get real client IP (handles proxies)
        client_ip = get_real_ip_from_environ(environ)

        # Check if IP is banned
        if IPBan.is_ip_banned(client_ip):
            # Clean up scoped session — this runs at WSGI level, outside Flask
            # request context, so blueprint/app teardown handlers won't fire.
            logs_session.remove()

            # Return 403 Forbidden for banned IPs
            status = "403 Forbidden"
            headers = [("Content-Type", "text/plain")]
            start_response(status, headers)
            logger.warning(f"Blocked banned IP: {client_ip}")
            return [b"Access Denied: Your IP has been banned"]

        # For non-banned IPs: session cleanup is handled by Flask's
        # teardown_app_request in traffic.py and security.py blueprints.
        return self.app(environ, start_response)


def check_ip_ban(f: Callable) -> Callable:
    """
    Decorator to check if IP is banned before processing request.

    Args:
        f (Callable): The view function to decorate.

    Returns:
        Callable: The decorated function that checks for IP bans.
    """

    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        client_ip = get_real_ip()

        if IPBan.is_ip_banned(client_ip):
            logger.warning(f"Blocked banned IP in decorator: {client_ip}")
            abort(403, description="Access Denied: Your IP has been banned")

        return f(*args, **kwargs)

    return decorated_function


def init_security_middleware(app: Any) -> None:
    """
    Initialize security middleware for the Flask application.

    Args:
        app (Any): The Flask application instance.
    """
    # Wrap the WSGI app with security middleware
    app.wsgi_app = SecurityMiddleware(app.wsgi_app)

    logger.debug("Security middleware initialized")

    # Note: 404 handler is now in app.py to avoid conflicts
    # The main app's 404 handler calls Error404Tracker.track_404()

    # Register 403 error handler for banned IPs
    @app.errorhandler(403)
    def handle_403(e):
        return jsonify({"error": "Access Denied"}), 403

    logger.debug("Security middleware initialized")
