import copy

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
        """
        self._config = {}
        self.update(*args)

    def update(self, *args):
        """ Set a configuration value.

            Parameters:

                *args -- One or more configuration objects or dictionaries.

            The configurations from the passed in items will be merged in
            with the current configuration from first to last.  Dictionaries
            will be merged in recursively and lists or tuples will be appeded
            as a list internally.  Additionaly, the names of items in the top
            as well as nested dictionaries will be split by a dot '.' in the
            name to preduce the configuration structure.
        """
        for arg in args:
            if isinstance(arg, dict):
                self._merge(self._config, arg)
            elif isinstance(arg, Config):
                self._merge(self._config, arg._config)

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
                    where[part] = {}
                where = where[part]

            # Found where to put it, what to do with the value
            if isinstance(value, dict):
                # Merge nested items
                if not name in where or not isinstance(where[name], dict):
                    where[name] = {}
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
        if name is None:
            return copy.deepcopy(self._config)

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
            return copy.deepcopy(where[name])
        else:
            return defval

