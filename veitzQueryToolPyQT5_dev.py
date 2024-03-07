import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QTextEdit, QMainWindow, QAction, QLabel, QMenu, QMessageBox, QGridLayout
import pyfiglet
from datetime import datetime
import json
import os
import webbrowser
from time import sleep
import requests
import configparser
from math import floor      # Funktion zum Abrunden von float
import pandas as pd
from pathlib import Path
import http.client          # only for delete_stopp_loss_order or closing all orders atm
import veitzQueryToolFunctions
from veitzQueryToolFunctions import api_status, json_search, confcheck, stringtimenow
from io import StringIO
import contextlib
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
#from data_loader import get_version




class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Pyfiglet-Text als QLabel anzeigen
        figlet_text = pyfiglet.figlet_format("          VeitzQueryTool")
        figlet_label = QLabel(figlet_text, self)
        figlet_label.setStyleSheet("font-family: monospace; font-size: 15px; text-align: center;")
        layout.addWidget(figlet_label)

        # hier Text_Edit
        self.text_edit = QTextEdit(self)
        #self.text_edit.setStyleSheet("background-color: black; color: white;")  # Stiländerungen hier
        layout.addWidget(self.text_edit)

        #ascii_banner = pyfiglet.figlet_format("VeitzQueryTool")     # in der Console
        #print(ascii_banner)

        # Starteintrag
        try:
            self.text_edit.append("Datetime: " + stringtimenow() + "\n")
            with redirect_stdout_ext(self.text_edit):
                veitzQueryToolFunctions.json_search()
        except Exception as e:
            self.text_edit.append(f"Error at startup: {e}")

        grid_layout = QGridLayout()

        button1 = QPushButton('-> buy Bitcoin', self)
        button1.setStyleSheet("background-color: #bfe5ad;")
        button1.clicked.connect(self.button_btc_buy)
        grid_layout.addWidget(button1, 0, 0)

        button2 = QPushButton('<- sell Bitcoin', self)
        button2.setStyleSheet("background-color: #f09292;")
        button2.clicked.connect(self.button_btc_sell)
        grid_layout.addWidget(button2, 0, 1)
        """
        button3 = QPushButton('-> buy Ethereum', self)
        button3.setStyleSheet("background-color: #bfe5ad;")
        button3.clicked.connect(self.button3Clicked)
        grid_layout.addWidget(button3, 1, 0)

        button4 = QPushButton('<- sell Ethereum', self)
        button4.setStyleSheet("background-color: #f09292;")
        button4.clicked.connect(self.button4Clicked)
        grid_layout.addWidget(button4, 1, 1)
        """
        # Exit Button hinzugefügt
        exitbutton = QPushButton('Exit', self)
        exitbutton.setStyleSheet("background-color: #f0f0f0; color: #333333; border: 1px solid #cccccc;")
        exitbutton.clicked.connect(self.buttonExitClicked)
        layout.addWidget(exitbutton)

        layout.addLayout(grid_layout)
        self.setLayout(layout)



    def button_btc_buy(self):
        try:
            self.text_edit.append("- buy BTC trigger - Datetime: " + stringtimenow())
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
            self.text_edit.append("- sell BTC trigger - Datetime: " + stringtimenow())
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



    def button3Clicked(self):
        QMessageBox.information(self, 'Information', 'buy Ethereum action\n \n'
                                                     'in development...')

    def button4Clicked(self):
        QMessageBox.information(self, 'Information', 'sell Ethereum action\n \n'
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

        self.initMenu()

        self.setGeometry(500, 300, 850, 768) # def setGeometry (x, y, w, h)   # https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QWidget.html
        self.setWindowTitle(" veitzQueryTool :: GUI :: QT5 ")

        app_icon = QIcon("icon.png")
        self.setWindowIcon(app_icon)

        self.show()

    def initMenu(self):
        menubar = self.menuBar()

        fileMenu = menubar.addMenu('File')
        dataviewerAction = QAction('Data Viewer', self)
        dataviewerAction.triggered.connect(self.data_viewer)  # Hier wird die Methode test aufgerufen
        fileMenu.addAction(dataviewerAction)
        apiinfoAction = QAction('api Info', self)
        apiinfoAction.triggered.connect(self.api_info)
        fileMenu.addAction(apiinfoAction)

        ## Abstandsbalken im Menü vor "Exit" einfügen
        #spacerMenu = QMenu('', self)
        #spacerAct = QAction('', self)
        #spacerAct.setDisabled(True)
        #spacerAct.setVisible(False)  # Sichtbarkeit auf False setzen
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



        fileMenu = menubar.addMenu('Settings')
        configinfoAction = QAction('config Info/Update', self)
        configinfoAction.triggered.connect(self.config_info)  # Hier wird die Methode test aufgerufen
        fileMenu.addAction(configinfoAction)
        showconfigAction = QAction('show config.ini', self)
        showconfigAction.triggered.connect(self.show_config)  # Hier wird die Methode test aufgerufen
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
            self.central_widget.text_edit.append("Datetime: " + stringtimenow())
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
            self.central_widget.text_edit.append("Datetime: " + stringtimenow())
            with redirect_stdout_ext(self.central_widget.text_edit):
                veitzQueryToolFunctions.btcinfonow()
        except Exception as e:
            self.central_widget.text_edit.append(f"Error in running external cc(): {e}")
            #self.text_edit.append(f"Error in running external cc(): {e}")

    def eth_info(self):
        # Aktion des Menüeintrags # aus externer Funktion
        try:
            self.central_widget.text_edit.append("Datetime: " + stringtimenow())
            with redirect_stdout_ext(self.central_widget.text_edit):
                veitzQueryToolFunctions.ethinfonow()
        except Exception as e:
            self.central_widget.text_edit.append(f"Error in running external cc(): {e}")
            #self.text_edit.append(f"Error in running external cc(): {e}")

    def fear_greed(self):
        # Aktion des Menüeintrags # aus externer Funktion
        try:
            self.central_widget.text_edit.append("Datetime: " + stringtimenow())
            with redirect_stdout_ext(self.central_widget.text_edit):
                veitzQueryToolFunctions.fearandgreed()
        except Exception as e:
            self.central_widget.text_edit.append(f"Error in running external cc(): {e}")
            #self.text_edit.append(f"Error in running external cc(): {e}")

    def open_orders(self):
        # Aktion des Menüeintrags # aus interner Funktion
        try:
            self.central_widget.text_edit.append("Datetime: " + stringtimenow())
            with redirect_stdout_int(self.central_widget.text_edit):
                self.openorder()
        except:
            #self.central_widget.text_edit.append(f"Error in running external cc(): {e}")
            self.central_widget.text_edit.append("error in openorders(self) method \n")

    def my_wallet(self):
        # Aktion des Menüeintrags # aus externer Funktion
        try:
            self.central_widget.text_edit.append("Datetime: " + stringtimenow())
            with redirect_stdout_ext(self.central_widget.text_edit):
                veitzQueryToolFunctions.walletinfo()
        except Exception as e:
            self.central_widget.text_edit.append(f"Error: maybe in running external show_last100(): {e}")
            #self.text_edit.append(f"Error in running external cc(): {e}")

    def show_last100(self):
        # Aktion des Menüeintrags # aus externer Funktion
        try:
            self.central_widget.text_edit.append("Datetime: " + stringtimenow())
            with redirect_stdout_ext(self.central_widget.text_edit):
                veitzQueryToolFunctions.show_last100()
        except Exception as e:
            self.central_widget.text_edit.append(f"Error: maybe in running external show_last100(): {e}")
            #self.text_edit.append(f"Error in running external cc(): {e}")





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