from random import randint, choice
from string import ascii_lowercase, ascii_uppercase, digits, punctuation


__all__ = ["password"]


def password(
    length: int = 20, punc: str = punctuation
) -> str:
    """Generate strong password

    Keywords:
        length (int): password length
        punc (str): possible punctuation list (not empty)

    Returns:
        str: generated password 
    """
    password = ""
    characters = "".join([ascii_lowercase, ascii_uppercase, digits, punc])

    if not punc:
        raise AttributeError("punc attribute must not be empty")

    if length < 8:
        raise AttributeError("length attribute must be greater than 8")

    while not (
        set(password) & set(ascii_lowercase) and 
        set(password) & set(ascii_uppercase) and 
        set(password) & set(digits) and
        set(password) & set(punc)
    ):
        password = "".join((choice(characters) for _ in range(length)))
    
    return password


'''
def iban() -> str:
    """Generate random valid iban number
    TODO
    """
    pass

def visacard() -> int:
    """
    """
    num = 0
    while not verifycard(num):
        num = int("".join(str(randint(0, 9)) for i, _ in enumerate(range(0, 16))))
    return num

def creditcard(length):
    num = [randint(0, 9) for i, _ in enumerate(range(0, length - 1))]
    checksum = sum(num)%10

    print(num, checksum)

    for i, _ in enumerate(num): 
        if nu

    for i, _ in enumerate(num):
        if i%2 == 0:
            num[i] = int(num[i]/2)

    num = num[::-1]

    num += [checksum]

    return int("".join(str(n) for n in num))


def verifycard(number: int) -> int:
    num = str(number).split()
    
    checksum = num[:-1]

    # Drop the last digit
    if len(num) > 0:
        num = num[:-1]
    
    # Reverse the digits
    num = num[::-1]

    # Multiple odd digits by 2
    for i, _ in enumerate(num): 
        if i%2 == 0:
            num[i] *= 2

    # Subtract 9 to numbers over 9
    for i, _ in enumerate(num):
        if num[i] > 9:
            num[i] -= 9

    return sum(num)%10 == checksum
'''