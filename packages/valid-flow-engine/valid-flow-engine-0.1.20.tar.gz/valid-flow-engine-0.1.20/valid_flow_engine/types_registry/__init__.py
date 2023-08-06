from __future__ import annotations
import typing


class UnregisteredTypeError(Exception):
    def __init__(self, type: typing.Type):
        super().__init__(
            f'Type: {type.__name__} has not been registered.'
            'Did you mark it with `@register_type`'
        )


class _TypeRegistry:
    """
    Class to Keep Reference to all Types Used throughout the app
    """

    @property
    def types(self):
        return self.__types

    def __init__(self):
        self.__types: typing.List[typing.Type[BaseModel]] = []

    def __contains__(self, type_):
        return type_ in self.__types

    def register(self, _class: typing.Type[BaseModel]):
        """
        Register a base model to the type registry
        :_class: Class inheriting from `BaseModel`
        """
        if _class not in self.__types:
            self.__types.append(_class)

    def schemas(self, **kwargs) -> str:
        """
        Get the Output Open API Schema for the types
        """
        out = [t.schema_json(**kwargs) for t in self.__types]
        return '\n'.join(out) if 'indent' in kwargs else ''.join(out)


type_registry = _TypeRegistry()


def register_type(_class: typing.Type[BaseModel]) -> typing.Type[BaseModel]:
    """
    Decorator to register then class and the return it, un modified
    """
    type_registry.register(_class)
    return _class


if typing.TYPE_CHECKING:
    pass
if __name__ == '__main__':
    from pydantic import BaseModel

    class T(BaseModel):
        ints: typing.List[int]
        name: str

    print(T.schema_json(indent=2))
