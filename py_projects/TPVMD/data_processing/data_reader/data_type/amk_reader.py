from data_processing.data_reader.data_type.data_type_reader import DataReader
import struct
import numpy as np
from utility.my_time import to_second


class AMKReader(DataReader):

    def unpack_file(self, bytes_array):
        start_file = bytes_array[:17]
        middle_file = bytes_array[17:-14]
        end_file = bytes_array[-14:]
        start_time = to_second(list(struct.unpack('<hhhhhhhhb', start_file))[:7])
        middle_file = list(struct.iter_unpack('<hhhhhhb', middle_file))
        self._predict_length = len(middle_file)
        end_time = to_second(struct.unpack('<hhhhhhh', end_file))
        instantaneous_value = (end_time - start_time) / self._predict_length
        self._averaging.append(instantaneous_value)
        for middle in middle_file:
            yield np.array([start_time] + list(middle))
            start_time += instantaneous_value

    def get_averaging(self):
        return sum(self._averaging) / len(self._averaging)
