

def is_binary_string(bytes_str):
    """ Use a heuristic to check if the bytes_str are binary data (not text).
    Attention: It will not works in all cases.
    """
    textchars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})
    return bool(bytes_str.translate(None, textchars))


def human_readable_size(size, decimal_places=2):
    """
    Convert the integer bits in a human readable string with Mb, Gb and so on.
    :param size: bits (integer)
    :param decimal_places: decimals to show
    :return: Size in string format.
    """
    for unit in ['bytes', 'Kb', 'Mb', 'Gb', 'Tb', 'Pb']:
        if size < 1024.0 or unit == 'Pb':
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"
