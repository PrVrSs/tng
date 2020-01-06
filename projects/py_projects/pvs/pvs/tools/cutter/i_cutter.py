from abc import ABC, abstractmethod
from typing import Iterable


class ICutter(ABC):

    @abstractmethod
    async def cut_file(self, input_file: str = '', output_dir: str = '', qualities: Iterable = None):
        raise NotImplementedError()
