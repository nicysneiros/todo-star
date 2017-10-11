import base64
from apistar import http
from apistar.authentication import Authenticated
from apistar.backends.sqlalchemy_backend import Session

from models import User


class BasicAuthentication():
    def authenticate(self, authorization: http.Header, session: Session):
        """
        Determine the user associated with a request,
        using HTTP Basic Authentication.
        """
        if authorization is None:
            return None

        scheme, token = authorization.split()
        if scheme.lower() != 'basic':
            return None

        username, password = base64.b64decode(token).decode('utf-8').split(':')
        print(username)
        user = session.query(User).filter_by(username=username).first()
        if user:
            if user.validate_password(password):
                return Authenticated(username, user=user)

        return None
