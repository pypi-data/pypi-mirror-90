from typing import (
    Any,
    Dict,
    Pattern,
    Callable,
    Union,
    Type,
    Tuple,
    List,
    get_type_hints
)
from abc import ABC, abstractmethod
import inspect
from copy import deepcopy

from pydantic.schema import field_schema, field_class_to_schema, get_flat_models_from_models, get_model_name_map
from pydantic.utils import lenient_issubclass, get_model
from pydantic import BaseModel, BaseConfig, validate_arguments
from pydantic.fields import ModelField

from valid_flow_engine.types_registry import (
    type_registry,
    register_type,
    UnregisteredTypeError
)

object_members = inspect.getmembers(object)


class OpSet(ABC):

    @classmethod
    def export(cls):
        return {
            'description': cls.description()
        }

    @classmethod
    @abstractmethod
    def description(cls):
        pass


class Op:
    def __init__(self, func: Callable, display: str = None, help_text: str = None):
        self.func = validate_arguments(func)
        self.display = display or ''
        self.help_text = help_text or ''

    def call(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def export(self):
        vals = {
            'title': self.display,
            'helpText': self.help_text
        }
        ret = {}
        for key, value in vals.items():
            if value:
                ret[key] = value
        return ret


def put_arg_schema_type(
    arg_type: Any,
    schema: Dict[str, Any],
    extra_data: Dict[str, Any] = {}
) -> None:
    """
    Add Arugment Type information to the provided Schema. If the argument
    type is not from the standard lib, it will provide a reference to
    proper '$ref' in the schemas
    :param: arg_type Type of the argument to find
    :param: schema The Dictionary to Update
    :param: extra_data Dictionary of meta data
            to provide in the entry to the schema
    :returns: None
    :raises: UnregisteredTypeError
    :example:
    ```
    arg_type = int
    schema = {}
    extra_data = {
        'description': 'Integer argument to multiple by'
    }
    put_arg_schema_type(arg_type, schema, extra_data)
    print(schema)
    '''
    {
        'type': 'integer',
        'description': 'Integer argument to multiple by'
    }
    '''
    ```
    """
    found = False
    for type_, t_schema in field_class_to_schema:
        if lenient_issubclass(arg_type, type_) or arg_type is type_ is Pattern:
            d = deepcopy(extra_data)
            d.update(t_schema)
            schema.update(d)
            found = True
            break
    if found:
        return
    if arg_type in type_registry:
        d = deepcopy(extra_data)
        d.update({
            '$ref': f'#/components/schemas/{arg_type.__name__}'
        })
        schema.update(d)
    else:
        raise UnregisteredTypeError(arg_type)


def process_func(func: Union[Callable, Op], schema: Dict[str, Any]):
    models = type_registry.types
    localns = {m.__name__: m for m in models}
    clean_models = [get_model(model) for model in models]

    flat_models = get_flat_models_from_models(clean_models)
    model_name_map = get_model_name_map(flat_models)
    hints = get_type_hints(func, localns=localns)
    args_dict: Dict[str, Any] = {}
    for name, type_ in hints.items():
        field = ModelField(name=name, type_=type_, class_validators=[], model_config=BaseConfig)
        f_schema, f_definitions, f_nested_models = field_schema(field, model_name_map=model_name_map)
        args_dict[name] = f_schema
        if hasattr(type_, '__args__'):
            if any([t == type(None) for t in type_.__args__]):
                args_dict[name].update({'optional': True})
    name = func.__name__
    extra_data = func.op.export()
    extra_data.update({'parameters': args_dict})
    schema.update({name: extra_data})


def process_op_set(class_: Union[Type, OpSet]) -> Dict[str, Dict]:
    class_members = inspect.getmembers(class_)

    def include(member: Tuple[str, Any]) -> bool:
        if member in object_members:
            return False
        if member[0].startswith('__'):
            return False
        func = member[1]
        if isinstance(getattr(func, 'op', None), Op):
            return True
        return False
    members = [m for m in class_members if include(m)]
    func_dict = {}
    for member in members:
        process_func(member[1], func_dict)
    schema = {
        'functions': func_dict
    }
    if isinstance(class_, OpSet):
        schema.update(class_.export())
    return schema


if __name__ == '__main__':
    @register_type
    class Test(BaseModel):
        field: int

    class TestOps:

        @staticmethod
        def test_func(t: Test):
            print(t.field)

        @staticmethod
        def other_func(t: int):
            print(t * 2)

        @staticmethod
        def method(t: List[Test]):
            pass
    import json
    print(json.dumps(process_op_set(TestOps), indent=2))
