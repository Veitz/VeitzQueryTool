import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTextEdit, QFrame, QHBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Datei, aus der die Werte gelesen werden sollen
datei_pfad = 'btcwerte.txt'

class GraphUpdaterThread(QThread):
    update_plot = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.running = False

    def run(self):
        while self.running:
            werte = self.lese_letzte_werte(datei_pfad)
            if werte:
                self.update_plot.emit(werte)
            time.sleep(1)

    def lese_letzte_werte(self, datei_pfad, anzahl_werte=99):
        try:
            with open(datei_pfad, 'r') as datei:
                zeilen = datei.readlines()
                werte = [float(zeile.strip()) for zeile in zeilen[-anzahl_werte:]]
            return werte
        except Exception as e:
            print(f"Fehler beim Einlesen der Datei: {e}")
            return []

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ONETRADING - BTC Echtzeit-Graph")
        self.setGeometry(100, 100, 800, 600)

        self.text_area = QTextEdit(self)
        self.text_area.setReadOnly(True)
        self.text_area.setPlaceholderText("Dies wird nur funktionieren, wenn du erst die Daten holst ...")

        self.graph_frame = QFrame(self)
        self.graph_frame.setFrameShape(QFrame.Box)
        self.graph_frame.setFrameShadow(QFrame.Raised)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        self.start_button = QPushButton("Start", self)
        self.stop_button = QPushButton("Stop", self)
        self.stop_button.setEnabled(False)

        self.start_button.setFixedWidth(120)
        self.stop_button.setFixedWidth(120)
        self.start_button.setStyleSheet("background-color: lightgreen;")
        self.stop_button.setStyleSheet("background-color: salmon;")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.setAlignment(Qt.AlignCenter)

        graph_layout = QVBoxLayout()
        graph_layout.addLayout(button_layout)
        graph_layout.addWidget(self.canvas)
        self.graph_frame.setLayout(graph_layout)

        layout = QVBoxLayout()
        layout.addWidget(self.text_area)
        layout.addWidget(self.graph_frame)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.thread = GraphUpdaterThread()
        self.thread.update_plot.connect(self.plot_werte)

        self.start_button.clicked.connect(self.start_plotting)
        self.stop_button.clicked.connect(self.stop_plotting)

    def start_plotting(self):
        self.text_area.append("Echtzeit-Plot gestartet...")
        self.thread.running = True
        self.thread.start()
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_plotting(self):
        self.text_area.append("Echtzeit-Plot gestoppt.")
        self.thread.running = False
        self.thread.quit()
        self.thread.wait()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def plot_werte(self, werte):
        self.ax.clear()
        self.ax.plot(werte, marker='o', linestyle='-')
        self.ax.set_title("Letzte 99 BTC-Werte (Echtzeit-Update - Onetrading)")
        self.ax.set_xlabel("Messung")
        self.ax.set_ylabel("BTC-Wert")
        self.ax.grid(True)
        if werte:
            self.ax.set_ylim(min(werte) - 1, max(werte) + 1)
        self.canvas.draw()

        letzter_wert = werte[-1] if werte else "Keine Werte vorhanden"
        self.text_area.append(f"Letzter abgerufener Wert: {letzter_wert}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
