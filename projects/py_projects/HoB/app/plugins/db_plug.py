import asyncio
from app.interfaces import Plugin


class DBPlugin(Plugin):
    def __init__(self):
        self.keywords = ['plugs']
        self.description = 'Test pluginds'

    def process(self, **kwargs):
        print(kwargs.items())

    def report(self, **kwargs):
        print(kwargs.items())
