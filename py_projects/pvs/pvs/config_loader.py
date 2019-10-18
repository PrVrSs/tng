import os
from configparser import ConfigParser, SectionProxy
from enum import Enum


class Section(Enum):
    GLOBAL = 'GLOBAL'
    PROD = 'PROD'
    DEV = 'DEV'
    TEST = 'TEST'


class Config:

    __slots__ = ()

    configParser = ConfigParser()
    configFilePath = (os.path.join(os.getcwd(), 'config.ini'))
    config_type = Section.DEV

    def __new__(cls, *args, **kwargs):
        if cls is Config:
            return None

        return object.__new__(cls, *args, **kwargs)

    @classmethod
    def initialize(cls, config_file_path: str = '') -> None:
        cls.configParser.read(config_file_path or cls.configFilePath)
        cls.config_type = cls.configParser.get(Section.GLOBAL.name, 'TYPE')

    @classmethod
    def globall(cls, key):
        return cls.configParser.get(Section.GLOBAL.name, key)

    @classmethod
    def get(cls, key):
        if Section(cls.config_type) is Section.PROD:
            return cls._prod(key)
        elif Section(cls.config_type) is Section.DEV:
            return cls._dev(key)

    @classmethod
    def _prod(cls, key):
        return cls.configParser.get(Section.PROD.name, key)

    @classmethod
    def _dev(cls, key):
        return cls.configParser.get(Section.DEV.name, key)
