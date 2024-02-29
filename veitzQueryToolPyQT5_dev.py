import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QMainWindow, QAction, QMenu, QMessageBox
from datetime import datetime
import easygui
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
import pyfiglet

from tkinter import *
import tkinter
import tkinter.messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter import font

import veitzQueryToolFunctions
from veitzQueryToolFunctions import api_status, json_search, confcheck, stringtimenow
from io import StringIO
import contextlib





class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.text_edit = QTextEdit(self)
        #self.text_edit.setStyleSheet("background-color: black; color: white;")  # Stiländerungen hier
        layout.addWidget(self.text_edit)

        ascii_banner = pyfiglet.figlet_format("VeitzQueryTool")     # in der Console
        print(ascii_banner)
        self.text_edit.append("pending... ")
        self.text_edit.append("")
        self.text_edit.append(">>>")

        button1 = QPushButton('button1 -> buy Bitcoin', self)
        button1.clicked.connect(self.button1Clicked)
        layout.addWidget(button1)

        button2 = QPushButton('button2 <- sell Bitcoin', self)
        button2.clicked.connect(self.button2Clicked)
        layout.addWidget(button2)

        self.setLayout(layout)

    def button1Clicked(self):
        try:
            self.text_edit.append("Datetime: " + stringtimenow())
            self.text_edit.append("du hast button1 gedrückt (buy) \n")
        except:
            self.text_edit.append("error in button1 buy-method")

    def button2Clicked(self):
        try:
            self.text_edit.append("Datetime: " + stringtimenow())
            self.text_edit.append("einen kleinen Moment bitte ... das war button2 (sell) \n")
        except:
            self.text_edit.append("error in button2 sell-method")




class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = MyWidget()
        self.setCentralWidget(self.central_widget)

        self.initMenu()

        self.setGeometry(500, 300, 864, 480)
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



        fileMenu = menubar.addMenu('Settings')
        configinfoAction = QAction('config Info/Update', self)
        configinfoAction.triggered.connect(self.config_info)  # Hier wird die Methode test aufgerufen
        fileMenu.addAction(configinfoAction)
        showconfigAction = QAction('show config.ini', self)
        showconfigAction.triggered.connect(self.show_config)  # Hier wird die Methode test aufgerufen
        fileMenu.addAction(showconfigAction)



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
        openordersAction = QAction('show open Orders', self)
        openordersAction.triggered.connect(self.open_orders)
        fileMenu.addAction(openordersAction)



        infoMenu = menubar.addMenu('Info')
        infoAction = QAction('About', self)
        infoAction.triggered.connect(self.showInfo)
        infoMenu.addAction(infoAction)

        # ... Weitere Menüpunkte ...





    ### function for menu ###

    def showInfo(self):
        QMessageBox.information(self, 'Information', 'veitzQueryToolPyQT5 - v2.0-dev\n'
                                        'Changelog:\n \n'
                                        '- pyQT5 release_version \n')









    def btc_info(self):
        # Aktion des Menüeintrags # aus interner Funktion
        try:
            self.central_widget.text_edit.append("Datetime: " + stringtimenow())
            with redirect_stdout_ext(self.central_widget.text_edit):
                veitzQueryToolFunctions.btcinfonow()
        except Exception as e:
            self.central_widget.text_edit.append(f"Error in running external cc(): {e}")
            #self.text_edit.append(f"Error in running external cc(): {e}")

    def eth_info(self):
        # Aktion des Menüeintrags # aus interner Funktion
        try:
            self.central_widget.text_edit.append("Datetime: " + stringtimenow())
            with redirect_stdout_ext(self.central_widget.text_edit):
                veitzQueryToolFunctions.ethinfonow()
        except Exception as e:
            self.central_widget.text_edit.append(f"Error in running external cc(): {e}")
            #self.text_edit.append(f"Error in running external cc(): {e}")

    def fear_greed(self):
        # Aktion des Menüeintrags # aus interner Funktion
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
            self.central_widget.text_edit.append(f"Error in running external cc(): {e}")
            #self.central_widget.text_edit.append("error in openorders(self) method \n")






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
                veitzQueryToolFunctions.json_search()
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
    window.show()      # wird hier ausgeführt: def __init__(self):
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()