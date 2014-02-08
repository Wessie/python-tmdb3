class AttributeDict(dict):
    """
    Simple dictionary subclass that supports attribute
    access to the dictionary alongside normal access.
    """
    def __init__(self, dct):
        super(AttributeDict, self).__init__(dct)

        self.recursive_instantion()

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            return super(AttributeDict, self).__getattr__(key)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        del self[key]

    def recursive_instantion(self):
        """
        Recursively check if there are any other dicts
        nested in our `self`. Make all we find also an
        `AttributeDict`.

        note: This only checks recursively in dicts and lists
        """
        for key, value in self.items():
            if isinstance(value, dict):
                self[key] = AttributeDict(value)
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, dict):
                        value[i] = AttributeDict(item)
