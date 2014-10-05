"""
Some utility functions
"""

def convert_to_bytes(string, encoding):
    """ Convert a string to bytes if not already bytes. """
    if isinstance(string, bytes):
        return string

    return string.encode(encoding)

def convert_from_bytes(raw, encoding):
    """ Convert a string from bytes if not aready decoded. """
    if isinstance(raw, bytes):
        return raw.decode(encoding)
    return raw



