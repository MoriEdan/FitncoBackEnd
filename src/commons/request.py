# -*- coding: utf-8 -*-
from flask import request
from flask_jwt_extended import current_user, get_jwt_identity
from typing import TypeVar
from src.commons.exception import ValidationError, AuthenticationError

T = TypeVar('T')


def is_auth():
    try:
        if current_user is not None:
            return True

        return False

    except Exception as ex:
        raise AuthenticationError("request.jwt.authentication_not_found", "" + str(ex))


def get_auth_token(key: str = None):
    """
    print(1, current_user)
    print(2, get_current_user())
    print(3, get_raw_jwt())
    print(4, get_jwt_identity())
    print(5, get_jwt_claims())
    """

    jwt_identity = get_jwt_identity()
    if jwt_identity is None:
        raise AuthenticationError("request.jwt.authentication_identity_not_found", "jwt_identity is null",
                                  "jwt_identity")

    if key is None:
        return jwt_identity

    try:
        value = jwt_identity[key]
        return value

    except Exception:
        raise AuthenticationError("request.jwt.authentication_identity_key_not_found", "key not found", "key")
