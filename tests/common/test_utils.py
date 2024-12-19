import asyncio

import pytest

from common.utils import apply_decorator_to_methods


@pytest.mark.parametrize(
    "apply_to_protected_methods",
    [
        pytest.param(True, id="protected_methods"),
        pytest.param(False, id="no_protected_methods"),
    ],
)
@pytest.mark.parametrize(
    "apply_to_private_methods",
    [
        pytest.param(True, id="private_methods"),
        pytest.param(False, id="no_private_methods"),
    ],
)
async def test_class_decorator(
    apply_to_protected_methods: bool,
    apply_to_private_methods: bool,
):
    def add_ten_decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return result + 10

        async def async_wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            return result + 10

        return wrapper if not asyncio.iscoroutinefunction(func) else async_wrapper

    @apply_decorator_to_methods(
        decorator=add_ten_decorator,
        protected_methods=apply_to_protected_methods,
        private_methods=apply_to_private_methods,
    )
    class MyClass:
        def get_public(self):
            return 10

        def _get_protected(self):
            return 10

        def __get_private(self):
            return 10

        async def get_apublic(self):
            return 10

        async def _get_aprotected(self):
            return 10

        async def __get_aprivate(self):
            return 10

    c = MyClass()
    assert c.get_public() == 20
    assert c._get_protected() == 20 if apply_to_protected_methods else 10
    assert c._MyClass__get_private() == 20 if apply_to_private_methods else 10  # type: ignore
    assert await c.get_apublic() == 20
    assert await c._get_aprotected() == 20 if apply_to_protected_methods else 10
    assert await c._MyClass__get_aprivate() == 20 if apply_to_private_methods else 10  # type: ignore
