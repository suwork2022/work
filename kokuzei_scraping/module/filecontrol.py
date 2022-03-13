import datetime
import pandas as pd
from glob import glob
import os
import logging
import inspect
from logcontrol import LogControl 
lg = LogControl()

class FileControl:
#   ■ExcelSheetRead(pathstr,headerrow,sheetnum,colrange,rowrange)
#   指定したEXCELブックから特定のシートを読み込む。
#   引数1[pathstr]:EXCELブックのファイルパスを指定
#   引数2[headerrow]:ヘッダー行を指定
#   引数3[sheetnum]:読み込むシート番号を０オリジンで指定（シートの左から順に０，１，２，……
#   引数4[colrange]:読み込む列範囲を０オリジンで指定（例：4を指定したら5列目（E列）まで取得
#   引数5[rowrange]:読み込む行範囲を０オリジンで指定（例：5を指定したら6行目まで取得
#   返却値:指定ファイルのDataFrame
    def ExcelSheetRead(self,pathstr,headerrow,sheetnum,colrange,rowrange):
        loggername = lg.getloggername()
        logger = logging.getLogger(loggername)
        logger.info(' □FileControl ExcelSheetRead start')
        usecollist = list(range(colrange))
        input_sheet = pd.read_excel(pathstr,header=headerrow,sheet_name=0,usecols=usecollist,nrows=rowrange)
        logger.info(' □FileControl ExcelSheetRead end')
        return input_sheet

#   ■ExcelbookRead(pathstr)
#   指定したEXCELブックを読み込む。
#   引数1[pathstr]:EXCELブックのファイルパスを指定
#   返却値:指定ファイルのDataFrame
    def ExcelbookRead(self,pathstr):
        loggername = lg.getloggername()
        logger = logging.getLogger(loggername)
        logger.info(' □FileControl ExcelbookRead start')
        input_book = input_book = pd.ExcelFile(pathstr)
        logger.info(' □FileControl ExcelbookRead end')
        return input_book

#   ■PrevFileGet(sckey,no)
#   引数に指定したキー・番号に該当する最新のCSVファイルを取得して読み込む。
#   引数1[sckey]:スクレイピングキーを指定
#   引数2[no]:連番を指定
#   返却値:指定ファイルのDataFrame
#   例）sckey='kokuzei'、no=1で呼び出された場合、[./data/kokuzei]フォルダ配下の最新の[kokuzei_1_*.csv]を取得する。
    def PrevFileGet(self,sckey,no):
        loggername = lg.getloggername()
        logger = logging.getLogger(loggername)
        logger.info(' □FileControl PrevFileGet start')
        dirpath = "./data/" + sckey
        prevfilepath = self.get_latest_modified_file_path(dirpath,sckey,no)
        prevfilepath = str(prevfilepath).replace('\\','/')
        input_sheet = pd.read_csv(prevfilepath)
        logger.info(' □FileControl PrevFileGet end')
        return input_sheet

#   ■CurrentFilePut(sckey,no,outdata)
#   引数に指定したDataFrameをキー・番号・タイムスタンプでファイル名を生成してCSV出力する。
#   引数1[sckey]:スクレイピングキーを指定
#   引数2[no]:連番を指定
#   引数3[outdata]:出力対象のDataFrame
#   返却値:なし
    def CurrentFilePut(self,sckey,no,outdata):
        loggername = lg.getloggername()
        logger = logging.getLogger(loggername)
        logger.info(' □FileControl CurrentFilePut start')
        d = datetime.datetime.now()
        daystr = d.strftime('%Y%m%d')
        timestr = d.strftime('%H%M%S')
        outdata.to_csv("./data/" + str(sckey) + "/" + str(sckey) + "_" + str(no) + "_" + str(daystr) + str(timestr) + ".csv",index=False)
        logger.info(' □FileControl CurrentFilePut end')
        return 

#   ■get_latest_modified_file_path(dirname,sckey,no)
#   引数に指定したディレクトリ内でキー・番号に該当する最新のCSVファイル名を取得する。
#   引数1[dirname]:取得先ディレクトリを指定
#   引数2[sckey]:スクレイピングキーを指定
#   引数3[no]:連番を指定
#   返却値:最新ファイル名
    def get_latest_modified_file_path(self,dirname,sckey,no):
        loggername = lg.getloggername()
        logger = logging.getLogger(loggername)
        logger.info(' □FileControl get_latest_modified_file_path start')
        target = os.path.join(dirname, str(sckey) + '_' + str(no) + '_' + '*.csv')
        files = [(f, os.path.getmtime(f)) for f in glob(target)]
        latest_modified_file_path = sorted(files, key=lambda files: files[1])[-1]
        logger.info(' □FileControl get_latest_modified_file_path end')
        return latest_modified_file_path[0]

