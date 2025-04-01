import os
import json

import pandas as pd
from data.data_source.mt5.mt5 import MT5Exchange


def save_rates_to_csv(symbol, timeframe, rates, base_path=None):
    df = pd.DataFrame(rates)
    df["time"] = pd.to_datetime(df["time"], unit="s")

    if base_path is None:
        # 'historical' klasörü fetch_data_main.py'nin bulunduğu yerin içinde olsun
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../historic_data")

    folder_path = os.path.join(base_path, symbol)
    os.makedirs(folder_path, exist_ok=True)

    filename = os.path.join(folder_path, f"{timeframe}.csv")
    df.to_csv(filename, index=False)
    print(f"✅ {symbol} - {timeframe} verisi kaydedildi → {filename}")


def main():
    # Script konumuna göre config path belirle
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "config.json")

    with open(config_path, "r") as f:
        config = json.load(f)

    # MT5'e bağlan
    exchange = MT5Exchange()
    exchange.connect()

    # Her sembol ve zaman dilimi için verileri çek ve kaydet
    for symbol in config["symbols"]:
        for tf in config["timeframes"]:
            print(f"🔄 Veri çekiliyor: {symbol} - {tf}")
            rates = exchange.get_historical_data(symbol, tf, config["bars"])

            if rates is None or len(rates) == 0:
                print(f"❌ Veri alınamadı: {symbol} - {tf}")
                continue

            print(f"🔢 Toplam veri: {len(rates)}")
            save_rates_to_csv(symbol, tf, rates)

    print("📁 Çalışma dizini:", os.getcwd())


if __name__ == "__main__":
    main()
