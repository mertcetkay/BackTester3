import pandas as pd
from strategy.exp_moving_average import MovingAverageStrategy
from core.logger import Logger


class Executor:
    def __init__(self, strategy_class, data):
        """
        Executor sınıfı, verilen stratejiyi kullanarak ticaret işlemlerini yürütür.

        Args:
            strategy_class (class): Örneğin, MovingAverageStrategy gibi kullanılacak strateji sınıfı.
            data (pandas.DataFrame): Stratejinin çalışacağı tarihsel veri.
        """
        self.logger = Logger(__name__)
        self.strategy = strategy_class(data)

    def run(self):
        """
        Stratejiyi çalıştırır. Veri üzerinde adım adım ilerleyerek, stratejinin
        ürettiği sinyalleri loglar.
        """
        self.logger.info("Executor başlatıldı.")

        # Strateji verisi üzerinde adım adım döngü simülasyonu
        for i in range(len(self.strategy.data)):
            # Her adımda mevcut veri dilimini güncelle
            current_data = self.strategy.data.iloc[:i + 1]
            self.strategy.on_data(current_data)
            signal = self.strategy.execute()
            self.logger.info(f"Adım {i}: Üretilen sinyal: {signal}")

        self.logger.info("Executor tamamlandı.")
