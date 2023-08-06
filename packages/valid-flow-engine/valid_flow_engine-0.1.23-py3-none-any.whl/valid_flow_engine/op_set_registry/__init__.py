import typing
from functools import wraps
from pydantic import validate_arguments

from valid_flow_engine.types_registry import register_type

from valid_flow_engine.op_set_registry.processor import process_op_set, process_func, Op

if typing.TYPE_CHECKING:
    from .typing import AnyCallable, TypeVar

    Callable = TypeVar('Callable', bound=AnyCallable)


class _OpSetRegistry:
    """
    Class to Keep Reference to all Types Used throughout the app
    """

    def __init__(self):
        self.__op_sets = {
            'default': {}
        }
        self.__schemas = {
            'default': {}
        }

    def __contains__(self, type_):
        return type_.__name__ in self.__op_sets

    def register_set(self, _class: typing.Type):
        """
        Register a base model to the type registry
        :_class: a class contaings ops
        """
        if _class.__name__ not in self.__op_sets:
            self.__op_sets[_class.__name__] = _class
            self.__schemas[_class.__name__] = process_op_set(_class)

    def register_op(self, func):
        self.__op_sets['default'][func.__name__] = func
        process_func(func, self.__schemas['default'])

    def schemas(self, **kwargs) -> str:
        """
        Get the Output Open API Schema for the types
        """
        import json
        return json.dumps(self.__schemas, **kwargs)

    def find_op(self, op_set_key: str = 'default', op_key: str = None):
        if op_key is None:
            raise ValueError('Argument `op_key` must be proivded')
        if op_set_key not in self.__op_sets:
            raise ValueError(
                f'op_set_key of: {op_set_key} was not registered, did you '
                'decorate with `@register_op_set`?'
            )
        op_set = self.__op_sets.get(op_set_key)
        if not hasattr(op_set, op_key):
            raise ValueError(
                f'op_key of: {op_key} was not found in {op_set_key} op set'
            )
        return getattr(op_set, op_key)


op_set_registry = _OpSetRegistry()


def register_op_set(_class: typing.Type) -> typing.Type:
    """
    Decorator to register then class and the return it, un modified
    """
    op_set_registry.register_set(_class)
    return _class


def register_op(func):
    op_set_registry.register_op(func)
    return func


def as_op(func=None, *, display=None, help_text=None):
    def create_op(_func):
        op = Op(_func, display, help_text)

        @wraps(_func)
        def wrapper(*args, **kwargs):
            return op.call(*args, **kwargs)

        wrapper.op = op
        return typing.cast('Callable', wrapper)

    if func:
        return create_op(func)
    else:
        return typing.cast('Callable', create_op)

def get_op(op_set_key: str, op_key: str):
    return op_set_registry.find_op(op_set_key, op_key)

if typing.TYPE_CHECKING:
    pass

if __name__ == '__main__':
    from pydantic import BaseModel

    @register_type
    class Test(BaseModel):
        field: int

    @register_op_set
    class TestOps:
        @staticmethod
        @as_op
        def run(t: typing.List[Test]):
            print([_t.field for _t in t])

        @staticmethod
        @as_op(display='Other Runner', help_text='Used to print lines')
        def other_run(t: typing.List[Test]):
            print([_t.field for _t in t])

    opts = [{'field': i} for i in range(0, 10)]
    TestOps.run(opts)
