"""LEVEL 09"""

from utils.level_wrapper import level_handler


@level_handler
def solve_level09(_, snow_crash):
    """Decrypt password where each character is rotated by its index"""

    crypted_token = snow_crash.download_data("token")
    # alternative to using "surrogateescape" error handling as detailed in README
    password = "".join([chr(l - i) for i, l in enumerate(crypted_token) if l - i >= 0])
    return "flag", password
