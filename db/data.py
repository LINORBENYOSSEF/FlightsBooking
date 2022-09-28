from typing import Type, TypeVar, Dict, List

from model.base import Model

T = TypeVar('T')


class Adapter(object):

    def dict_to_obj(self, data: Dict, obj_type: Type[T]) -> T:
        fields = Model.get_columns(obj_type)
        obj = obj_type()
        for name, field_type in fields:
            if name not in data:
                continue

            value = data[name]
            if isinstance(value, dict):
                value = self.dict_to_obj(value, field_type)
            if isinstance(value, list):
                value = self.dict_list_to_obj(value, field_type)

            setattr(obj, name, value)

        return obj

    def dict_list_to_obj(self, data: List[Dict], obj_type: Type[T]) -> List[T]:
        return [self.serialized_to_obj(entry, obj_type) for entry in data]

    def serialized_to_obj(self, data, obj_type: Type[T]):
        if isinstance(data, list):
            return self.dict_list_to_obj(data, obj_type)
        return self.dict_to_obj(data, obj_type)

    def obj_to_dict(self, data: T, data_type=None) -> Dict:
        if isinstance(data, dict):
            return data

        if data_type is None:
            data_type = data.__class__

        result = dict()
        fields = Model.get_columns(data_type)
        for name, field_type in fields:
            value = getattr(data, name)
            if isinstance(value, Model):
                value = self.obj_to_dict(value)
            if isinstance(value, list):
                value = self.obj_list_to_dict(value)

            result[name] = value

        return result

    def obj_list_to_dict(self, data: List[T]) -> List[Dict]:
        return [self.obj_to_dict(entry) for entry in data]

    def obj_to_serialized(self, data):
        if isinstance(data, list):
            return self.obj_list_to_dict(data)
        return self.obj_to_dict(data)
