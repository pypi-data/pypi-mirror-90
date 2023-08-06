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

    def info(self, msg: str):
        """Log information

        Args:
            msg (str): message to log
        """
        pre = "[.]"
        if self.colors:
            pre = f"\033[2;1m{pre}\033[0m"
        self._log(" ".join([pre, msg]))

    def success(self, msg: str):
        """Log a success

        Args:
            msg (str): message to log
        """
        pre = "[+]"
        if self.colors:
            pre = f"\033[32;1m{pre}\033[0m"
        self._log(" ".join([pre, msg]))

    def partial(self, msg: str):
        """Log a partial success

        Args:
            msg (str): message to log
        """
        pre = "[/]"
        if self.colors:
            pre = f"\033[94;1m{pre}\033[0m"
        self._log(" ".join([pre, msg]))

    def fail(self, msg: str):
        """Log a fail

        Args:
            msg (str): message to log
        """
        pre = "[-]"

        if self.colors:
            pre = f"\033[34;1m{pre}\033[0m"
        self._log(" ".join([pre, msg]))

    def verbose(self, msg: str, v: int = 1):
        """Log an additional information
        
        Args:
            msg (str): message to log
        Keywords:
            v (int): message verbosity number
        """
        if v < 1:
            raise ValueError(f"v keyword must be greater than 1")

        if self.verbosity >= v:
            pre = ("v"*v).join(["[", "]"])
            if self.colors:
                pre = f"\033[90;1m{pre}\033[0m"
            self._log(" ".join([pre, msg]))

    def warning(self, msg):
        """Log a warning

        Args:
            msg (str): message to log
        """
        pre = "[warning]"
        if self.colors:
            pre = f"\033[33m{pre}\033[0m"
        self._log(" ".join([pre, msg]))

    def error(self, msg):
        """Log an error

        Args:
            msg (str): message to log
        """
        pre = "[error]"
        if self.colors:
            pre = f"\033[31m{pre}\033[0m"
        self._log(" ".join([pre, msg]))

    def _log(self, msg: str):
        """Print message and write it in a file

        Args:
            msg (str): message to log
        """
        if self.filename:
            with open(self.filename, "a") as f:
                f.write(f"{msg}{os.linesep}")
        print(msg)
