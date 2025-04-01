import backtrader as bt
from strategy.base_strategy import BaseStrategy


class BacktesterConnector:
    def __init__(self, strategy, data_feed, cash=10000, commission=0.001):
        """
        Backtesting ortamını başlatır.

        Args:
            strategy (class): Çalıştırılacak strateji sınıfı.
            data_feed (bt.feeds.DataBase): Backtrader için uygun veri akışı.
            cash (float): Başlangıç sermayesi.
            commission (float): Komisyon oranı.
        """
        self.cerebro = bt.Cerebro()
        self.strategy = strategy
        self.data_feed = data_feed
        self.cash = cash
        self.commission = commission

    def setup(self):
        # Stratejiyi ekle
        self.cerebro.addstrategy(self.strategy)
        # Başlangıç sermayesini belirle
        self.cerebro.broker.setcash(self.cash)
        # Komisyon oranını ayarla
        self.cerebro.broker.setcommission(commission=self.commission)
        # Veri akışını ekle
        self.cerebro.adddata(self.data_feed)
        print("Backtrader bağlantısı ayarlandı.")

    def run(self):
        """
        Backtesting sürecini başlatır ve sonuçları döner.
        """
        self.setup()
        print("Backtesting başlatılıyor...")
        results = self.cerebro.run()
        print("Backtesting tamamlandı.")
        # Son portföy değerini yazdırır
        print('Final Portfolio Value: %.2f' % self.cerebro.broker.getvalue())
        return results
