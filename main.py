import json
import os
import sys
import pandas as pd
import backtrader as bt

# Gerekli modüllerin içe aktarılması
from connectors.backtester_connector import BacktesterConnector
from connectors.mt5_connector import MetaTrader5Connector
from strategy.exp_moving_average import MovingAverageStrategy


def load_config(file_path):
    """
    Belirtilen JSON konfigürasyon dosyasını yükler.
    """
    try:
        with open(file_path, 'r') as file:
            config = json.load(file)
        return config
    except Exception as e:
        print(f"Konfigürasyon dosyası yüklenemedi: {e}")
        return {}


def run_backtest():
    """
    Backtest modunu çalıştırır:
    - JSON formatındaki backtester konfigürasyonunu yükler.
    - Config içindeki dosya yolunu kullanarak CSV dosyasını okur.
    - DataFrame'i bt.feeds.PandasData formatına çevirir.
    - Backtester connector aracılığıyla stratejiyi yürütür.
    """
    backtest_config_path = os.path.join('config', 'backtester_config.json')
    config = load_config(backtest_config_path)

    # Config içindeki "file_path" değeri kullanılarak CSV dosyasını okuyoruz.
    data_file = config["data"]["file_path"]
    date_column = config["data"]["date_column"]
    price_column = config["data"]["price_column"]

    df = pd.read_csv(data_file, parse_dates=[date_column])

    # DataFrame'i backtrader'ın veri feed'ine çeviriyoruz.
    # Eğer CSV sadece tarih ve fiyat bilgisi içeriyorsa,
    # open, high, low değerlerini price_column olarak ayarlayabiliriz.
    data_feed = bt.feeds.PandasData(
        dataname=df,
        datetime=date_column,
        open=price_column,
        high=price_column,
        low=price_column,
        close=price_column,
        volume=-1,
        openinterest=-1
    )

    backtester = BacktesterConnector(
        MovingAverageStrategy,
        data_feed,
        cash=config["backtester"]["initial_capital"],
        commission=config["backtester"]["commission"]
    )

    results = backtester.run()
    print("Backtest sonuçları:", results)

def run_metatrader5():
    """
    MetaTrader5 modunu çalıştırır:
    - MetaTrader5 konfigürasyonunu yükler.
    - MetaTrader5 connector aracılığıyla bağlantı kurar.
    - Örnek olarak, belirli bir sembol için geçmiş verileri getirir.
    """
    mt5_config_path = os.path.join('config', 'metatrader5_config.json')
    config = load_config(mt5_config_path)

    # Config üzerinden gerekli bilgiler alınır: login, password, server
    login = config.get('login')
    password = config.get('password')
    server = config.get('server')

    mt5_connector = MetaTrader5Connector(login, password, server)
    if not mt5_connector.initialize():
        print("MetaTrader5 bağlantısı kurulamadı.")
        return

    # Örnek veri çekimi: Sembol, timeframe ve bar sayısı config üzerinden veya default değerlerle belirlenir.
    symbol = config.get('symbol', 'EURUSD')

    # MetaTrader5 modülünden timeframe sabiti kullanabilmek için ek içe aktarma yapıyoruz
    import MetaTrader5 as mt5
    timeframe = config.get('timeframe', mt5.TIMEFRAME_H1)
    data = mt5_connector.get_data(symbol, timeframe, n_bars=100)

    if data is not None:
        print("Veri çekildi:")
        print(data.head())
    else:
        print("Veri çekilemedi.")

    # Canlı emir gönderimi örneği (gerçek emir göndermeden önce test edilmelidir):
    # order_result = mt5_connector.send_order(symbol, mt5.ORDER_TYPE_BUY, volume=0.1, price=data['close'].iloc[-1])
    # print("Emir sonucu:", order_result)

    mt5_connector.shutdown()


def main():
    """
    Uygulamanın giriş noktası.
    Komut satırı argümanına göre mod seçimi yapılır:
      - 'backtest': Tarihsel veri üzerinde backtesting yapılır.
      - 'mt5' veya 'metatrader5': MetaTrader5 üzerinden canlı veri ve işlem gerçekleştirilir.
    """
    mode = 'backtest'
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()

    if mode == 'backtest':
        print("Backtest modu seçildi.")
        run_backtest()
    elif mode in ['mt5', 'metatrader5']:
        print("MetaTrader5 modu seçildi.")
        run_metatrader5()
    else:
        print("Geçersiz mod. Lütfen 'backtest' veya 'mt5' (MetaTrader5) modunu seçiniz.")


if __name__ == '__main__':
    main()
