import unittest
import pandas as pd
import numpy as np
from strategy.exp_moving_average import MovingAverageStrategy


class TestMovingAverageStrategy(unittest.TestCase):
    def setUp(self):
        # Testler için örnek veri seti oluşturuyoruz
        dates = pd.date_range(start='2023-01-01', periods=120, freq='D')
        np.random.seed(42)
        prices = np.linspace(100, 150, 120) + np.random.normal(0, 1, 120)
        self.data = pd.DataFrame({'close': prices}, index=dates)

        # MovingAverageStrategy'yi örnek veriyle başlatıyoruz
        self.strategy = MovingAverageStrategy(self.data)

    def test_on_data(self):
        # on_data metodunun, 'short_ma' ve 'long_ma' sütunlarını eklediğini kontrol ediyoruz.
        self.strategy.on_data(self.data)
        self.assertIn('short_ma', self.strategy.data.columns, "short_ma sütunu eklenmemiş!")
        self.assertIn('long_ma', self.strategy.data.columns, "long_ma sütunu eklenmemiş!")

    def test_execute_no_signal(self):
        # Yeterli veri olmadığında execute metodunun "Yeterli veri yok." mesajı döndürdüğünü test ediyoruz.
        # long_window değerimiz 100 olduğu için 50 veriden oluşan bir veri seti yetersizdir.
        short_data = self.data.iloc[:50]
        self.strategy.on_data(short_data)
        result = self.strategy.execute()
        self.assertEqual(result, "Yeterli veri yok.", "Yetersiz veri durumunda yanlış sonuç!")

    def test_execute_buy_signal(self):
        # Alım sinyali üretecek durumun simülasyonu:
        # Önce veri üzerinde short_ma ve long_ma hesaplamalarını yapıyoruz.
        self.strategy.data = self.data.copy()
        self.strategy.on_data(self.strategy.data)

        # Son iki satırda crossover durumu oluşturuyoruz:
        if len(self.strategy.data) >= 2:
            # Bir önceki satırda kısa MA < uzun MA
            self.strategy.data.iloc[-2, self.strategy.data.columns.get_loc('short_ma')] = 90
            self.strategy.data.iloc[-2, self.strategy.data.columns.get_loc('long_ma')] = 95
            # Son satırda kısa MA > uzun MA
            self.strategy.data.iloc[-1, self.strategy.data.columns.get_loc('short_ma')] = 100
            self.strategy.data.iloc[-1, self.strategy.data.columns.get_loc('long_ma')] = 98

        signal = self.strategy.execute()
        self.assertEqual(signal, "Alım sinyali", "Alım sinyali üretilmedi!")

    def test_execute_sell_signal(self):
        # Satış sinyali üretecek durumun simülasyonu:
        self.strategy.data = self.data.copy()
        self.strategy.on_data(self.strategy.data)

        # Son iki satırda, önce kısa MA > uzun MA, sonra kısa MA < uzun MA olacak şekilde ayarlıyoruz.
        if len(self.strategy.data) >= 2:
            # Bir önceki satırda kısa MA > uzun MA
            self.strategy.data.iloc[-2, self.strategy.data.columns.get_loc('short_ma')] = 110
            self.strategy.data.iloc[-2, self.strategy.data.columns.get_loc('long_ma')] = 105
            # Son satırda kısa MA < uzun MA
            self.strategy.data.iloc[-1, self.strategy.data.columns.get_loc('short_ma')] = 100
            self.strategy.data.iloc[-1, self.strategy.data.columns.get_loc('long_ma')] = 102

        signal = self.strategy.execute()
        self.assertEqual(signal, "Satış sinyali", "Satış sinyali üretilmedi!")


if __name__ == '__main__':
    unittest.main()
