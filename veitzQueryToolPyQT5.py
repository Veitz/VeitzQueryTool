import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QTextEdit, QMainWindow, QAction, QLabel, QMenu, QMessageBox, QGridLayout
import pyfiglet
import requests
import configparser
import veitzQueryToolFunctions
from io import StringIO
import contextlib
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

from realTimeGraph import MainWindow
from realTimeCacheData import BTCInfoApp
from PyQt5.QtCore import QProcess


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        ### Pyfiglet-Text show as QLabel anzeigen ###
        figlet_text = pyfiglet.figlet_format("          VeitzQueryTool")
        #figlet_text = "          VeitzQueryTool"
        figlet_label = QLabel(figlet_text, self)
        figlet_label.setStyleSheet("font-family: monospace; font-size: 15px; text-align: center;")
        layout.addWidget(figlet_label)

        # Text_Edit
        self.text_edit = QTextEdit(self)
        #self.text_edit.setStyleSheet("background-color: black; color: white;")  # Stylechange
        layout.addWidget(self.text_edit)

        # ascii_banner = pyfiglet.figlet_format("VeitzQueryTool")     # in Console
        # print(ascii_banner)

        # Start entry
        try:
            self.text_edit.append("Datetime: " + veitzQueryToolFunctions.stringtimenow() + "\n")
            with redirect_stdout_ext(self.text_edit):
                veitzQueryToolFunctions.json_search()
        except Exception as e:
            self.text_edit.append(f"Error at startup: {e}")

        grid_layout = QGridLayout()

        button1 = QPushButton('buy Bitcoin (with usdc)', self)
        button1.setStyleSheet("background-color: #bfe5ad;")
        button1.clicked.connect(self.button_btc_buy)
        grid_layout.addWidget(button1, 0, 0)

        button2 = QPushButton('sell Bitcoin (to usdc)', self)
        button2.setStyleSheet("background-color: #f09292;")
        button2.clicked.connect(self.button_btc_sell)
        grid_layout.addWidget(button2, 0, 1)

        button3 = QPushButton('buy USDC (with euro)', self)
        button3.setStyleSheet("background-color: #bfe5ad;")
        button3.clicked.connect(self.button_usdc_buy)
        grid_layout.addWidget(button3, 1, 0)

        button4 = QPushButton('sell USDC (to euro)', self)
        button4.setStyleSheet("background-color: #f09292;")
        button4.clicked.connect(self.button_usdc_sell)
        grid_layout.addWidget(button4, 1, 1)

        # Exit Button hinzugefügt
        exitbutton = QPushButton('Exit', self)
        exitbutton.setStyleSheet("background-color: #f0f0f0; color: #333333; border: 1px solid #cccccc;")
        exitbutton.clicked.connect(self.buttonExitClicked)
        layout.addWidget(exitbutton)

        layout.addLayout(grid_layout)
        self.setLayout(layout)



    def button_btc_buy(self):
        try:
            self.text_edit.append("- buy BTC trigger - Datetime: " + veitzQueryToolFunctions.stringtimenow())
            with redirect_stdout_ext(self.text_edit):
                reply = QMessageBox.question(self, 'Bestätigung',
                                             "Möchten Sie BTC kaufen?",
                                             QMessageBox.Yes | QMessageBox.No,
                                             QMessageBox.No)
                if reply == QMessageBox.Yes:
                    veitzQueryToolFunctions.buy_trigger()
                else:
                    print("aborted...")
                    print("")
                    print(">>>")
        except Exception as e:
            self.text_edit.append(f"Error in running external buy_trigger(): {e}")



    def button_btc_sell(self):
        try:
            self.text_edit.append("- sell BTC trigger - Datetime: " + veitzQueryToolFunctions.stringtimenow())
            with redirect_stdout_ext(self.text_edit):
                reply = QMessageBox.question(self, 'Bestätigung',
                                             "Möchten Sie BTC verkaufen?",
                                             QMessageBox.Yes | QMessageBox.No,
                                             QMessageBox.No)
                if reply == QMessageBox.Yes:
                    veitzQueryToolFunctions.sell_trigger()
                else:
                    print("aborted...")
                    print("")
                    print(">>>")
        except Exception as e:
            self.text_edit.append(f"Error in running external sell_trigger(): {e}")



    def button_usdc_buy(self):
        QMessageBox.information(self, 'Information', 'buy USDC action:\n \n'
                                                     'in development...')

    def button_usdc_sell(self):
        QMessageBox.information(self, 'Information', 'sell USDC action:\n \n'
                                                     'in development...')

    def buttonExitClicked(self):
        reply = QMessageBox.question(self, 'Bestätigung',
                                     "Möchten Sie das Programm wirklich beenden?",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            sys.exit()




        


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = MyWidget()
        self.setCentralWidget(self.central_widget)

        # QProcess-Instanzen für externe Programme
        self.process_gui1 = None
        self.process_gui2 = None
        self.process_gui3 = None
        self.process_gui4 = None

        self.initMenu()

        self.setGeometry(500, 300, 850, 768) # def setGeometry (x, y, w, h)   # https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QWidget.html
        self.setWindowTitle(" VeitzQueryTool :: GUI :: QT5 ")

        app_icon = QIcon("icon.png")
        self.setWindowIcon(app_icon)

        self.show()

    def initMenu(self):
        menubar = self.menuBar()

        fileMenu = menubar.addMenu('File')
        dataviewerAction = QAction('Data Viewer', self)
        dataviewerAction.triggered.connect(self.data_viewer)
        fileMenu.addAction(dataviewerAction)
        apiinfoAction = QAction('api Info', self)
        apiinfoAction.triggered.connect(self.api_info)
        fileMenu.addAction(apiinfoAction)
        ## Abstandsbalken im Menü vor "Exit" einfügen ##
        #spacerMenu = QMenu('', self)
        #spacerAct = QAction('', self)
        #spacerAct.setDisabled(True)
        #spacerAct.setVisible(False)
        #spacerMenu.addAction(spacerAct)
        # Horizontaler Strich als Trennung
        fileMenu.addSeparator()
        exitAction = QAction('Exit', self)
        exitAction.triggered.connect(self.close)
        #fileMenu.addMenu(spacerMenu)
        fileMenu.addAction(exitAction)



        fileMenu = menubar.addMenu('Trading')
        btcinfoAction = QAction('show BTC Value', self)
        btcinfoAction.triggered.connect(self.btc_info)
        fileMenu.addAction(btcinfoAction)
        usdcinfoAction = QAction('show USDC Value', self)
        usdcinfoAction.triggered.connect(self.usdc_info)
        fileMenu.addAction(usdcinfoAction)
        ethinfoAction = QAction('show ETH Value', self)
        ethinfoAction.triggered.connect(self.eth_info)
        fileMenu.addAction(ethinfoAction)
        feargreedAction = QAction('show Fear and Greed Index', self)
        feargreedAction.triggered.connect(self.fear_greed)
        fileMenu.addAction(feargreedAction)
        fileMenu.addSeparator()
        mywalletAction = QAction('show myWallet', self)
        mywalletAction.triggered.connect(self.my_wallet)
        fileMenu.addAction(mywalletAction)
        fileMenu.addSeparator()
        shlast100Action = QAction('show last 100 trades', self)
        shlast100Action.triggered.connect(self.show_last100)
        fileMenu.addAction(shlast100Action)
        openordersAction = QAction('show open Orders', self)
        openordersAction.triggered.connect(self.open_orders)
        fileMenu.addAction(openordersAction)


        fileMenu = menubar.addMenu('Real-Time Tools')                           ##########################
        configinfoAction = QAction('get realTime BTC-Value - onetrading', self) ##########################
        configinfoAction.triggered.connect(self.get_realtime_btc_value)         ##########################
        fileMenu.addAction(configinfoAction)                                    ###### RealTimeTools #####
        showconfigAction = QAction('show realTimeGraph - onetrading', self)     ##########################
        showconfigAction.triggered.connect(self.show_real_time_graph)           ##########################
        fileMenu.addAction(showconfigAction)                                    ##########################
        fileMenu.addSeparator()
        configinfoAction = QAction('get realTime BTC-Value - binance', self)    ##########################
        configinfoAction.triggered.connect(self.get_realtime_btc_value_binance) ##########################
        fileMenu.addAction(configinfoAction)                                    ###### RealTimeTools #####
        showconfigAction = QAction('show realTimeGraph - binance', self)        ##########################
        showconfigAction.triggered.connect(self.show_real_time_graph_binance)   ##########################
        fileMenu.addAction(showconfigAction)


        fileMenu = menubar.addMenu('Settings')
        configinfoAction = QAction('config Info/Update', self)
        configinfoAction.triggered.connect(self.config_info)  
        fileMenu.addAction(configinfoAction)
        showconfigAction = QAction('show config.ini', self)
        showconfigAction.triggered.connect(self.show_config)  
        fileMenu.addAction(showconfigAction)



        infoMenu = menubar.addMenu('Info')
        changelogAction = QAction('Changelog', self)
        changelogAction.triggered.connect(self.change_log)
        infoMenu.addAction(changelogAction)
        infoAction = QAction('About', self)
        # Verbindung des triggered-Signals mit einer lambda-Funktion
        version = veitzQueryToolFunctions.get_version()
        infoAction.triggered.connect(lambda: self.showInfo(version))
        infoMenu.addAction(infoAction)

        # ... Weitere Menüpunkte ...



    ### function for menu ###

    def change_log(self):
        # Aktion des Menüeintrags # aus externer Funktion
        try:
            self.central_widget.text_edit.append("Datetime: " + veitzQueryToolFunctions.stringtimenow())
            with redirect_stdout_ext(self.central_widget.text_edit):
                veitzQueryToolFunctions.changelog()
        except Exception as e:
            self.central_widget.text_edit.append(f"Error in running external cc(): {e}")
            #self.text_edit.append(f"Error in running external cc(): {e}")

    """
    def showInfo(self):
        QMessageBox.information(self, 'Information', 'veitzQueryTool made with PyQT5 \n \n'
                                        'v2.0-dev')
    """
    def showInfo(self, version):
        QMessageBox.information(self, 'Information', f'veitzQueryTool made with PyQT5 \n \n'
                                                     f'Version: {version}')








    def btc_info(self):
        # Aktion des Menüeintrags # aus externer Funktion
        try:
            self.central_widget.text_edit.append("Datetime: " + veitzQueryToolFunctions.stringtimenow())
            with redirect_stdout_ext(self.central_widget.text_edit):
                veitzQueryToolFunctions.btcinfonow()
        except Exception as e:
            self.central_widget.text_edit.append(f"Error in running external cc(): {e}")
            #self.text_edit.append(f"Error in running external cc(): {e}")

    def usdc_info(self):
        # Aktion des Menüeintrags # aus externer Funktion
        try:
            self.central_widget.text_edit.append("Datetime: " + veitzQueryToolFunctions.stringtimenow())
            with redirect_stdout_ext(self.central_widget.text_edit):
                veitzQueryToolFunctions.usdcinfonow()
        except Exception as e:
            self.central_widget.text_edit.append(f"Error in running external cc(): {e}")
            #self.text_edit.append(f"Error in running external cc(): {e}")

    def eth_info(self):
        # Aktion des Menüeintrags # aus externer Funktion
        try:
            self.central_widget.text_edit.append("Datetime: " + veitzQueryToolFunctions.stringtimenow())
            with redirect_stdout_ext(self.central_widget.text_edit):
                veitzQueryToolFunctions.ethinfonow()
        except Exception as e:
            self.central_widget.text_edit.append(f"Error in running external cc(): {e}")
            #self.text_edit.append(f"Error in running external cc(): {e}")

    def fear_greed(self):
        # Aktion des Menüeintrags # aus externer Funktion
        try:
            self.central_widget.text_edit.append("Datetime: " + veitzQueryToolFunctions.stringtimenow())
            with redirect_stdout_ext(self.central_widget.text_edit):
                veitzQueryToolFunctions.fearandgreed()
        except Exception as e:
            self.central_widget.text_edit.append(f"Error in running external cc(): {e}")
            #self.text_edit.append(f"Error in running external cc(): {e}")

    def open_orders(self):
        # Aktion des Menüeintrags # aus interner Funktion
        try:
            self.central_widget.text_edit.append("Datetime: " + veitzQueryToolFunctions.stringtimenow())
            with redirect_stdout_int(self.central_widget.text_edit):
                self.openorder()
        except Exception as e:
            self.central_widget.text_edit.append(f"Error in running internal openorders(self): {e}")
            #self.central_widget.text_edit.append("error in openorders(self) method \n")

    def my_wallet(self):
        # Aktion des Menüeintrags # aus externer Funktion
        try:
            self.central_widget.text_edit.append("Datetime: " + veitzQueryToolFunctions.stringtimenow())
            with redirect_stdout_ext(self.central_widget.text_edit):
                veitzQueryToolFunctions.walletinfo()
        except Exception as e:
            self.central_widget.text_edit.append(f"Error: maybe in running external show_last100(): {e}")
            #self.text_edit.append(f"Error in running external cc(): {e}")

    def show_last100(self):
        # Aktion des Menüeintrags # aus externer Funktion
        try:
            self.central_widget.text_edit.append("Datetime: " + veitzQueryToolFunctions.stringtimenow())
            with redirect_stdout_ext(self.central_widget.text_edit):
                veitzQueryToolFunctions.show_last100()
        except Exception as e:
            self.central_widget.text_edit.append(f"Error: maybe in running external show_last100(): {e}")
            #self.text_edit.append(f"Error in running external cc(): {e}")






    ### RealTime Tools ###

    def get_realtime_btc_value(self):
        """Externe GUI 1 starten (BTC Info)"""
        try:
            if self.process_gui1 is None or self.process_gui1.state() == QProcess.NotRunning:
                self.process_gui1 = QProcess(self)
                self.process_gui1.finished.connect(lambda: print("BTC Info GUI onetraiding beendet"))
                self.process_gui1.start("python3", ["realTimeCacheData.py"])  
            else:
                QMessageBox.warning(self, "Warnung", "BTC Info GUI onetraiding läuft bereits!")
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Fehler beim Starten der BTC Info GUI onetraiding: {e}")

    def show_real_time_graph(self):
        """Externe GUI 2 starten (BTC Graph)"""
        try:
            if self.process_gui2 is None or self.process_gui2.state() == QProcess.NotRunning:
                self.process_gui2 = QProcess(self)
                self.process_gui2.finished.connect(lambda: print("BTC Graph GUI onetraiding beendet"))
                self.process_gui2.start("python3", ["realTimeGraph.py"])  
            else:
                QMessageBox.warning(self, "Warnung", "BTC Graph GUI ontraiding läuft bereits!")
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Fehler beim Starten der BTC Graph GUI onetraiding: {e}")



    def get_realtime_btc_value_binance(self):
        """Externe GUI binance 1 starten (BTC Info)"""
        try:
            if self.process_gui3 is None or self.process_gui3.state() == QProcess.NotRunning:
                self.process_gui3 = QProcess(self)
                self.process_gui3.finished.connect(lambda: print("BTC Info GUI binance beendet"))
                self.process_gui3.start("python3", ["realTimeCacheDataBinance.py"])  
            else:
                QMessageBox.warning(self, "Warnung", "BTC Info GUI binance läuft bereits!")
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Fehler beim Starten der BTC Info GUI binance: {e}")

    def show_real_time_graph_binance(self):
        """Externe GUI binance 2 starten (BTC Graph)"""
        try:
            if self.process_gui4 is None or self.process_gui4.state() == QProcess.NotRunning:
                self.process_gui4 = QProcess(self)
                self.process_gui4.finished.connect(lambda: print("BTC Graph GUI binance beendet"))
                self.process_gui4.start("python3", ["realTimeGraphBinance.py"])  
            else:
                QMessageBox.warning(self, "Warnung", "BTC Graph GUI binance läuft bereits!")
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Fehler beim Starten der BTC Graph GUI binance: {e}")






    ### Settings ###

    def config_info(self):
        # Aktion des Menüeintrags # aus externer .py
        try:
            with redirect_stdout_ext(self.central_widget.text_edit):
                veitzQueryToolFunctions.confcheck()
        except Exception as e:
            self.central_widget.text_edit.append(f"Error in running external cc(): {e}")
            #self.text_edit.append(f"Error in running external cc(): {e}")

    def show_config(self):
        # Aktion des Menüeintrags # aus externer .py
        try:
            with redirect_stdout_ext(self.central_widget.text_edit):
                veitzQueryToolFunctions.readconf()
        except Exception as e:
            self.central_widget.text_edit.append(f"Error in running external cc(): {e}")
            #self.text_edit.append(f"Error in running external cc(): {e}")





    ### About ###

    def data_viewer(self):
        # Aktion des Menüeintrags # aus externer .py
        try:
            with redirect_stdout_ext(self.central_widget.text_edit):
                veitzQueryToolFunctions.json_search2()
        except Exception as e:
            self.central_widget.text_edit.append(f"Error in running external cc(): {e}")
            #self.text_edit.append(f"Error in running external cc(): {e}")

    def api_info(self):
        # Aktion des Menüeintrags # aus externer .py
        try:
            with redirect_stdout_ext(self.central_widget.text_edit):
                veitzQueryToolFunctions.api_status()
        except Exception as e:
            self.central_widget.text_edit.append(f"Error in running external cc(): {e}")
            #self.text_edit.append(f"Error in running external cc(): {e}")







    ### my side Functions ####
    """
    def stringtimenow():
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y_%H:%M:%S")
        return dt_string
    """
    def openorder(self):
        """get orders ist der Bericht über offene Orders https://developers.bitpanda.com/exchange/?python#get-orders"""
        config = configparser.ConfigParser()
        config.read('CONFIG.INI')
        bpkey = str(config['DEFAULT']['apikey'])
        headers = {
            'Accept': 'application/json',
            'Authorization': bpkey
        }
        r = requests.get('https://api.onetrading.com/fast/v1/account/orders', params={
        }, headers=headers)
        print(" - Liste der offenen Orders - ")
        print(r.json())
        print("")
        print(">>>")
    ### end my side Functions ####

    ### end function for menu ###







@contextlib.contextmanager
def redirect_stdout_int(target):
    original = sys.stdout
    sys.stdout = StringIO()
    yield
    target.append(sys.stdout.getvalue())
    sys.stdout = original


@contextlib.contextmanager
def redirect_stdout_ext(target):
    original = sys.stdout
    sys.stdout = StringIO()
    try:
        yield
    finally:
        target.append(sys.stdout.getvalue())
        sys.stdout = original


def main():
    app = QApplication(sys.argv)
    #ex = MyMainWindow() #ori
    window = MyMainWindow()
    window.close()
    window.show()      # wird hier ausgeführt: def __init__(self):
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()
