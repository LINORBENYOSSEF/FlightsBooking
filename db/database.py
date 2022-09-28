from typing import Type, TypeVar, Optional
from contextlib import contextmanager
from pymongo import MongoClient

from .data import Adapter


T = TypeVar('T')


class Database(object):

    def __init__(self):
        self._client = MongoClient()
        self._db = self._client.get_database('test-flightmanager-2')
        self._adapter = Adapter()

    def add(self, value: T, session=None):
        collection = self._db.get_collection(value.__class__.__name__)
        raw = self._adapter.obj_to_dict(value)
        collection.insert_one(raw, session=session)

    def get_all(self, data_type: Type[T], session=None, offset=None, limit=None):
        collection = self._db.get_collection(data_type.__name__)
        results = collection.find(session=session)
        if offset is not None:
            results = results.skip(offset)
        if limit is not None:
            results = results.limit(limit)

        return self._adapter.dict_list_to_obj(list(results), data_type)

    def find_one(self, data_type: Type[T], column: str, value, session=None) -> Optional[T]:
        collection = self._db.get_collection(data_type.__name__)
        result = collection.find_one({column: value}, session=session)
        if result is None:
            return None
        return self._adapter.dict_to_obj(result, data_type)

    def update_one(self, value: T, key_column: str, data_type=None, session=None):
        if data_type is None:
            data_type = value.__class__

        value_dict = self._adapter.obj_to_dict(value, data_type=data_type)
        collection = self._db.get_collection(data_type.__name__)
        collection.update_one({key_column: value_dict[key_column]},
                              {"$set": value_dict}, session=session)

    def delete_one(self, value: T, key_column: str, data_type=None, session=None):
        if data_type is None:
            data_type = value.__class__

        value_dict = self._adapter.obj_to_dict(value, data_type=data_type)
        collection = self._db.get_collection(data_type.__name__)
        collection.delete_one({key_column: value_dict[key_column]}, session=session)

    @contextmanager
    def do_transaction(self):
        with self._client.start_session() as session:
            with session.start_transaction():
                yield session
