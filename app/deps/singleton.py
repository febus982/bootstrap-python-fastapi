class Singleton(type):
    __instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super(type(cls), cls).__call__(*args, **kwargs)
        return cls.__instances[cls]
