# -*- coding: utf-8 -*-

import json


class ObjectDict(dict):
    """Makes a dictionary behave like an object, with attribute-style access.
    """

    def __init__(self, *args, **kwargs):

        super(ObjectDict, self).__init__(*args, **kwargs)
        for k, v in self.__class__.__dict__.items():
            if not k.startswith('_'):
                self[k] = v


    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setitem__(self, name, value):
        super(ObjectDict, self).__setitem__(name, value)
        super(ObjectDict, self).__setattr__(name, value)

    def __setattr__(self, name, value):
        super(ObjectDict, self).__setitem__(name, value)
        super(ObjectDict, self).__setattr__(name, value)

    def from_json(self, json_data, json_loads=json.loads):
        self.update(json_loads(json_data))
        return self
