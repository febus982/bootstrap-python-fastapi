def apply_decorator_to_methods(
    decorator, protected_methods: bool = False, private_methods: bool = False
):
    """
    Class decorator to apply a given function or coroutine decorator
    to all functions and coroutines within a class.
    """

    def is_private_method(attr_name, cls_name):
        """Check if the attribute is a private method."""
        return attr_name.startswith(f"_{cls_name}__")

    def is_protected_method(attr_name, cls_name):
        """Check if the attribute is a protected method."""
        return attr_name.startswith("_") and not attr_name.startswith(f"_{cls_name}__")

    def class_decorator(cls):
        cls_name = cls.__name__

        for attr_name, attr_value in cls.__dict__.items():
            # Skip attributes that are not callable
            if not callable(attr_value):
                continue

            # Check for private methods
            if is_private_method(attr_name, cls_name):
                if not private_methods:
                    continue

            # Check for protected methods
            elif is_protected_method(attr_name, cls_name) and not protected_methods:
                continue

            # Replace the original callable with the decorated version
            setattr(cls, attr_name, decorator(attr_value))

        return cls

    return class_decorator
