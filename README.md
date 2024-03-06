
# VeitzQueryTool    

This tool is a GUI to use the ontrading.com exchange. Create a personal API key on the trading platform, enter the key in the config file and you can trade using the tool.
   
## VeitzQueryTool is a Querytool for the crypto Exchange onetrading.com

Linklist:   
Ontrading.com doc: *https://docs.onetrading.com/*  
API DOC: *https://api.onetrading.com/fast/v1*   
REST API: *https://docs.onetrading.com/#fast-upgrade---*   
.MD-File Syntax: *http://markdown-syntax.de/Syntax/Zeilenumbrueche/* 




### StoppLoss:
`StopLoss will be calculated on based BTC-Value.`

new Functions:  
`set_StopLoss (set a stopLoss order),   
delete_openOrders (closed all open orders),  
buy Order (takes the entire value),  
sell Order (takes the entire value)`  
Bei Änderung der JSON (duch BitPanda) muss die Variable "btcnow = j[2]['best_bid']" 
in der Methode "def buy_trigger(self):" angepasst werden (alle JSON kontrollieren)!

### Requirements:
sudo apt update && upgrade   
sudo apt install python3-pyqt5   
sudo apt install python3-tk   
pip3 install --upgrade pip   
pip3 install pyqt5
pip3 install requests   
pip3 install datetime   
pip3 install configparser    
pip3 install easygui   
pip3 install pandas   
pip3 install pathlib   
pip3 install path   
pip3 install pyfiglet
