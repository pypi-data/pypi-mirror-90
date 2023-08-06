import re


def multiple_strip(input_string: str, char: str) -> str:
    """
    Clean multiple characters in strings to single character
    :param input_string: str
    :param char: str
    :return: str
    """
    if len(char) != 1:
        raise ValueError(f"char has lenght {len(char)}, expected 1")
    return re.sub(f"{char}+", char, input_string)

