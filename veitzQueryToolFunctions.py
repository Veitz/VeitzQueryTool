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
import pprint

def hello():
    print("HelloWorld!")

def orderbook_btc_snap_ask():
    conn = http.client.HTTPSConnection("api.onetrading.com")
    headers = {'Accept': "application/json"}
    conn.request("GET", "/fast/v1/order-book/BTC_USDC", headers=headers)
    res = conn.getresponse()

    dat = res.read()
    data = dat.decode("utf-8")
    jdata = json.loads(data)
    jsonask = jdata['asks'][0]['price']
    return jsonask


def orderbook_btc_snap_bid():
    conn = http.client.HTTPSConnection("api.onetrading.com")
    headers = {'Accept': "application/json"}
    conn.request("GET", "/fast/v1/order-book/BTC_USDC", headers=headers)
    res = conn.getresponse()

    dat = res.read()
    data = dat.decode("utf-8")
    jdata = json.loads(data)
    jsonbid = jdata['bids'][0]['price']
    return jsonbid



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
    usdcval = int(config['DEFAULT']['coinvalusdc'])

    conn = http.client.HTTPSConnection("api.onetrading.com")
    headers = {'Accept': "application/json"}
    conn.request("GET", "/fast/v1/market-ticker", headers=headers)
    res = conn.getresponse()
    print("api request status:", res.status, res.reason)

    dat = res.read()
    data = dat.decode("utf-8")
    jdata = json.loads(data)
    try:
        jsonelement = jdata[btcval]['state']
        print("market state BTC-usdc:", jsonelement) #, "json-value:", ethval, "\n")
    except Exception as e:
        print("market state BTC-usdc:", type(e), e)
    try:
        jsonelement = jdata[usdcval]['state']
        print("market state USDC-euro:", jsonelement) #, "json-value:", ethval, "\n")
    except Exception as e:
        print("market state USDC-euro:", type(e), e)
    try:
        jsonelement = jdata[ethval]['state']
        print("market state ETH-usdc:", jsonelement, "\n") #, "json-value:", ethval, "\n")
    except Exception as e:
        print("market state ETH-usdc:", type(e), e)
    print("")
    print(">>>")


def json_search():
    """sucht den BTC-Block in der JSON und gibt die momentan gueltige Elementnummer für den 'def btcinfonow_trigger' zurueck."""
    headers = {
        'Accept': 'application/json'
    }
    r = requests.get('https://api.onetrading.com/fast/v1/market-ticker', params={
        "instrument_code": "BTC_USDC"
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
    pd.set_option('display.max_columns', None)
    #pd.set_option("display.max_rows", 200)
    #pd.set_option("display.max_columns", 100)
    #pd.set_option("display.max_colwidth", 200)
    print(df)
    #pprint.pprint(data)
    # save to csv
    df.to_csv('jsontmp.csv', index=False, encoding='utf-8')
    # number of row
    # print(df[df['instrument_code'] == 'BTC_USDC'].index)
    # print(df[df['instrument_code'] == 'BTC_USDC'].index[0])
    config = configparser.ConfigParser()
    config.read('CONFIG.INI')
    config['DEFAULT']['last_access'] = str(datetime.now())  # create
    config['DEFAULT']['coinvalbtc'] = str(df[df['instrument_code'] == 'BTC_USDC'].index[0])  # create
    config['DEFAULT']['coinvaleth'] = str(df[df['instrument_code'] == 'ETH_USDC'].index[0])  # create
    config['DEFAULT']['coinvalusdc'] = str(df[df['instrument_code'] == 'USDC_EUR'].index[0])  # create
    with open('CONFIG.INI', 'w') as configfile:  # save
        config.write(configfile)
    # clean-up
    os.remove("jsontmp.json")
    os.remove("jsontmp.csv")
    print("")
    print(">>>")
json_search()


def json_search2():
    """Output of all value pairs and their information."""
    headers = {
        'Accept': 'application/json'
    }
    r = requests.get('https://api.onetrading.com/fast/v1/market-ticker', params={
        "instrument_code": "BTC_USDC"
    }, headers=headers)
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
    pprint.pprint(data)
     # clean-up
    os.remove("jsontmp.json")
    print("")
    print(">>>")


def confcheck():
    config = configparser.ConfigParser()
    config.read('CONFIG.INI')
    btcval = int(config['DEFAULT']['coinvalbtc'])
    ethval = int(config['DEFAULT']['coinvaleth'])
    usdcval = int(config['DEFAULT']['coinvalusdc'])
    print('')
    print('use JSON-Value for BTC:', btcval)
    print('use JSON-Value for ETH:', ethval)
    print('use JSON-Value for USDC:', usdcval)
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
    """returns the current market price information."""
    config = configparser.ConfigParser()
    config.read('CONFIG.INI')
    ethval = int(config['DEFAULT']['coinvaleth'])
    headers = {
        'Accept': 'application/json'
    }
    r = requests.get('https://api.onetrading.com/fast/v1/market-ticker', params={
        "instrument_code": "ETH_USDC"
    }, headers=headers)
    j = r.json()
    #h = j[int(ethval)]['time']
    print("- aktuelle ETH_usdc Informationen in $ -")
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

def usdcinfonow():
    """returns the current market price information."""
    config = configparser.ConfigParser()
    config.read('CONFIG.INI')
    usdcval = int(config['DEFAULT']['coinvalusdc'])
    headers = {
        'Accept': 'application/json'
    }
    r = requests.get('https://api.onetrading.com/fast/v1/market-ticker', params={
        "instrument_code": "USDC_EUR"
    }, headers=headers)
    j = r.json()
    # h = j[int(usdcval)]['time']
    print("- aktuelle USDC_eur Informationen in € -")
    print('Zeitstempel: ', str(datetime.now()))
    f = j[int(usdcval)]['last_price']
    print('last_price: ', f)
    # i = j[int(usdcval)]['best_bid']
    # print('best_bid  : ', i)
    # g = j[int(usdcval)]['best_ask']
    # print('best_ask  : ', g)
    n = j[int(usdcval)]['high']
    print('high 24h  : ', n)
    m = j[int(usdcval)]['low']
    print('low 24h   : ', m)
    print("")
    print(">>>")


def btcinfonow():
    """returns the current btc market price information."""
    config = configparser.ConfigParser()
    config.read('CONFIG.INI')
    btcval = int(config['DEFAULT']['coinvalbtc'])
    headers = {
        'Accept': 'application/json'
    }
    r = requests.get('https://api.onetrading.com/fast/v1/market-ticker', params={
        "instrument_code": "BTC_USDC"
    }, headers=headers)
    j = r.json()
    #print(j)
    #h = j[int(btcval)]['time']
    print("- aktuelle BTC_usdc Informationen in $ -")
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
    btc_book_ask = orderbook_btc_snap_ask()
    btc_book_sell = orderbook_btc_snap_bid()
    spreadbook =  float(btc_book_ask) - float(btc_book_sell)
    print('orderbook buy: ', btc_book_ask)
    print('orderbook sell: ', btc_book_sell)
    print('spread: ', round(spreadbook,2))
    print("")
    print(">>>")


def show_last100():
    """show last 100 trades"""
    config = configparser.ConfigParser()
    config.read('CONFIG.INI')
    bpkey = str(config['DEFAULT']['apikey'])
    headers = {
        'Accept': 'application/json',
        'Authorization': bpkey
    }
    r = requests.get('https://api.onetrading.com/fast/v1/account/trades', params={
    }, headers=headers)
    print("- Liste der letzten 100 Trades -")
    print(r.json())
    data = json.dumps(r.json())
    # write json to file
    with open("tmp.json", "w") as f:
        f.write(data)
    # open json in browser
    filename = "tmp.json"
    webbrowser.open('file://' + os.path.realpath(filename))
    print("")
    sleep(3)
    os.remove("tmp.json")
    print("cleaning up tempfiles done!")
    print("")
    print(">>>")


def walletinfo():
    """get wallet-balance"""
    def btcBestBid():
        """returns the current btc market price. is required for the calculation of the btc amount in the fiat wallet"""
        headers = {
            'Accept': 'application/json'
        }
        r = requests.get('https://api.onetrading.com/fast/v1/market-ticker', params={
            "instrument_code": "BTC_USDC"
        }, headers=headers)
        j = r.json()
        config = configparser.ConfigParser()
        config.read('CONFIG.INI')
        btcval = int(config['DEFAULT']['coinvalbtc'])
        return j[int(btcval)]['last_price']               # best bid btc, for wallet-calculation

    def ethBestBid():
        """returns the current eth market price. is required for the calculation of the btc amount in the fiat wallet"""
        headers = {
            'Accept': 'application/json'
        }
        r = requests.get('https://api.onetrading.com/fast/v1/market-ticker', params={
            "instrument_code": "ETH_USDC"
        }, headers=headers)
        j = r.json()
        config = configparser.ConfigParser()
        config.read('CONFIG.INI')
        ethval = int(config['DEFAULT']['coinvaleth'])
        return j[int(ethval)]['last_price']               # best bid eth, for wallet-calculation

    def usdcBestBid():
        """returns the current usdc market price. is required for the calculation of the btc amount in the fiat wallet"""
        headers = {
            'Accept': 'application/json'
        }
        r = requests.get('https://api.onetrading.com/fast/v1/market-ticker', params={
            "instrument_code": "USDC_EUR"
        }, headers=headers)
        j = r.json()
        config = configparser.ConfigParser()
        config.read('CONFIG.INI')
        usdcval = int(config['DEFAULT']['coinvalusdc'])
        return j[int(usdcval)]['last_price']  # best bid usdc, for wallet-calculation

    config = configparser.ConfigParser()
    config.read('CONFIG.INI')
    bpkey = str(config['DEFAULT']['apikey'])
    headers = {
        'Accept': 'application/json',
        'Authorization': bpkey
    }
    r = requests.get('https://api.onetrading.com/fast/v1/account/balances', params={
    }, headers=headers)
    # print(r.json())
    j = r.json()
    e = j['balances']
    #print(e)
    #print(btcBestBid())
    #print(ethBestBid())
    try:
        print("- aktuelle Werte der Wallet's -")
        print("currency_code: ", e[0]['currency_code'])  # fiat, muss auch in sell_trigger() angepasst werden!!         # euro
        print("available:     ", e[0]['available'], " sind ", float(e[0]['available']) / float(btcBestBid()), "btc")  # euro
        print("currency_code: ", e[4]['currency_code'])  # btc muss auch in buy_trigger() angepasst werden !!           # btc
        print("available:     ", e[4]['available'], " sind ", float(btcBestBid()) * float(e[4]['available']), "€")  # btc
        print("currency_code: ", e[1]['currency_code'])  # eth
        print("available:     ", e[1]['available'])  # eth
        print("currency_code: ", e[3]['currency_code'])  # usdc
        print("available:     ", e[3]['available'], " sind ", float(usdcBestBid()) * float(e[3]['available']), "€")  # usdc
        # print("currency_code: ", e[4]['currency_code'])
        # print("available:     ", e[4]['available'])
        # print('HINWEIS: Currencies mit gesetztem Stop-Loss sind LOCKED und werden daher nicht angezeigt!')
    except KeyError:
        print("ERROR: in api_getbalance.py or JSON doesn't exist")
    print("")
    print(">>>")


def changelog():
    with open('changelog.md', 'r') as info:
        for line in info:
            print(line)
        print("")
        print(">>>")


def get_version():
    config = configparser.ConfigParser()
    config.read('CONFIG.INI')
    vnr = str(config['VERSION']['versionnum'])
    return vnr


def sell_trigger():
    def btcnow():
        """returns the current btc market price. is required for the calculation of the btc amount in the fiat wallet"""
        config = configparser.ConfigParser()
        config.read('CONFIG.INI')
        btcval = int(config['DEFAULT']['coinvalbtc'])
        bpkey = str(config['DEFAULT']['apikey'])
        headers = {
            'Accept': 'application/json',
            'Authorization': bpkey
        }
        r = requests.get('https://api.onetrading.com/fast/v1/market-ticker', params={
            "instrument_code": "BTC_USDC"
        }, headers=headers)
        j = r.json()
        btcnow = j[int(btcval)]['last_price']             # best bid btc
        #print('BTC Value now : ', btcnow, '€')
        return btcnow

    def orderbook_snap_bid():
        conn = http.client.HTTPSConnection("api.onetrading.com")
        headers = {'Accept': "application/json"}
        conn.request("GET", "/fast/v1/order-book/BTC_USDC", headers=headers)
        res = conn.getresponse()

        dat = res.read()
        data = dat.decode("utf-8")
        jdata = json.loads(data)
        jsonbid = jdata['bids'][0]['price']
        return jsonbid

    print(" - BTC INFOS CURRENTLY - ")
    print("btc price: ", btcnow(), "€")
    print("order-book price: ", orderbook_snap_bid(), "€")
    print(" - ASK Order - ")
    """gibt den btc amount des wallets wieder, wird zum verkauf benötigt"""
    config = configparser.ConfigParser()
    config.read('CONFIG.INI')
    bpkey = str(config['DEFAULT']['apikey'])
    headers = {
        'Accept': 'application/json',
        'Authorization': bpkey
    }
    r = requests.get('https://api.onetrading.com/fast/v1/account/balances', params={
    }, headers=headers)
    # print(r.json())
    j = r.json()
    e = j['balances']
    a = e[1]['available']
    b = float(a)
    av = "%.5f" % (b - b % 0.00001)
    print("your absolute Value: ", a)
    print("sell amount of BTC wallet: ", av)
    """post ask order on marketprice"""
    config = configparser.ConfigParser()
    config.read('CONFIG.INI')
    bpkey = str(config['DEFAULT']['apikey'])
    headers = {
        'Accept': 'application/json',
        'Authorization': bpkey
    }
    r = requests.post('https://api.onetrading.com/fast/v1/account/orders',
                      json={"instrument_code": "BTC_USDC","type": "LIMIT" , "side": "SELL", "amount": str(av), "price": str(orderbook_snap_bid()), "time_in_force": "IMMEDIATE_OR_CANCELLED"},             # , "time_in_force": "GOOD_TILL_CANCELLED"
                      headers=headers)
    print("used order-book price: ", orderbook_snap_bid(), "€")
    print(" - carry out / err msg - ")
    print(r.json())
    data = json.dumps(r.json())
    with open("_selllog.json", "a") as f:
        f.write(stringtimenow() + " - " + data + '\r\n')
        #f.write(data + '\r\n')
    print("")
    print(">>>")
    #print(1 * 40000 / 100)  # 1% von 40000




def buy_trigger():
    def btcnow():
        """returns the current btc market price. is required for the calculation of the btc amount in the fiat wallet"""
        config = configparser.ConfigParser()
        config.read('CONFIG.INI')
        btcval = int(config['DEFAULT']['coinvalbtc'])
        bpkey = str(config['DEFAULT']['apikey'])
        headers = {
            'Accept': 'application/json',
            'Authorization': bpkey
        }
        r = requests.get('https://api.onetrading.com/fast/v1/market-ticker', params={
            "instrument_code": "BTC_USDC"
        }, headers=headers)
        j = r.json()
        btcnow = j[int(btcval)]['last_price']             # best bid btc
        #print('BTC Value now : ', btcnow, '€')
        return btcnow

    def orderbook_snap_ask():
        conn = http.client.HTTPSConnection("api.onetrading.com")
        headers = {'Accept': "application/json"}
        conn.request("GET", "/fast/v1/order-book/BTC_USDC", headers=headers)
        res = conn.getresponse()

        dat = res.read()
        data = dat.decode("utf-8")
        jdata = json.loads(data)
        jsonask = jdata['asks'][0]['price']
        return jsonask

    print(" - BTC INFOS CURRENTLY - ")
    print("btc price: ", btcnow(), "€")
    print("order-book price: ", orderbook_snap_ask(), "€")
    print(" - BID Order - ")
    print('BTC Value now : ', btcnow(), '€')
    # print("order-book price: ", orderbook_snap_ask(), "€")    # is displayed at the bottom of the order-book-price used
    """gibt die FIAT Wallet-Balance aus"""
    config = configparser.ConfigParser()
    config.read('CONFIG.INI')
    bpkey = str(config['DEFAULT']['apikey'])
    headers = {
        'Accept': 'application/json',
        'Authorization': bpkey
    }
    r = requests.get('https://api.onetrading.com/fast/v1/account/balances', params={
    }, headers=headers)
    # print(r.json())
    j = r.json()
    e = j['balances']
    try:
        fiatval2 = e[0]['available']
        #fiatval3 = round(float(fiatval2), 2)
        print('my Fiatwallet amount : ', fiatval2, '€')
    except KeyError:
        print("ERROR: in api_getbalance.py or JSON doesn't exist")
    bbv = floor(float(fiatval2)) / float(orderbook_snap_ask())  # Original calculation from btcnow()
    bbvr = round(bbv, 5) - float(0.001)
    print('your BTC buy amount:', bbvr)
    ### buy BTC at Limitprice ###
    config = configparser.ConfigParser()
    config.read('CONFIG.INI')
    bpkey = str(config['DEFAULT']['apikey'])
    headers = {
        'Accept': 'application/json',
        'Authorization': bpkey
    }
    r = requests.post('https://api.onetrading.com/fast/v1/account/orders',
                      json={"instrument_code": "BTC_USDC", "type": "LIMIT", "side": "BUY", "amount": str(bbvr), "price": str(orderbook_snap_ask()), "time_in_force": "IMMEDIATE_OR_CANCELLED"},  # , "time_in_force": "GOOD_TILL_CANCELLED"
                      headers=headers)
    print("used order-book price: ", orderbook_snap_ask(), "€")
    print(" - carry out / err msg - ")
    print(r.json())
    data = json.dumps(r.json())
    with open("_buylog.json", "a") as f:
        f.write(stringtimenow() + " - " + data + '\r\n')
        #f.write(data + '\r\n')
    print("")
    print(">>>")