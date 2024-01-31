#!/usr/bin/env python3
"""
Basic auth class
"""

from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """ BasicAuth class
    """

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """extract base64 auth header"""
        if not authorization_header or not isinstance(authorization_header, str) or not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """decode base64 auth header"""
        if not base64_authorization_header or not isinstance(base64_authorization_header, str):
            return None
        try:
            return base64.b64decode(base64_authorization_header).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """extract user credentials"""
        if not decoded_base64_authorization_header or not isinstance(decoded_base64_authorization_header, str) or ':' not in decoded_base64_authorization_header:
            return None, None
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """user object from credentials"""
        if not user_email or not isinstance(user_email, str) or not user_pwd or not isinstance(user_pwd, str):
            return None

        users = User.search({'email': user_email})

        if not users or not users[0].is_valid_password(user_pwd):
            return None

        return users[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """current user"""
        header = self.authorization_header(request)
        if not header:
            return None
        b64 = self.extract_base64_authorization_header(header)
        if not b64:
            return None
        decoded = self.decode_base64_authorization_header(b64)
        if not decoded:
            return None
        user_info = self.extract_user_credentials(decoded)
        if not user_info:
            return None
        email, pwd = user_info
        return self.user_object_from_credentials(email, pwd)
