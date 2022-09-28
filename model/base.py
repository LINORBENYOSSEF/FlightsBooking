import sys
from typing import Type, TypeVar, List

T = TypeVar('T')


class Column(object):

    def __init__(self, field_type, is_many=False):
        self.field_type = field_type
        self.is_many = is_many


class Model(object):

    def __init__(self, **kwargs):
        fields = Model.get_columns(self.__class__)
        for name, field_type in fields:
            if name in kwargs:
                value = kwargs[name]
            else:
                value = None

            setattr(self, name, value)

    def __str__(self):
        fields = Model.get_columns(self.__class__)
        values = [f"{name}={getattr(self, name)}" for name, _ in fields]
        return f"{self.__class__.__name__}({','.join(values)})"

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def get_columns(cls: Type) -> List:
        return [(field, Model.get_field_type(cls, value))
                for field, value in cls.__dict__.items() if isinstance(value, Column)]

    @staticmethod
    def get_field_type(cls: Type, field_type: Column):
        field_type = field_type.field_type

        if isinstance(field_type, str):
            return getattr(sys.modules[cls.__module__], field_type)

        return field_type
