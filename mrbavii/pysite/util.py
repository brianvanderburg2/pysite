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

class ImmutableDict(dict):
    """ A simple immutable dictionary.
        This dictionary once locked will not allow changes to items.  The
        lock will apply recursively to nested lists and dictionaries.
    """

    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__locked = (kwargs.get('locked', False) == True);

    def lock(self):
        if self.__locked:
            return

        for (key, value) in self.items():
            self[key] = self.__lock(value)

        self.__locked = True

    def __lock(self, value):
        if isinstance(value, dict):
            return self.__lock_dict(value)
        elif isinstance(value, list):
            return self.__lock_list(value)
        else:
            return value

    def __lock_dict(self, value):
        if not isinstance(value, ImmutableDict):
            value = ImmutableDict(value)
        value.lock()
        return value

    def __lock_list(self, value):
        clone = list(value)
        for idx in range(len(clone)):
            clone[idx] = self.__lock(clone[idx])

        return tuple(clone)

    def __setitem__(self, name, value):
        if self.__locked:
            raise TypeError("'ImmutableDict' object does not support item assignment after being locked")
        else:
            dict.__setitem__(self, name, value)

    def __delitem__(self, name):
        if self.__locked:
            raise TypeError("'ImmutableDict' object does not support item deletion after being locked")

    def __repr__(self):
        return "ImmutableDict(" + dict.__repr__(self) + (", locked=True)" if self.__locked else ")")

