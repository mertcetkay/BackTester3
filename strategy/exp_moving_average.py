import pandas as pd
from strategy.base_strategy import BaseStrategy
import backtrader as bt

class MovingAverageStrategy(bt.Strategy):
    def initialize(self):
        """
        Hareketli ortalama stratejisinin başlangıç ayarlarını yapar.
        """


        self.short_window = 40  # Kısa dönem için pencere boyutu
        self.long_window = 100  # Uzun dönem için pencere boyutu
        self.position = 0  # Mevcut pozisyon: 0 = pozisyon yok, 1 = alım, -1 = satış
        print("Hareketli Ortalama Stratejisi başlatıldı.")

    def on_data(self, new_data):
        """
        Yeni gelen veriyi değerlendirir ve hareketli ortalamaları hesaplar.

        Args:
            new_data (pandas.DataFrame): 'close' sütununu içeren fiyat verileri.
        """
        self.data = new_data.copy()
        if len(self.data) >= self.long_window:
            self.data['short_ma'] = self.data['close'].rolling(window=self.short_window).mean()
            self.data['long_ma'] = self.data['close'].rolling(window=self.long_window).mean()

    def execute(self):
        """
        Hareketli ortalama crossover sinyallerine göre alım veya satış sinyali üretir.

        Returns:
            str: Alım, satış sinyali veya veri yetersiz mesajı.
        """
        if len(self.data) < self.long_window:
            return "Yeterli veri yok."

        latest = self.data.iloc[-1]
        previous = self.data.iloc[-2]

        # Kısa MA'nın uzun MA'nın altından uzun MA'nın üstüne geçmesi alım sinyali üretir
        if previous['short_ma'] < previous['long_ma'] and latest['short_ma'] > latest['long_ma']:
            self.position = 1
            return "Alım sinyali"
        # Kısa MA'nın uzun MA'nın üstünden uzun MA'nın altına geçmesi satış sinyali üretir
        elif previous['short_ma'] > previous['long_ma'] and latest['short_ma'] < latest['long_ma']:
            self.position = -1
            return "Satış sinyali"
        else:
            return "Pozisyon değişmedi."
