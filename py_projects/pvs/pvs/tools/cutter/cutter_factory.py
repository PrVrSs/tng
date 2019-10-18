from enum import Enum, auto

from .i_cutter import ICutter
from .hls_cutter import HlsCutter
from .dash_cutter import DashCutter


class CutterType(Enum):
    DASH = auto()
    HLS = auto()


class CutterFactory:

    __slots__ = (
        '_builders',
    )

    def __init__(self):
        self._builders = {}

        self._init_builder()

    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super(CutterFactory, cls).__new__(cls)

        return cls._instance

    def create(self, key: CutterType, *args, **kwargs) -> ICutter:
        builder = self._builders.get(key)

        if builder is None:
            raise ValueError(key)

        return builder(*args, **kwargs)

    def _init_builder(self):
        self._builders[CutterType.DASH] = DashCutter
        self._builders[CutterType.HLS] = HlsCutter
