import FlyerControl
import SQLControl

import configparser
import numpy as np

import datetime
import sys
import time

class MainControl:
    def __init__(self):
        #configparserのインスタス
        config_ini = configparser.ConfigParser()
        config_ini.read('setting.ini', encoding='utf-8')

        #BTCが平均よりどんくらい低いかとどんくらい買うか
        self.DownPercentage = float(config_ini['parameter']['DownPercentage'])
        self.UpPercentage = float(config_ini['parameter']['UpPercentage'])
        self.TradeSize = float(config_ini['parameter']['TradeSize'])
        self.ChartPeriod = (int(config_ini['parameter']['ChartPeriod'])*60) + 1
        self.BuyPeriod = float(config_ini['parameter']['BuyPeriod']) * 3600

    def main(self):
        #インスタンスを生成
        FlyerInstance = FlyerControl.FlyerControl()
        SQLInstance = SQLControl.SQLControl()
        ChartData = []

        #チャートを格納する変数を定義

        while True:
            #今回のループが始まった時間を記録
            StartTime = datetime.datetime.now()

            #今のBTCの価格を取得
            BtcPrice = FlyerInstance.BtcPrice()
            #データをチャートの末尾に追加
            ChartData.append(BtcPrice)

            #買い注文で未完了のデータを全て取得
            IncompData = SQLInstance.ReadIncomplete()

            #買い注文データない場合は適当に最後の取引の日付を作る
            if len(IncompData) == 0:
                LastDate = '2021-4-24 12:00:00'
            else:
                LastDate = IncompData[-1][3]

            #チャート内のデータが十分な時
            if len(ChartData) == self.ChartPeriod:
                del ChartData[0] #一番古いデータを削除
                ChartAverage = np.mean(np.array(ChartData)) #ここ2時間の価格平均

                #今の値段が平均より指定%低いか考える
                if BtcPrice < (ChartAverage*self.DownPercentage):
                    #自分の残金敵にBTCがそもそも買えるのか考える
                    if FlyerInstance.Balance() > (self.TradeSize*BtcPrice):
                        #買い注文の最後から指定時間以上離れているか考える
                        LastOrderTime = datetime.datetime.strptime(LastDate, '%Y-%m-%d %H:%M:%S')
                        if (StartTime - LastOrderTime).total_seconds() > self.BuyPeriod:
                        
                            #購入処理を行う
                            FlyerInstance.BuyBtc(self.TradeSize)
                            #買った時の情報をDBに登録
                            SQLInstance.RegBuyData(self.TradeSize, BtcPrice, StartTime.strftime('%Y-%m-%d %H:%M:%S'))
                            print('買いました')
            
            #売却処理
            if not len(IncompData) == 0:
                for i in range(len(IncompData)):
                    #現在の価格が購入時より指定%高い場合
                    if BtcPrice > (IncompData[i][2]*self.UpPercentage):
                        #売る処理
                        FlyerInstance.SellBtc(IncompData[i][1])
                        #ステータスを更新する処理
                        SQLInstance.UpdateData(IncompData[i][0])
                        print('売りました')

            #1分待機
            WaitTime = 60 - (datetime.datetime.now() - StartTime).total_seconds()
            time.sleep(int(WaitTime))

if __name__ == '__main__':
    MainControl().main()