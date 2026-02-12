import json
import http.client
import requests
from datetime import datetime
import configparser
from PyQt5 import QtWidgets, QtCore


class BTCInfoApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.update_btc_info()

    def initUI(self):
        # Fenster und Layout erstellen
        self.setWindowTitle("Onetrading - BTC Live Tracker")
        self.setGeometry(100, 100, 500, 150)

        # Grid-Layout erstellen
        grid_layout = QtWidgets.QGridLayout()

        # Labels für die Beschreibungen und Werte erstellen
        self.label_time_desc = QtWidgets.QLabel("Zeitstempel-Server:")
        self.label_last_price_desc = QtWidgets.QLabel("Letzter Preis ($):")
        self.label_high_desc = QtWidgets.QLabel("Hoch 24h ($):")
        self.label_low_desc = QtWidgets.QLabel("Tief 24h ($):")
        self.label_orderbook_buy_desc = QtWidgets.QLabel("Orderbook Kauf ($):")
        self.label_orderbook_sell_desc = QtWidgets.QLabel("Orderbook Verkauf ($):")
        self.label_spread_desc = QtWidgets.QLabel("Spread ($):")

        # Labels für die angezeigten Werte
        self.label_time = QtWidgets.QLabel("")
        self.label_last_price = QtWidgets.QLabel("")
        self.label_high = QtWidgets.QLabel("")
        self.label_low = QtWidgets.QLabel("")
        self.label_orderbook_buy = QtWidgets.QLabel("")
        self.label_orderbook_sell = QtWidgets.QLabel("")
        self.label_spread = QtWidgets.QLabel("")

        # Beschreibungen und Werte zum Grid-Layout hinzufügen
        grid_layout.addWidget(self.label_time_desc, 0, 0)
        grid_layout.addWidget(self.label_time, 0, 1)
        grid_layout.addWidget(self.label_last_price_desc, 1, 0)
        grid_layout.addWidget(self.label_last_price, 1, 1)
        grid_layout.addWidget(self.label_high_desc, 2, 0)
        grid_layout.addWidget(self.label_high, 2, 1)
        grid_layout.addWidget(self.label_low_desc, 3, 0)
        grid_layout.addWidget(self.label_low, 3, 1)
        grid_layout.addWidget(self.label_orderbook_buy_desc, 4, 0)
        grid_layout.addWidget(self.label_orderbook_buy, 4, 1)
        grid_layout.addWidget(self.label_orderbook_sell_desc, 5, 0)
        grid_layout.addWidget(self.label_orderbook_sell, 5, 1)
        grid_layout.addWidget(self.label_spread_desc, 6, 0)
        grid_layout.addWidget(self.label_spread, 6, 1)

        # Layout setzen
        self.setLayout(grid_layout)

        # Timer erstellen, um die Daten alle 1 Sekunden zu aktualisieren
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_btc_info)
        self.timer.start(4000)

    def update_btc_info(self):
        try:
            # Hole die aktuellen Bitcoin-Informationen
            btc_info = self.btcinfonow()

            # Aktualisiere die Labels mit den Werten
            self.label_time.setText(str(btc_info["time"]))
            self.label_last_price.setText(f"{btc_info['last_price']:.2f}")
            self.label_high.setText(f"{btc_info['high']:.2f}")
            self.label_low.setText(f"{btc_info['low']:.2f}")
            self.label_orderbook_buy.setText(f"{btc_info['orderbook_buy']:.2f}")
            self.label_orderbook_sell.setText(f"{btc_info['orderbook_sell']:.2f}")
            self.label_spread.setText(f"{btc_info['spread']:.2f}")

            # Speichern der Daten und Beschneiden der Datei auf 100 Zeilen
            self.save_to_file(btc_info["last_price"])
        except Exception as e:
            print("Fehler beim Abrufen der BTC-Daten:", e)

    def btcinfonow(self):
        config = self.read_config()

        headers = {'Accept': 'application/json'}
        response = requests.get('https://api.onetrading.com/fast/v1/market-ticker', params={
            "instrument_code": "BTC_USDC"
        }, headers=headers)
        response.raise_for_status()
        ticker_data = response.json()

        btc_index = int(config['DEFAULT'].get('coinvalbtc', 0))  # Standardwert 0, falls nicht konfiguriert

        # Hole Daten für BTC
        btc_info = {
            "time": datetime.now(),
            "last_price": float(ticker_data[btc_index]['last_price']),
            "high": float(ticker_data[btc_index]['high']),
            "low": float(ticker_data[btc_index]['low']),
            "orderbook_buy": float(self.orderbook_btc_snap('asks')),
            "orderbook_sell": float(self.orderbook_btc_snap('bids')),
            "spread": round(
                float(self.orderbook_btc_snap('asks')) - float(self.orderbook_btc_snap('bids')), 2
            )
        }
        return btc_info

    def orderbook_btc_snap(self, order_type):
        conn = http.client.HTTPSConnection("api.onetrading.com")
        headers = {'Accept': "application/json"}
        conn.request("GET", "/fast/v1/order-book/BTC_USDC", headers=headers)
        response = conn.getresponse()
        data = json.loads(response.read().decode("utf-8"))
        return data[order_type][0]['price']

    def save_to_file(self, last_price):
        try:
            with open("btcwerte.txt", "a") as savef:
                savef.write(f"{last_price:.2f}\n")
            self.trim_file_to_last_n_lines("btcwerte.txt", 100)
        except Exception as e:
            print("Fehler beim Speichern der Daten:", e)

    def trim_file_to_last_n_lines(self, file_path, n=100):
        try:
            with open(file_path, 'r+') as file:
                lines = file.readlines()
                last_n_lines = lines[-n:]
                file.seek(0)
                file.writelines(last_n_lines)
                file.truncate()
        except Exception as e:
            print("Fehler beim Beschneiden der Datei:", e)

    def read_config(self):
        try:
            config = configparser.ConfigParser()
            config.read('CONFIG.INI')
            if 'DEFAULT' not in config:
                raise ValueError("Standardwerte fehlen in der Konfigurationsdatei.")
            return config
        except Exception as e:
            print(f"Fehler beim Lesen der Konfigurationsdatei: {e}")
            raise


# Hauptprogramm
if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = BTCInfoApp()
    window.show()
    sys.exit(app.exec_())
