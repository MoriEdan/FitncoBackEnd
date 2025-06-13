# -*- coding: utf-8 -*-
import base64
import random
import string


def random_string(string_length=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


def byte_to_str(byte):
    return str(byte, 'utf-8', 'ignore')


def str_to_base64(data):
    encoded_bytes = base64.b64encode(data.encode("utf-8"))
    encoded_str = str(encoded_bytes, "utf-8")
    return encoded_str
