import abc


class AbstractDataReader(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def unpack_file(self, data):
        pass


class DataReader(AbstractDataReader):

    def __init__(self):
        self._predict_length = None
        self._averaging = []

    def unpack_file(self, data):
        pass

    def predict_length(self):
        return self._predict_length
