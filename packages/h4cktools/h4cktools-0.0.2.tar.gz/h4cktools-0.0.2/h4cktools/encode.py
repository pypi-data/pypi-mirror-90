# Encoder
from base64 import (
    urlsafe_b64encode, 
    urlsafe_b64decode, 
    b64encode as _b64encode, 
    b64decode as _b64decode
)
from typing import Union
import cgi
import html
from urllib.parse import (
    quote_plus,
    unquote_plus
)

__all__ = [
    "b64encode",
    "hexencode",
    "uhexencode",
    "octencode",
    "urlencode",
    "urlb64encode",
    "furlencode",
    "durlencode",
    "htmlencode",
    "fhtmlencode",

    "b64decode",
    "htmldecode",
    "urldecode",
    "urlb64decode",
    "autodecode"
]

## Encoding
def b64encode(obj: Union[str, bytes], encoding="utf-8") -> str:
    """Base64 encode characters of a string 

    Args:
        obj: string or bytes to encode

    Returns:
        str: encoded string
    """
    _obj = obj
    if not isinstance(obj, bytes):
        _obj = str(obj).encode(encoding)
    return _b64encode(_obj).decode(encoding)


def hexencode(s: str, p: str = "\\x") -> str:
    """Hexadecimal encode all characters of a string 

    Args:
        s: string to encode

    Returns:
        str: encoded string
    """
    return "".join(f"{p}{hex(ord(c))[2:]}" for c in s)


def uhexencode(s: str) -> str:
    """Unicode hexadecimal encode all characters of a string 

    Args:
        s: string to encode

    Returns:
        str: encoded string
    """
    return "".join(f"%u00{hex(ord(c))[2:]}" for c in s)

    
def octencode(s: str) -> str:
    """Octal encode all characters of a string 

    Args:
        s: string to encode

    Returns:
        str: encoded string
    """
    return "".join(f"\\{oct(ord(c))}" for c in s)


def urlencode(
    s: str, safe: str = "", encoding: str = "utf-8", errors: str = "replace"
) -> str:
    """Url encode characters of a string 

    Args:
        obj: string or bytes to encode

    Returns:
        str: encoded string
    """
    return quote_plus(s, safe=safe, encoding=encoding, errors=errors)


def urlb64encode(obj: Union[str, bytes], encoding="utf-8") -> str:
    """Url and base64 encode characters of a string 

    Args:
        obj: string or bytes to encode

    Returns:
        str: encoded string
    """
    return b64encode(urlencode(obj, encoding=encoding), encoding=encoding)


def furlencode(s: str) -> str:
    """Url encode all (full) characters of a string
    
    Args:
        s: string to encode
    
    Returns:
        str: encoded string
    """
    return "".join("%{0:0>2}".format(format(ord(c), "x")) for c in s)


def durlencode(s: str) -> str:
    """Double url encode all characters of a string
    
    Args:
        s: string to encode
    
    Returns:
        str: encoded string
    """
    return furlencode(furlencode(s))


def htmlencode(s: str) -> str:
    """HTML escape special characters of a string
    
    Args:
        s: string to encode
    
    Returns:
        str: encoded string
    """
    return html.escape(s, quote=False)


def fhtmlencode(s: str) -> str:
    """HTML escape all (full) characters of a string
    
    Args:
        s: string to encode
    
    Returns:
        str: encoded string
    """
    return "".join(f"&#{ord(c)}" for c in s)


## Decoding

def b64decode(obj: Union[str, bytes], encoding="utf-8") -> str:
    """HTML unescape encoded string

    Args:
        s: string or bytes to decode
    
    Returns:
        str: decoded string
    """
    _obj = obj
    if not isinstance(obj, bytes):
        _obj = str(obj).encode(encoding)
    return _b64decode(_obj).decode(encoding)


def htmldecode(s: str) -> str:
    """HTML unescape encoded string

    Args:
        s: string to decode
    
    Returns:
        str: decoded string
    """
    return html.unescape(s)

def urldecode(s: str, encoding: str = "utf-8", errors: str = "replace") -> str:
    """Url and base64 encode characters of a string 

    Args:
        s: string to decode

    Returns:
        str: decoded string
    """
    return unquote_plus(s, encoding=encoding, errors=errors)


def urlb64decode(obj: Union[str, bytes], encoding="utf-8") -> str:
    """Url and base 64 decode characters of a string

    Args:
        s: string or bytes to decode

    Returns:
        str: decoded string
    """
    _obj = obj
    if not isinstance(obj, bytes):
        _obj = str(obj).encode(encoding)
    return b64decode(urldecode(obj))


def autodecode(string: str) -> str:
    """Detect the string encoding and try to decode
    TODO

    Args:
        s: string to decode
    
    Returns:
        str: decoded string
    """
    pass
