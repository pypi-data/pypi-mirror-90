"""Contains utilities that the api uses."""
import hashlib
import hmac
import time


def get_nonce():
    return int(time.time() * 1000)


def get_signature(message: str, salt: str) -> str:
    return hmac.new(salt.encode(), message.encode(), hashlib.sha512).hexdigest()


def get_digest(message: str) -> str:
    return hashlib.sha512(message.encode()).hexdigest()


def compose_url(url, path: str) -> str:
    result = f"{url}/{path}"
    return result
