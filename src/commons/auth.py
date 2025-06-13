# -*- coding: utf-8 -*-
import functools
from src.commons.request import get_auth_token
from src.commons.response import bad_request_result, forbidden_result


def check(auth_roles, user_roles):
    for auth_role in auth_roles:
        if auth_role in user_roles:
            return True

    return False


def authorize(_func=None, *, user_type: list):  # = ["anonymous", ]
    def decorator_auth(func):

        @functools.wraps(func)
        def wrapper_auth(*args, **kwargs):
            auth_token = get_auth_token()
            user_roles = auth_token["user_type"]

            if user_roles not in user_type:
                return forbidden_result(code=401, message="Bu işlem için yetkiniz bulunmamaktadır.", data=[])

            return func(*args, **kwargs)

        return wrapper_auth

    if _func is None:
        return decorator_auth
    else:
        return decorator_auth(_func)
