from app.interfaces import Plugin


class Plug(Plugin):
    def __init__(self):
        self.keywords = ['plug']
        self.description = 'Test plugin'

    def process(self, **kwargs):
        print(kwargs.items())

    def report(self, **kwargs):
        print(kwargs.items())
