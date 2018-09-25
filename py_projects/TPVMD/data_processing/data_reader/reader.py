from data_processing.data_reader.read_from import ReadFromLocal, ReadFromServer


class Reader(object):

    def __init__(self, read_from=None):
        self._read_from = read_from

    def set_read_from(self, read_from: str='') -> None:
        if read_from.lower() == 'server':
            self._read_from = ReadFromServer()
        elif read_from.lower() == 'local':
            self._read_from = ReadFromLocal()
        else:
            raise RuntimeError("Unknown read from: {}".format(read_from))

    def read_file(self, path_or_server: str='', time_of_observation: str=''):
        data = self._read_from.read_data(path_or_server, time_of_observation)
        return data
