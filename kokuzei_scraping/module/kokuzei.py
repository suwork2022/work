#
import requests
import logging
import pandas as pd
from bs4 import BeautifulSoup as bs4
from time import sleep 
from logcontrol import LogControl 
baseurl = 'https://www.nta.go.jp/'
lg = LogControl()

class Kokuzei:
#   ■PamphletParse(sckey,no,keyword)
#   国税庁HP「パンフレット・手引き」から法定調書関係の見出し・URLを取得する。
#   引数1[sckey]:スクレイピングキーを指定
#   引数2[no]:連番を指定
#   引数3[keyword]:検索キーワードを指定（複数可能・基本的にはor条件
#   返却値:取得したURL・見出しのDataFrame
    def PamphletParse(self,sckey,no,keyword):
        loggername = lg.getloggername()
        logger = logging.getLogger(loggername)
        logger.info('■Kokuzei PamphletParse start')
        keywordlist = keyword.split(sep=',')
        
        # 対象中見出しのidを指定
        sel_key1='a-12'
        req = requests.get('https://www.nta.go.jp/publication/pamph/01.htm')
        sup = bs4(req.content,'html.parser')
        sel_elm = sup.find(id=sel_key1)
        
        #ULに移動
        for i in range(3):
            sel_elm = sel_elm.next_element
        
        #dataframe用意
        scdata = pd.DataFrame(columns=['sckey', 'no', 'midashi', 'url' , 'lastupd'])
        sel_li = sel_elm.find_all("li")
        #li取得
        for elm_li in sel_li:
            midashi = elm_li.text
            atag = elm_li.a
            elmurl = baseurl + atag.get('href')
            lastupd = '' #PDFファイルへのリンクであるため取得不可
            addRow = pd.DataFrame([sckey,no,midashi,elmurl,lastupd], index=scdata.columns).T
            scdata = scdata.append(addRow)
        scdata = scdata.reset_index(drop=True)
        #キーワードを含むもののみを抽出
        scdata = scdata.query('midashi.str.contains("|".join(@keywordlist))', engine='python')
        logger.info('■Kokuzei PamphletParse end')
        return scdata
