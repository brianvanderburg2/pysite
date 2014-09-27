import copy

class Config(object):
    """ A simple configuration container. """

    def __init__(self, config=None):
        """ Initialize the configuration object. """
        self._config = {}
        self.update(config)

    def update(self, config=None):
        """ Set a configuration value. """

        # Create the dict we are setting
        if isinstance(config, dict):
            self._merge(self._config, config)
        elif isinstance(config, Config):
            self._merge(self._config, config._config)

    def clone(self, config=None):
        """ Return a copy of the configuration. """
        return Config(self._config)

    def _merge(self, target, config):
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

    def get(self, name, defval=None):
        """ Get a value from the data """
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


