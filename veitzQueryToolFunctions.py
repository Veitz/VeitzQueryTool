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



def hellowelt():
    #return "HelloWorld!"
    print("HelloWelt!")


def stringtimenow():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y_%H:%M:%S")
    return dt_string


def api_status():
    """checkt status of onetrading api and markets - NOTE: - but config.ini will be updated after runtime... well, you can place this function after json_sarch() and it will be always up to date!"""
    config = configparser.ConfigParser()
    config.read('CONFIG.INI')
    btcval = int(config['DEFAULT']['coinvalbtc'])
    ethval = int(config['DEFAULT']['coinvaleth'])

    conn = http.client.HTTPSConnection("api.onetrading.com")
    headers = {'Accept': "application/json"}
    conn.request("GET", "/fast/v1/market-ticker", headers=headers)
    res = conn.getresponse()
    print("api request status:", res.status, res.reason)

    dat = res.read()
    data = dat.decode("utf-8")
    jdata = json.loads(data)
    jsonelement = jdata[btcval]['state']
    print("market state BTC-EUR:", jsonelement, "json-value:", btcval)
    jsonelement = jdata[ethval]['state']
    print("market state ETH-EUR:", jsonelement, "json-value:", ethval, "\n")
    print("Infos: https://api.onetrading.com/fast/v1 - REST API & \n https://docs.onetrading.com/#fast-upgrade--- \n")
    print("")
    print(">>>")
#api_status()


def json_search():
    """sucht den BTC-Block in der JSON und gibt die momentan gueltige Elementnummer für den 'def btcinfonow_trigger' zurueck."""
    headers = {
        'Accept': 'application/json'
    }
    r = requests.get('https://api.onetrading.com/fast/v1/market-ticker', params={
        "instrument_code": "BTC_EUR"
    }, headers=headers)
    # j = r.json()
    #print("api request status:", r.status_code, r.reason, "\n") # status_code ist bei request und nur status bei http.client
    data = json.dumps(r.json())
    # write json to file
    with open("jsontmp.json", "w") as f:
        f.write(data)

    # set path to file
    p = Path(r'jsontmp.json')
    # read json
    with p.open('r', encoding='utf-8') as f:
        data = json.loads(f.read())
    # create dataframe
    df = pd.json_normalize(data)
    #pd.set_option('display.max_columns', None)
    #pd.set_option("display.max_rows", 200)
    #pd.set_option("display.max_columns", 100)
    #pd.set_option("display.max_colwidth", 200)
    print(df)
    # save to csv
    df.to_csv('jsontmp.csv', index=False, encoding='utf-8')
    # number of row
    # print(df[df['instrument_code'] == 'BTC_EUR'].index)
    # print(df[df['instrument_code'] == 'BTC_EUR'].index[0])
    config = configparser.ConfigParser()
    config.read('CONFIG.INI')
    config['DEFAULT']['last_access'] = str(datetime.now())  # create
    config['DEFAULT']['coinvalbtc'] = str(df[df['instrument_code'] == 'BTC_EUR'].index[0])  # create
    config['DEFAULT']['coinvaleth'] = str(df[df['instrument_code'] == 'ETH_EUR'].index[0])  # create
    with open('CONFIG.INI', 'w') as configfile:  # save
        config.write(configfile)
    # clean-up
    os.remove("jsontmp.json")
    os.remove("jsontmp.csv")
    print("")
    print(">>>")
#json_search()


def confcheck():
    config = configparser.ConfigParser()
    config.read('CONFIG.INI')
    btcval = int(config['DEFAULT']['coinvalbtc'])
    ethval = int(config['DEFAULT']['coinvaleth'])
    print('')
    print('use JSON-Value for BTC:', btcval)
    print('use JSON-Value for ETH:', ethval)
    print('configuration was updated!')
    print("")
    print(">>>")


def readconf():
    print('Variabes from configuration File - CONFIG.INI:')
    print("")
    with open('CONFIG.INI', 'r') as conf:
        for line in conf:
            print(line)
        print("")
        print(">>>")
#print(readconf())


def fearandgreed():
    """gibt den aktuellen Fear and Greed zurück"""
    r = requests.get('https://api.alternative.me/fng/')
    j = r.json()
    e = j['data']
    try:
        print("- aktueller Fear and Greed Index -")
        print("Fear&Greed-Wert vom ", datetime.now(), " liegt bei ", e[0]['value'])
    except KeyError:
        print("- aktueller Fear&Greed Value -")
        print("ERROR in API or JSON doesn't exist")
    print("")
    print(">>>")


def ethinfonow():
    """gibt den aktuellen btc marktpreis Informationen zurück."""
    config = configparser.ConfigParser()
    config.read('CONFIG.INI')
    ethval = int(config['DEFAULT']['coinvaleth'])
    headers = {
        'Accept': 'application/json'
    }
    r = requests.get('https://api.onetrading.com/fast/v1/market-ticker', params={
        "instrument_code": "ETH_EUR"
    }, headers=headers)
    j = r.json()
    #h = j[int(ethval)]['time']
    print("- aktuelle ETH Informationen -")
    print('Zeitstempel: ', str(datetime.now()))
    f = j[int(ethval)]['last_price']
    print('last_price: ', f)
    #i = j[int(ethval)]['best_bid']
    #print('best_bid  : ', i)
    #g = j[int(ethval)]['best_ask']
    #print('best_ask  : ', g)
    n = j[int(ethval)]['high']
    print('high 24h  : ', n)
    m = j[int(ethval)]['low']
    print('low 24h   : ', m)
    print("")
    print(">>>")


def btcinfonow():
    """gibt den aktuellen btc marktpreis Informationen zurück."""
    config = configparser.ConfigParser()
    config.read('CONFIG.INI')
    btcval = int(config['DEFAULT']['coinvalbtc'])
    headers = {
        'Accept': 'application/json'
    }
    r = requests.get('https://api.onetrading.com/fast/v1/market-ticker', params={
        "instrument_code": "BTC_EUR"
    }, headers=headers)
    j = r.json()
    #print(j)
    #h = j[int(btcval)]['time']
    print("- aktuelle BTC Informationen -")
    print('Zeitstempel: ', str(datetime.now()))
    f = j[int(btcval)]['last_price']
    print('last_price: ', f)
    #i = j[int(btcval)]['best_bid']
    #print('best_bid  : ', i)
    #g = j[int(btcval)]['best_ask']
    #print('best_ask  : ', g)
    n = j[int(btcval)]['high']
    print('high 24h  : ', n)
    m = j[int(btcval)]['low']
    print('low 24h   : ', m)
    print("")
    print(">>>")