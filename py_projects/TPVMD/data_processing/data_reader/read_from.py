from data_processing.data_reader.data_type.gr_reader import GRReader
from data_processing.data_reader.data_type.mgr_reader import MGRReader
from data_processing.data_reader.data_type.amk_reader import AMKReader
from data_processing.data_reader.server_factory import ServerFactory, read_url
import abc
import os
import numpy as np
from data_processing.data import Data


class AbstractReadFrom(metaclass=abc.ABCMeta):

    def __init__(self):
        if type(self) is AbstractReadFrom:
            raise NotImplementedError()

    @abc.abstractmethod
    def read_data(self):
        """
        :return: generator
        """

    @abc.abstractmethod
    def set_file_type(self):
        """
        set strategy for unpack
        :return:
        """


class ReadFrom(AbstractReadFrom):

    def __init__(self):
        super().__init__()
        self._file_type = None

    def set_file_type(self, file_type: str = '') -> None:
        if file_type.lower() == 'gr':
            self._file_type = GRReader()
        elif file_type.lower() == 'mgr':
            self._file_type = MGRReader()
        elif file_type.lower() == 'amk':
            self._file_type = AMKReader()
        else:
            raise RuntimeError("Unknown file type: {}".format(file_type))

    def read_data(self):
        pass

    def reset_file_type(self):
        self._file_type = None

    def set_extension(self, f):
        _, file_extension = os.path.splitext(f)
        if file_extension == '.07B':
            self.set_file_type('amk')
        else:
            pass


class ReadFromServer(ReadFrom):

    def read_data(self, server_url: str='', time_of_observation: str=''):
        # TODO: решить проблему связанную с многопоточностью: передача генератора с помощью сигнала из 1 потока в другой
        # TODO: расширить для gr и mgr
        server = ServerFactory.create(server_url, time_of_observation)
        file_list = server.get_file_url()
        result_array = np.empty(0)
        for file in file_list:
            self.set_extension(file)
            data = read_url(url=file)
            unpack_data = self._file_type.unpack_file(data)
            for i, el in enumerate(unpack_data):
                result_array = np.append(result_array, el)
            break
        result_array.shape = (int(len(result_array)/8), 8)
        averaging = self._file_type.get_averaging()
        return Data(data=result_array, averaging=averaging)


class ReadFromLocal(ReadFrom):

    def read_data(self, *path):
        if path:
            result_array = np.empty(0)
            if self._file_type is None:
                self.set_extension(path[0])
                # self.set_file_type(file_extension[1:])
            with open(path[0], 'rb') as file_:
                data = file_.read()
                unpack_data = self._file_type.unpack_file(data)
                for i, el in enumerate(unpack_data):
                    result_array = np.append(result_array, el)
            result_array.shape = (int(len(result_array) / 8), 8)
            averaging = self._file_type.get_averaging()
            return Data(data=result_array, averaging=averaging)
