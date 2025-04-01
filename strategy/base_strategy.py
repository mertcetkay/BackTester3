from abc import ABC, abstractmethod
import backtrader as bt


class BaseStrategy(ABC):
    def __init__(self, data):
        self.data = data
        self.initialize()

    @abstractmethod
    def initialize(self):
        """
        Strateji için başlangıç ayarlarını yapar.
        """
        pass

    @abstractmethod
    def on_data(self, new_data):
        """
        Yeni gelen veriyi değerlendirir.

        Args:
            new_data (pandas.DataFrame): Fiyat verilerini içeren DataFrame.
        """
        pass

    @abstractmethod
    def execute(self):
        """
        Stratejinin ana yürütme mantığını tanımlar.
        """
        pass
