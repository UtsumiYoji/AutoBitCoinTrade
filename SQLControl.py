import sqlite3

class SQLControl():
    #コンストラクト
    def __init__(self):
        self.conn = sqlite3.connect('BtcData.db', isolation_level=None)
        self.cur = self.conn.cursor()

    #買った注文を記録するテーブル
    def MakeBuyTable(self):
        self.cur.execute(
            'create table BuyBtc(\
                id integer primary key autoincrement,\
                size real,\
                price real,\
                date string,\
                state string)'
        )

    #デストラクト
    def __del__(self):
        self.cur.close()
        self.conn.close()

    #買った時の情報を記録しておく
    def RegBuyData(self, size, price, date):
        self.cur.execute(
            "insert into BuyBtc(size, price, state, date) values('"+\
            str(size) + "','" + str(price) + "','未完了','" + date + "')"
        )

    #売った事を記録する
    def UpdateData(self, IdNum):
        self.cur.execute(
            "update BuyBtc set state='完了' where id='" + str(IdNum) + "'"
        )

    #ステータスが未完了のデータだけを抽出する
    def ReadIncomplete(self):
        self.cur.execute(
            'select * from BuyBtc where state = "未完了"'
        )
        return self.cur.fetchall()
