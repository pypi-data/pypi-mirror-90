import logging
import os


__all__ = ["Logger"]


class Logger:
    """Simple Logger Object"""
    def __init__(self, filename=None, colors=True, verbosity=0):
        self.filename = filename
        self.colors = colors
        self.verbosity = verbosity

        if self.filename:
            with open(self.filename, 'w') as f: 
                f.write("")

    def info(self, msg):
        """
        """
        self._log(f"[*] {msg}")

    def success(self, msg):
        """
        """
        _msg = f"[+] {msg}"
        if self.colors:
            _msg = _msg.join(["\033[32m", "\033[0m"])
        self._log(_msg)

    def partial(self, msg):
        """
        """
        if self.verbosity >= 1:
            _msg = f"[-] {msg}"
            if self.colors:
                _msg = _msg.join(["\033[36m", "\033[0m"])
            self._log(_msg)

    def fail(self, msg):
        """
        """
        if self.verbosity >= 2:
            _msg = f"[.] {msg}"
            if self.colors:
                _msg = _msg.join(["\033[34m", "\033[0m"])
            self._log(_msg)

    def debug(self, msg):
        """
        """
        if self.verbosity >= 3:
            _msg = f"[=] {msg}"
            if self.colors:
                _msg = _msg.join(["\033[2;37m", "\033[0m"])
            self._log(_msg)

    def warning(self, msg):
        """
        """
        _msg = f"[Warning] {msg}"
        if self.colors:
            _msg = _msg.join(["\033[33m", "\033[0m"])
        self._log(_msg)

    def error(self, msg):
        """
        """
        _msg = f"[Error] {msg}"
        if self.colors:
            _msg = _msg.join(["\033[31m", "\033[0m"])
        self._log(_msg)

    def _log(self, msg):
        """
        """
        if self.filename:
            with open(self.filename, "a") as f:
                f.write(f"{msg}{os.linesep}")
        print(msg)
