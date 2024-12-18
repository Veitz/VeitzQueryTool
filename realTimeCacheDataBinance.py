import requests
import time
from datetime import datetime
from PyQt5 import QtWidgets, QtCore


class BTCInfoApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.update_btc_info()

    def initUI(self):
        # Fenster und Layout erstellen
        self.setWindowTitle("BINANCE - BTC Live Tracker")
        self.setGeometry(100, 100, 400, 300)

        # Grid-Layout erstellen
        grid_layout = QtWidgets.QGridLayout()

        # Labels für die Beschreibungen und Werte erstellen
        self.label_time_desc = QtWidgets.QLabel("Zeitstempel:")
        self.label_last_price_desc = QtWidgets.QLabel("Letzter Preis (€):")
        self.label_status_desc = QtWidgets.QLabel("Status:")

        # Labels für die angezeigten Werte
        self.label_time = QtWidgets.QLabel("")
        self.label_last_price = QtWidgets.QLabel("")
        self.label_status = QtWidgets.QLabel("Läuft...")

        # Beschreibungen und Werte zum Grid-Layout hinzufügen
        grid_layout.addWidget(self.label_time_desc, 0, 0)
        grid_layout.addWidget(self.label_time, 0, 1)
        grid_layout.addWidget(self.label_last_price_desc, 1, 0)
        grid_layout.addWidget(self.label_last_price, 1, 1)
        grid_layout.addWidget(self.label_status_desc, 2, 0)
        grid_layout.addWidget(self.label_status, 2, 1)

        # Layout setzen
        self.setLayout(grid_layout)

        # Timer erstellen, um die Daten kontinuierlich zu aktualisieren
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_btc_info)
        self.timer.start(4000)  # Aktualisierung alle 1 Sekunde

    def update_btc_info(self):
        try:
            # Hole den aktuellen Bitcoin-Preis
            btc_price = self.get_bitcoin_price_in_eur()

            # Aktualisiere die Labels mit den Werten
            self.label_time.setText(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            self.label_last_price.setText(f"{btc_price:.2f} €")
            self.label_status.setText("Aktualisiert")

            # Speichern des letzten Preises und Beschränkung der Datei auf 100 Zeilen
            self.save_to_file(btc_price)

        except Exception as e:
            # Fehler abfangen und Status aktualisieren
            self.label_status.setText(f"Fehler: {e}")
            print("Fehler beim Abrufen der BTC-Daten:", e)

    def get_bitcoin_price_in_eur(self):
        """
        Holt den aktuellen Bitcoin-Preis in Euro (BTC/EUR) von der Binance API.
        """
        url = "https://api.binance.com/api/v3/ticker/price"
        params = {"symbol": "BTCEUR"}
        response = requests.get(url, params=params)
        response.raise_for_status()  # Fehler auslösen bei HTTP-Problem
        data = response.json()
        return float(data["price"])

    def save_to_file(self, last_price):
        """
        Speichert den letzten Preis in die Datei und beschränkt diese auf 100 Zeilen.
        """
        file_name = "btcwertebinance.txt"
        with open(file_name, "a") as savef:
            savef.write(f"{last_price:.2f}\n")
        self.trim_file_to_last_n_lines(file_name, 100)

    def trim_file_to_last_n_lines(self, file_path, n=100):
        """
        Beschränkt die Datei auf die letzten `n` Zeilen.
        """
        with open(file_path, "r+") as file:
            lines = file.readlines()
            # Behalte nur die letzten `n` Zeilen
            last_n_lines = lines[-n:]
            # Gehe zum Anfang der Datei und überschreibe sie mit den letzten `n` Zeilen
            file.seek(0)
            file.writelines(last_n_lines)
            file.truncate()


# Hauptprogramm
if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = BTCInfoApp()
    window.show()
    sys.exit(app.exec_())
