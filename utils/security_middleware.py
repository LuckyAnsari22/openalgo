import logging
from functools import wraps
from typing import Any, Callable

from flask import abort, jsonify, request

from database.traffic_db import Error404Tracker, IPBan, logs_session
from utils.ip_helper import get_real_ip, get_real_ip_from_environ

logger = logging.getLogger(__name__)


class SecurityMiddleware:
    """Middleware to check for banned IPs and handle security"""

    def __init__(self, app: Any) -> None:
        """Initialize the SecurityMiddleware.

        Args:
            app (Any): The WSGI application structure.
        """
        self.app = app

    def __call__(self, environ: dict[str, Any], start_response: Callable) -> Any:
        """Process WSGI requests and block banned IP addresses.

        Args:
            environ (dict[str, Any]): The WSGI environment.
            start_response (Callable): The WSGI start response callable.

        Returns:
            Any: The response from the WSGI application.
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
    """Decorator to check if IP is banned before processing request.

    Args:
        f (Callable): The route function to wrap.

    Returns:
        Callable: The decorated route function.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        client_ip = get_real_ip()

        if IPBan.is_ip_banned(client_ip):
            logger.warning(f"Blocked banned IP in decorator: {client_ip}")
            abort(403, description="Access Denied: Your IP has been banned")

        return f(*args, **kwargs)

    return decorated_function


def init_security_middleware(app):
    """Initialize security middleware"""
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
