__author__ = 'ceremcem'

class Singleton(type):
    """
    Usage example:

        class my_singleton_class(some_other_class):
            __metaclass__ = Singleton

            ... class definition as usual

    """
    def __init__(self, *args, **kwargs):
        super(Singleton, self).__init__(*args, **kwargs)
        self.__instance = None
    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super(Singleton, self).__call__(*args, **kwargs)
        return self.__instance
