import re


__all__ = [
    "version_regex", 
    "f_version_regex", 
    "extract_version", 
    "extract_versions",
    "Version"
]


#: Regular expression that match a version
version_regex = r"((?:\d+\.)+\d+)"

#: Regular expression that match a version by specifying its length
#: e.g. f_version_regex.format(2)
f_version_regex = r"((?:\d+\.){}\d+)"


def extract_version(text: str, quantifier: int = 1):
    """Extract version from a string.

    Args:
        text (str): Text that contains a version.

    Keywords:
        quantifier (int): number of numbers expected in the version
            if 1 (default), it will get between 2 and unlimited numbers
            if greater than 1, it will get exact number numbers

    Returns:
        Version: Version if found, None otherwise
    """
    #: Regular expression quantifier
    q = "+"
    if quantifier > 1:
        q = str(quantifier - 1).join(["{", "}"])
    elif quantifier < 1:
        raise ValueError("Qunatifier must be a positive not null integer")
    
    match = re.search(f_version_regex.format(q), text)
    return Version(match.group(1)) if match else None


def extract_versions(text: str) -> list:
    """Extract versions from a string.

    Args:
        text (str): Text that contains a version.

    Returns:
        list: list of founded versions
    """
    versions = re.findall(version_regex, text)
    return [Version(v) for v in versions]


class Version:
    """Object parsing version number"""
    def __init__(self, version: str):
        #: List of numbers in version
        self.nums = [int(n) for n in version.split(".")]

    def __eq__(self, other) -> bool:
        if len(self) != len(other):
            return False

        for i in range(0, len(self)):
            if self.nums[i] != other.nums[i]:
                return False
        return True

    def __lt__(self, other) -> bool:
        for i in range(0, len(min(self.nums, other.nums, key=len))):
            if self.nums[i] < other.nums[i]:
                return True
            if self.nums[i] > other.nums[i]:
                return False
        return False

    def __le__(self, other) -> bool:
        if self == other:
            return True
        return self < other

    def __len__(self) -> int:
        return len(self.nums)

    def __repr__(self) -> str:
        return ".".join([str(num) for num in self.nums])
        