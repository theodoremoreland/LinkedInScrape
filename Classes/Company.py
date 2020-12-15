class Company:
    def __init__(self, name, **kwargs):
        self.name = name

        # All those keys will be initialized as class attributes
        allowed_keys = set(['address',
                            'linkedin',
                            'twitter',
                            'facebook',
                            'instagram',
                            'youtube'])

        # Initialize all allowed keys to false
        self.__dict__.update((key, False) for key in allowed_keys)

        # Update the given keys by their given values
        self.__dict__.update((key, value)
                             for key, value in kwargs.items() if key in allowed_keys)