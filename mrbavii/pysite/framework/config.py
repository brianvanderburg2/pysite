"""
Configuration container
"""

class _ConfigDict(dict):
    """ A simple immutable configuration dictionary.
        This dictionary once protected will not allow changes to items.  The
        protection will apply recursively to nested lists and dictionaries.
    """

    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__protected = (kwargs.get('protected', False) == True);

    def protect(self):
        if self.__protected:
            return

        for (key, value) in self.items():
            self[key] = self.__protect(value)

        self.__protected = True

    def __protect(self, value):
        if isinstance(value, dict):
            return self.__protect_dict(value)
        elif isinstance(value, list):
            return self.__protect_list(value)
        else:
            return value

    def __protect_dict(self, value):
        if not isinstance(value, _ConfigDict):
            value = _ConfigDict(value)
        value.protect()
        return value

    def __protect_list(self, value):
        clone = list(value)
        for idx in range(len(clone)):
            clone[idx] = self.__protect(clone[idx])

        return tuple(clone)

    def __setitem__(self, name, value):
        if self.__protected:
            raise TypeError("'ConfigDict' object does not support item assignment after being protected")
        else:
            dict.__setitem__(self, name, value)

    def __delitem__(self, name):
        if self.__protected:
            raise TypeError("'ConfigDict' object does not support item deletion after being protected")

    def __repr__(self):
        return "ConfigDict(" + dict.__repr__(self) + (", protected=True)" if self.__protected else ")")


class Config(object):
    """ A simple configuration container.

        A configuration container allows for configuration to be stored and
        used by other components.  When a set of values are set on a
        configuration object, dictionary values are merged and list values
        are appended.

        Some usage examples:

        Default configuration can be provided by a component as shown below.
        In this case, the configuration passed in will overwrite the default
        configuration.

            class Component(object):
                def __init__(self, config):
                    self._config = Config(self.default_config(), config)

                def default_config(self):
                    return {
                        'items': 'values'
                    }

        A global configuration can apply to several components, with per-item
        configuration overriding the global configuration

            global_config = Config({
                'global_items': 'global_values'
            })

            component1_config = Config(global_config, {
                'local_items': 'local_values'
            })

            component2_config = Config(global_config, {
                'local_items', 'local_values'
            })

            ...

            component1 = Component(component1_config)
            component2 = Component(component2_config)
        
    """

    def __init__(self, *args):
        """ Initialize the configuration object.

            Parameters:

                *args -- One or more configuration objects or dictionaries.
            
            The configurations from the passed in items will be merged from
            first to last.  Dictionaries will be merged recursively and lists
            or tuples will be appeded.  Additionaly, the names of items in the
            top as well as nested dictionaries will be split by a dot '.' in
            the name to produce the configuration structure.  After merging,
            the configuration data will be protected to be read-only.
        """

        self._config = None
        
        # No items
        if len(args) == 0:
            return

        # Only one item, we can optimize by making our config point to the
        # other config's dictionary which is already protected
        if len(args) == 1 and isinstance(args[0], Config):
            self._config = args[0]._config
            return

        # Merge in from first to last
        config = _ConfigDict()
        for arg in args:
            if isinstance(arg, dict):
                self._merge(config, arg)
            elif isinstance(arg, Config) and not arg._config is None:
                self._merge(config, arg._config)

        if len(config) != 0:
            config.protect()
            self._config = config

    def _merge(self, target, config):
        """ Merge config into the target recursively. """
        for (name, value) in config.items():
            # Split by '.'
            parts = str(name).split('.')
            name = parts.pop()

            # Process each part
            where = target
            for part in parts:
                if not part in where or not isinstance(where[part], dict):
                    where[part] = _ConfigDict()
                where = where[part]

            # Found where to put it, what to do with the value
            if isinstance(value, dict):
                # Merge nested items
                if not name in where or not isinstance(where[name], dict):
                    where[name] = _ConfigDict()
                self._merge(where[name], value)

            elif isinstance(value, (list, tuple)):
                # Extend the list
                if not name in where:
                    where[name] = []
                elif not isinstance(where[name], list):
                    where[name] = [where[name]]
               
                where[name].extend(value)

            else:
                # Just assign the item
                where[name] = value

    def get(self, name=None, defval=None):
        """ Get a value from the configuration.

            Parameters:

                name -- The name of the item to get.  Set to None to get the
                        entire configuration.
                defval -- The default value to return if the configuration item
                          is not round.

            Returns:

                If name is None, returns the entire configuration.  Otherwise,
                returns the configuration specified by name if it is set or
                defval if it is not set.
        """
        
        # Return total config if requested
        if self._config is None:
            return defval;

        if name is None:
            return self._config;

        # Split by '.'
        parts = str(name).split('.')
        name = parts.pop()

        # Process each part
        where = self._config
        for part in parts:
            if part in where and isinstance(where[part], dict):
                where = where[part]
            else:
                return defval

        # Return the value
        if name in where:
            return where[name]
        else:
            return defval

