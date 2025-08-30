from flask import Response, request
from typing import Callable
import functools

class ServerAuth:
    def __init__(self, correct_username: str, correct_password: str):
        self.correct_username = correct_username
        self.correct_password = correct_password

    def check_auth(self, username: str, password: str) -> bool:
        """Check if a username/password combination is valid."""
        return username == self.correct_username and password == self.correct_password

    def authenticate(self) -> Response:
        """Sends a 401 response that enables basic auth."""
        return Response(
            '',
            401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'})

    def requires_auth(self, func: Callable) -> Callable:
        """Decorator to require HTTP Basic Auth on Flask routes."""
        @functools.wraps(func)
        def decorated(*args, **kwargs):
            auth = request.authorization
            if not auth or not self.check_auth(auth.username, auth.password):
                return self.authenticate()
            return func(*args, **kwargs)
        return decorated
