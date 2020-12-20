import pandas as pd
import sys
import datetime

### 商品クラス
class Item:
    def __init__(self,code,name,price):
        self.code = code
        self.name = name
        self.price = price

    def get_code(self):
    # 商品コードを返す
        return self.code

    def get_name(self):
    # 商品名を返す
        return self.name

    def get_price(self):
    # 価格を返す
        return self.price

### 商品マスタクラス
class ItemMaster:
    def __init__(self):
        self.item_master = []

    def addItem(self,item):
    #商品クラスを追加する
        self.item_master.append(item)

    def getMenu(self):
    # メニューを返す

        menu = "*** メニュー ***<BR>" 
        for item in self.item_master:
            code = item.get_code()
            str = "{} {} {}円 <a href=\"javascript:OnLinkClick('" + code + "');\">かごに入れる</a><BR>"
            menu += str.format(item.get_code(),item.get_name(),item.get_price())        
        return menu

    def searchItem(self,code):
    # 商品コードをキーに商品マスタを検索する
        for item in self.item_master:
            if item.get_code() == code:
                return item

### オーダークラス
class Order:
    def __init__(self):
        # 受注した商品
        self.code = ""      # 商品コード
        self.name = ""      # 商品名
        self.price = ""      # 価格

        # 受注計算結果
        self.goukei = 0     # 合計
        self.oazukari = 0   # お預かり
        self.oturi = 0      # おつり

        self.item_order_list=[]

    def setMaster(self,item_master):
        self.item_master = item_master

    def add_item_order(self,code,kosu):
    # オーダーを追加する
        self.item_order_list.clear()
        self.item_order_list.append([code,kosu])

    def view_item_list(self):
    # オーダー内容を表示する
        for item in self.item_order_list:
            orderCord = item[0]
            orderKosu = item[1]
                        
            # 商品コードからマスタ情報を取得する
            master = self.item_master.searchItem(orderCord)

            if master is None:
                str = "商品コード:{}は当店では取り扱っていない商品です。".format(orderCord)
                break
            else:
                str = "*** 注文内容 ***<BR>"
                #商品コードを表示する
                str += "商品コード:{}<BR>".format(master.get_code())
                #商品名を表示する
                str += "商品名:{}<BR>".format(master.get_name())
                #価格を表示する
                str += "価格:{}<BR>".format(master.get_price())
                #個数を表示する
                str += "個数:{}<BR>".format(orderKosu)
                #合計金額を表示する
                self.goukei = int(orderKosu) * master.get_price()
                str += "合計金額:{}円になります。".format(self.goukei)

        return str

    def getOturi(self,oazukari):
    # おつりを計算する
        self.oazukari = int(oazukari)
        self.oturi = self.oazukari - self.goukei

        if self.oturi == 0:
            str = "ちょうどですね。ありがとうございました！"
        elif self.oturi > 0:
            str = "おつり{}円になります。ありがとうございました！".format(self.oturi)
        else:
            str = "お客さん、お金が足りませんよ！"

        return str

    def createReceipt(self):
    # レシートを発行する
        fileName = "{:%Y%m%d%H%M%S}.csv".format(datetime.datetime.now())
        receipt = open(fileName, "w", encoding="UTF-8")

        for item in self.item_order_list:
            orderCord = item[0]
            orderKosu = item[1]

            # 商品コードからマスタ情報を取得する
            master = self.item_master.searchItem(orderCord)           

            text = "*** 領収書 ***\n"
            text += "商品コード:{}\n".format(master.get_code())
            text += "商品名:{}\n".format(master.get_name())
            text += "価格:{}\n".format(master.get_price())
            text += "個数:{}\n".format(orderKosu)

            text += "合計金額:{}円\n".format(self.goukei)
            text += "お預かり金額:{}円\n".format(self.oazukari)
            text += "おつり:{}円".format(self.oturi)
            
        receipt.write(text)
        receipt.close

        return fileName