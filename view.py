import eel
import sys
import pandas as pd

import desktop
import pos  #POSクラス

app_name="html"
end_point="index.html"
size=(600,900)

item_master = pos.ItemMaster()  # 商品マスタ
order = pos.Order()

@ eel.expose
def getMenu():

    # マスタファイルを読み込む
    try:
        df = pd.read_csv("item_mast.csv",dtype={"商品コード":str,"商品名":str,"価格":int})
    except FileNotFoundError:
        print("マスタファイルが見つかりませんでした")
        sys.exit(0)

    for code, name, kakaku in zip(df["商品コード"], df["商品名"], df["価格"]):

        item_master.addItem(pos.Item(code,name,kakaku))

    order.setMaster(item_master)

    # メニューを画面に出力する
    menu = item_master.getMenu()
    eel.view_menu_js(menu)

@ eel.expose
def addOrder(code,kazu):
    # オーダー登録
    order.add_item_order(code,kazu)

    # オーダー内容を画面に表示する
    kakunin = order.view_item_list()
    eel.view_kakunin_js(kakunin)
 
@ eel.expose
def getOturi(oazukari):
    # おつりを計算して画面に表示する
    oturi = order.getOturi(oazukari)
    eel.view_oturi_js(oturi)

@ eel.expose
def createReceipt():
    # 領収書を発行する
    fileName = order.createReceipt()

desktop.start(app_name,end_point,size)