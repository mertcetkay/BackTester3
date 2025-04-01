import json
import os
import MetaTrader5 as mt5

#from utils.config_loader import load_config

class MT5Exchange():
    def __init__(self):
        # Config dosyasının aynı klasörde olduğunu belirtiyoruz
        self.config = self.load_config()  # Konfigürasyon dosyasını yükle
        self.connected = False

    def load_config(self):
        # Config dosyasının bulunduğu yolu belirliyoruz
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')  # Aynı klasörde config.json
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config

    def connect(self):
        mt5_config = self.config["mt5"]
        self.connected = mt5.initialize(
            path=mt5_config["path"],
            login=mt5_config["login"],
            password=mt5_config["password"],
            server=mt5_config["server"]
        )
        if not self.connected:
            raise Exception("MT5 bağlantısı kurulamadı")
        else:
            print(f"Bağlantı başarılı: {mt5.version()}")

    def get_historical_data(self, symbol, timeframe, bars):
        timeframes = {
            "M1": mt5.TIMEFRAME_M1,
            "M5": mt5.TIMEFRAME_M5,
            "M15": mt5.TIMEFRAME_M15,
            "H1": mt5.TIMEFRAME_H1,
            "D1": mt5.TIMEFRAME_D1,
        }
        rates = mt5.copy_rates_from_pos(symbol, timeframes[timeframe], 0, bars)
        return rates

    def place_order(self, symbol, lot, order_type, price=None, sl=None, tp=None):
        order_types = {
            "buy": mt5.ORDER_TYPE_BUY,
            "sell": mt5.ORDER_TYPE_SELL,
        }
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": order_types[order_type],
            "price": mt5.symbol_info_tick(symbol).ask if order_type == "buy" else mt5.symbol_info_tick(symbol).bid,
            "sl": sl,
            "tp": tp,
            "deviation": 20,
            "magic": 123456,
            "comment": "Trade from MT5Exchange",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        return mt5.order_send(request)

    def get_account_info(self):
        return mt5.account_info()

    def get_open_positions(self):
        return mt5.positions_get()
