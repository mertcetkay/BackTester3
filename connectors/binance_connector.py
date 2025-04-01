import ccxt
import pandas as pd


class BinanceConnector:
    def __init__(self, exchange_name, api_key, secret, config=None):
        """
        Generic Exchange Connector sınıfı.

        Args:
            exchange_name (str): Bağlanılacak borsanın adı (örn: 'binance', 'coinbasepro').
            api_key (str): API anahtarı.
            secret (str): API gizli anahtarı.
            config (dict, optional): Ek borsa yapılandırma ayarları.
        """
        self.exchange_name = exchange_name
        self.api_key = api_key
        self.secret = secret
        self.config = config if config else {}
        self.exchange = None

    def initialize(self):
        """
        Belirtilen borsa ile bağlantıyı başlatır ve market verilerini yükler.

        Returns:
            bool: Bağlantı başarılı ise True, başarısız ise False.
        """
        try:
            exchange_class = getattr(ccxt, self.exchange_name)
            self.exchange = exchange_class({
                'apiKey': self.api_key,
                'secret': self.secret,
                **self.config
            })
            self.exchange.load_markets()
            print(f"{self.exchange_name} bağlantısı başarılı.")
            return True
        except Exception as e:
            print("Exchange bağlantısı başarısız:", e)
            return False

    def fetch_ticker(self, symbol):
        """
        Belirtilen sembol için en güncel fiyat bilgilerini getirir.

        Args:
            symbol (str): İşlem sembolü (örn: 'BTC/USDT').

        Returns:
            dict: Sembolün fiyat bilgileri (ticker verileri).
        """
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return ticker
        except Exception as e:
            print("Ticker alınamadı:", e)
            return None

    def create_order(self, symbol, order_type, side, amount, price=None):
        """
        Emir gönderir.

        Args:
            symbol (str): İşlem sembolü.
            order_type (str): 'market' veya 'limit' gibi emir tipi.
            side (str): 'buy' veya 'sell' işlemi.
            amount (float): Emir miktarı.
            price (float, optional): Limit emirlerinde gerekli; market emirlerinde kullanılmaz.

        Returns:
            dict: Gönderilen emirle ilgili sonuç.
        """
        try:
            if order_type == 'market':
                order = self.exchange.create_market_order(symbol, side, amount)
            elif order_type == 'limit':
                if price is None:
                    print("Limit emirinde fiyat belirtilmelidir.")
                    return None
                order = self.exchange.create_limit_order(symbol, side, amount, price)
            else:
                print("Desteklenmeyen emir tipi:", order_type)
                return None
            return order
        except Exception as e:
            print("Emir gönderilemedi:", e)
            return None

    def fetch_order(self, order_id, symbol):
        """
        Belirtilen emir bilgisini getirir.

        Args:
            order_id (str): Emir ID'si.
            symbol (str): İşlem sembolü.

        Returns:
            dict: İlgili emrin detayları.
        """
        try:
            order = self.exchange.fetch_order(order_id, symbol)
            return order
        except Exception as e:
            print("Emir bilgisi alınamadı:", e)
            return None

    def cancel_order(self, order_id, symbol):
        """
        Belirtilen emri iptal eder.

        Args:
            order_id (str): İptal edilecek emir ID'si.
            symbol (str): İşlem sembolü.

        Returns:
            dict: İptal işleminin sonucu.
        """
        try:
            result = self.exchange.cancel_order(order_id, symbol)
            return result
        except Exception as e:
            print("Emir iptal edilemedi:", e)
            return None

    def fetch_balance(self):
        """
        Hesap bakiyelerini getirir.

        Returns:
            dict: Hesap bakiyesi bilgileri.
        """
        try:
            balance = self.exchange.fetch_balance()
            return balance
        except Exception as e:
            print("Bakiye bilgileri alınamadı:", e)
            return None
