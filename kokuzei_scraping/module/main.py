import datetime
import logging
import inspect
import pandas as pd
from filecontrol import FileControl
from logcontrol import LogControl
from mailcontrol import MailControl
from kokuzei import Kokuzei
import propertys as pr
pd.set_option('max_colwidth',pr.p_max_colwidth)
pd.set_option('max_columns', pr.p_max_columns)

def main():
    # 初期データセット
    fc = FileControl()
    kok = Kokuzei()
    lc = LogControl()
    mc = MailControl()
    d = datetime.datetime.now()
    daystr = d.strftime('%Y%m%d')
    timestr = d.strftime('%H%M%S')
    logfile = "./log/sc_" + daystr + timestr + ".log"
    methodname = inspect.currentframe().f_code.co_name
    noticedata = pd.DataFrame(columns=['name', 'midashi', 'url'])
    logger = lc.setup_logger(methodname,logfile)
    logger.info('■main start')
    
    # 設定ファイル読み込み
    pathstr='settei.xls'
    headerrow=0
    sheetnum=0
    colrange=5
    rowrange=10
    setteiexcel = fc.ExcelSheetRead(pathstr,headerrow,sheetnum,colrange,rowrange)
    
    # サイト別スクレイピング
    for ind,rowvalue in setteiexcel.iterrows():
        sckey=rowvalue['キー']
        no=rowvalue['No.']
        scname=rowvalue['名称']
        keyword=rowvalue['keyword']
        setsumei=rowvalue['説明']
        if sckey == 'kokuzei': #国税庁
            if no == 1: #パンフレット
                #当日分データ取得
                scdata = kok.PamphletParse(sckey,no,keyword)
        #elif sckey == 2: #総務省
        #elif sckey == 3: #etax
        #elif sckey == 4: #eltax
        else:
            continue
        #前回分データ取得
        scdata_prev = fc.PrevFileGet(sckey,no)
        #マージ
        scdata_merge = scdata.merge(scdata_prev, on=["sckey","no","midashi"], how="outer", indicator=True)
        #差分レコード抽出
        scdata_diff = scdata_merge[scdata_merge["_merge"]=="left_only"]
        if len(scdata_diff) != 0:
            for dind,drowvalue in scdata_diff.iterrows():
                diffmidashi = drowvalue['midashi']
                diffurl = drowvalue['url_x']
                addRow = pd.DataFrame({'name':[scname],'midashi':[diffmidashi],'url':[diffurl]})
                noticedata = noticedata.append(addRow)
        #当日分データ出力
        fc.CurrentFilePut(sckey,no,scdata)
    #通知
    if len(noticedata) != 0:
        mailmessage = ''
        for nind,nrowvalue in noticedata.iterrows():
            noticename = nrowvalue['name']
            noticemidashi = nrowvalue['midashi']
            noticeurl = nrowvalue['url']
            mailmessage = mailmessage + noticename + '\r\n' + noticemidashi + '\r\n' + noticeurl + '\r\n' + '\r\n'
        mc.SendOutlookMail(mailmessage)
    logger.info('■main end')

if __name__ == '__main__':
    main()

