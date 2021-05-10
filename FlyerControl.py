import configparser
import pybitflyer

class FlyerControl():
    #コンストラクト
    def __init__(self):
        #configparserのインスタス
        config_ini = configparser.ConfigParser()
        config_ini.read('setting.ini', encoding='utf-8')

        #設定ファイルからAPIキーとシークレットキーを取得
        api = config_ini['bitflyer']['api']
        secret = config_ini['bitflyer']['secret']

        #bitflyerオブジェクトの生成
        self.API = pybitflyer.API(api, secret)

    #今のbitcoinの値段を教えてくれる
    def BtcPrice(self):
        return self.API.ticker(product_code='BTC_JPY')['ltp']

    #現在の手数料を取得
    def BtcCommission(self):
        return self.API.gettradingcommission(product_code='BTC_JPY')['commission_rate']

    #日本円残高を取得
    def Balance(self):
        result = self.API.getbalance()[0]['amount']
        return int(result)
    
    #Btc残高を取得
    def BtcBalance(self):
        result = self.API.getbalance()[1]['amount']
        return result

    #BTC成行買い
    def BuyBtc(self, amt):
        result = self.API.sendchildorder(product_code='BTC_JPY',\
                                child_order_type='MARKET',\
                                side='BUY',\
                                size=amt,\
                                minute_to_expire=10,\
                                time_in_force='GTC')
        return result
    
    #BTC成行売り
    def SellBtc(self, amt):
        result = self.API.sendchildorder(product_code='BTC_JPY',\
                                child_order_type='MARKET',\
                                side='SELL',\
                                size=amt,\
                                minute_to_expire=10,\
                                time_in_force='GTC')
        return result
