# -*- coding: utf-8 -*-
import hashlib

from flask_bcrypt import check_password_hash
from flask_bcrypt import generate_password_hash


def hash_sha256(password: str):
    hash_object = hashlib.sha256(password.encode())
    return hash_object.hexdigest()


def hash_bcrypt(password: str):
    password_hash = generate_password_hash(password=password).decode('UTF-8')
    return password_hash


def check_bcrypt(password_hash: str, password: str):
    check = check_password_hash(pw_hash=password_hash, password=password)
    return check


def hash_md5(password: str):
    hash_object = hashlib.md5(str(password).encode())
    return hash_object.hexdigest()
