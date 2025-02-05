def apply_decorator_to_methods(decorator, protected_methods: bool = False, private_methods: bool = False):
    """
    Class decorator to apply a given function or coroutine decorator
    to all functions and coroutines within a class.
    """

    def class_decorator(cls):
        for attr_name, attr_value in cls.__dict__.items():
            # Check if the attribute is a callable (method or coroutine)
            if not callable(attr_value):
                continue

            if attr_name.startswith(f"_{cls.__name__}__"):
                if not private_methods:
                    continue

            elif attr_name.startswith("_") and not protected_methods:
                continue

            # Replace the original callable with the decorated version
            setattr(cls, attr_name, decorator(attr_value))
        return cls

    return class_decorator
