import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime


class MetaTrader5Connector:
    def __init__(self, login, password, server):
        """
        MetaTrader 5 bağlantısını başlatır.

        Args:
            login (int): Kullanıcı girişi numarası.
            password (str): Hesap şifresi.
            server (str): Bağlanılacak sunucu adı.
        """
        self.login = login
        self.password = password
        self.server = server

    def initialize(self):
        """
        MetaTrader 5 ile bağlantıyı gerçekleştirir.
        """
        if not mt5.initialize(server=self.server, login=self.login, password=self.password):
            print("initialize() başarısız, hata kodu =", mt5.last_error())
            return False
        print("MetaTrader5 bağlantısı başarılı.")
        return True

    def shutdown(self):
        """
        MetaTrader 5 bağlantısını kapatır.
        """
        mt5.shutdown()
        print("MetaTrader5 bağlantısı kapatıldı.")

    def get_data(self, symbol, timeframe, n_bars=1000):
        """
        Belirtilen sembol için geçmiş verileri getirir.

        Args:
            symbol (str): İşlem sembolü (ör: 'EURUSD').
            timeframe: mt5.TIMEFRAME_* değeri (ör: mt5.TIMEFRAME_H1).
            n_bars (int): Çekilecek bar sayısı.

        Returns:
            pandas.DataFrame: Zaman serisi verileri.
        """
        utc_from = datetime.now() - pd.Timedelta(days=10)  # Örnek: son 10 gün verisi
        rates = mt5.copy_rates_from(symbol, timeframe, utc_from, n_bars)
        if rates is None:
            print("Veri alınamadı, hata:", mt5.last_error())
            return None
        data = pd.DataFrame(rates)
        data['time'] = pd.to_datetime(data['time'], unit='s')
        return data

    def send_order(self, symbol, order_type, volume, price, slippage=20, magic=0, comment=""):
        """
        MetaTrader 5 üzerinden bir emir gönderir.

        Args:
            symbol (str): İşlem sembolü.
            order_type (int): mt5.ORDER_TYPE_* değeri (ör: mt5.ORDER_TYPE_BUY veya mt5.ORDER_TYPE_SELL).
            volume (float): İşlem hacmi.
            price (float): Emir fiyatı.
            slippage (int): Maksimum kayma.
            magic (int): Magic numarası.
            comment (str): Emir yorumu.

        Returns:
            dict: Emir gönderim sonucunu içeren sözlük.
        """
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            print("Sembol bulunamadı:", symbol)
            return None
        if not symbol_info.visible:
            if not mt5.symbol_select(symbol, True):
                print("Sembol görünür hale getirilemedi:", symbol)
                return None

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": order_type,
            "price": price,
            "sl": 0.0,
            "tp": 0.0,
            "deviation": slippage,
            "magic": magic,
            "comment": comment,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(request)
        print("Emir gönderildi:", result)
        return result
