__all__ = ["headers2dict", "query2dict"]


def headers2dict(raw: str) -> dict:
    """Get dictionary from raw HTTP Headers

    Args:
        raw (str): row HTTP headers (e.g.
            Host: Mozilla...
            Cookie: ...
            etc.
        )

    Returns:
        dict: HTTP headers dictionary
    """
    headers = {}
    lines = list(
        filter(None, [line.replace("\t", "") for line in raw.split("\n")])
    )

    for line in lines:
        try:
            name, value = line.split(":", 1)
            if name != "Host":
                headers[name.strip()] = value.strip()
        except ValueError:
            pass
    return headers


def dict2headers(dictionary: dict) -> str:
    """Convert dictionary to HTTP headers string
    TODO
    """
    pass


def query2dict(raw: str) -> dict:
    """Get dictionary from HTTP request parameters

    Args:
        raw (str): HTTP headers as row (e.g.
            name=...&password=...&csrf=...
        )

    Returns:
        dict: HTTP request parameters dictionary
    """
    data = {}
    params = raw.split("&")

    for param in params:
        try:
            name, value = param.split("=", 1)
            data[name] = value
        except ValueError:
            pass

    return data


def dict2query(dictionary: dict) -> str:
    """Convert dictionary to HTTP query string
    TODO
    """
    pass