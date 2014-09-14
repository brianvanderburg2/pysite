import copy

class Config(object):
    """ A simple configuration container. """

    def __init__(self, override=None, config=None):
        """ Initialize the configuration object. """
        self._config = {}
        self._override = override

        if isinstance(config, dict):
            self.set(config)

    def set(self, name, value=None):
        """ Set a configuration value. """

        # Create the dict we are setting
        if isinstance(name, dict):
            data = name
        else:
            data = {str(name) : value}

        self._merge(self._config, data)

    def _merge(self, where, data):
        for (name, value) in data.items():
            # Split by '.'
            parts = str(name).split('.')
            name = parts.pop()

            # Process each part
            tmpwhere = where
            for part in parts:
                if not part in tmpwhere or not isinstance(tmpwhere[part], dict):
                    tmpwhere[part] = {}
                tmpwhere = tmpwhere[part]

            # Found where to put it, what to do with the value
            if isinstance(value, dict):
                if not name in tmpwhere or not isinstance(tmpwhere[name], dict):
                    tmpwhere[name] = {}
                self._merge(tmpwhere[name], value)

            elif isinstance(value, (list, tuple)):
                if not name in tmpwhere:
                    tmpwhere[name] = []
                elif not isinstance(tmpwhere[name], list):
                    tmpwhere[name] = [tmpwhere[name]]
                
                tmpwhere[name].extend(value)

            else:
                tmpwhere[name] = value

    def get(self, name, defval=None):
        """ Get a value from the data """
        return copy.deepcopy(self._get(name, defval))

    def _get(self, name, defval=None):
        # Check override first
        override_result = None
        if self._override:
            override_result = self._override.get(name)
            if not override_result is None and not isinstance(override_result, dict):
                return override_result

        # Split by '.'
        parts = str(name).split('.')
        name = parts.pop()

        # Process each part
        tmpwhere = self._config
        for part in parts:
            if part in tmpwhere and isinstance(tmpwhere[part], dict):
                tmpwhere = tmpwhere[part]
            elif not override_result is None:
                return override_result
            else:
                return defval

        # Return the value
        if name in tmpwhere:
            result = tmpwhere[name]
            if override_result is None:
                return result
            elif not isinstance(result, dict):
                return override_result
            else:
                result = copy.deepcopy(result) # Make sure merge doesn't modify our config
                self._merge(result, override_result)
                return result

        elif not override_result is None:
            return override_result
        else:
            return defval

    def all(self, name):
        """ Return all named items from self and override """
        return copy.deepcopy(self._all(name))

    def _all(self, name):
        results = []
        if self._override:
            results.extend(self._override.all(name))
        
        # Split by '.'
        parts = str(name).split('.')
        name = parts.pop()

        # Process each part
        tmpwhere = self._config
        for part in parts:
            if part in tmpwhere and isinstance(tmpwhere[part], dict):
                tmpwhere = tmpwhere[part]
            else:
                return results

        # Return the value
        if name in tmpwhere:
            results.append(tmpwhere[name])

        return results

    def flatten(self, name):
        """ Return all named items from self and override, flattened into a single list """
        results = []
        self._flattenhelper(results, self.all(name))
        return results

    def _flattenhelper(self, target, values):
        """ This should be moved to a utility function called "flatten" """
        for value in values:
            if isinstance(value, (list, tuple)):
                self._flattenhelper(target, value)
            else:
                target.append(value)

