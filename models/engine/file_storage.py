#!/usr/bin/python3
'''
file storage
'''
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.place import Place


class FileStorage:
    '''
    serializes and deserialzes json files
    '''

    __file_path = 'file.json'
    __objects = {}
    class_dict = {"BaseModel": BaseModel, "User": User, "Place": Place,
                  "Amenity": Amenity, "City": City, "Review": Review,
                  "State": State}

    def all(self):
        '''
        Return dictionary
        '''
        return self.__objects

    def new(self, obj):
        '''
        Add new obj to existing dictionary
        '''
        if obj:
            key = '{}.{}'.format(obj.__class__.__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        '''
        Save obj dictionaries to json
        '''
        d = {}

        for key, obj in self.__objects.items():
            '''
            if type(obj) is dict:
            my_dict[key] = obj
            '''
            d[key] = obj.to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(d, f)

    def reload(self):
        '''
        convert obj dicts back to instances
        '''
        try:
            with open(self.__file_path, 'r') as f:
                new_obj = json.load(f)
            for k, v in new_obj.items():
                obj = self.class_dict[v['__class__']](**v)
                self.__objects[k] = obj
        except FileNotFoundError:
            pass
