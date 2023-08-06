import inspect
import json

import argparse


__all__ = ['argv', 'from_schema', 'from_file']


_types = {
    "str": str,
    "int": int,
    "float": float,
    "complex": complex,
    "bool": bool,
}


class _Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                _Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class _Args(metaclass=_Singleton):
    def __init__(self):
        self._args = {}

    def read(self, schema):
        parser = argparse.ArgumentParser(description=schema['description'])

        for argument in schema['arguments']:
            parser.add_argument(
                '-' + argument['short'],
                '--' + argument['long'],
                help=argument['help'],
                default=argument['default'],
                type=_types[argument['type']],
                metavar=argument['var']
            )

        known_args = parser.parse_known_args()

        for i in inspect.getmembers(known_args[0]):
            if not i[0].startswith('_'):
                if not inspect.ismethod(i[1]):
                    self._args[i[0]] = i[1]

    def __getitem__(self, item):
        if item not in self._args:
            return None

        return self._args[item]


argv = _Args()


def from_schema(schema):
    _Args().read(schema)


def from_file(file):
    with open(file, 'r') as f:
        _Args().read(json.load(f))
