import numpy as np
from datetime import datetime


class Data(object):

    def __init__(self, data, averaging: float=0.0125):
        # averaging - second
        self._data = None
        self.set_data(new_data=data)
        self._averaging = averaging

    def averaging(self, averaging: float=None, copy_: bool=False):
        if averaging <= self._averaging:
            raise RuntimeError("Error")
        new_data = np.empty(0)
        steps_ = int(round(averaging / self._averaging, 0))
        for i in range(0, len(self._data), steps_):
            new_list = []
            for col in range(len(self._data[0])):
                new_list.append(np.mean(self._data[i:i+steps_][:, col], axis=0))
            new_data = np.append(new_data, np.array(new_list))
        new_data.shape = (int(len(new_data) / 8), 8)
        if copy_:
            self.set_data(new_data)
        self._averaging = averaging
        return new_data

    def create_data_range(self, range_start: datetime=None, range_end: datetime=None, copy_: bool=False):
        new_data = np.empty(0)
        for data in self._data:
            pass
        if copy_:
            self.set_data(new_data)
        return new_data

    def set_data(self, new_data):
        self._data = new_data
