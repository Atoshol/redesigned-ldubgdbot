class SingletonMeta(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance:
            return cls._instance
        cls._instance = super(SingletonMeta, cls).__call__(*args, **kwargs)
        cls._instance._connection = None
        return cls._instance


# pylint: disable=R0903
class Singleton(metaclass=SingletonMeta):
    """Easy use of SingletonMeta"""
