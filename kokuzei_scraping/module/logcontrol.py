#
import logging
import inspect
import propertys as pr

class LogControl:
#   ■setup_logger(name,logfile)
#   ロガーを作成して返却する。
#   引数1[name]:ロガー名称を指定
#   引数2[logfile]:ログファイルアドレスを指定
#   返却値:ロガー
    def setup_logger(self,name,logfile):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        # ファイルハンドラ作成・設定
        fh = logging.FileHandler(logfile)
        fh.setLevel(logging.DEBUG) # 【ログレベル】 低（DEBUG ⇒ INFO ⇒ WARNING ⇒ ERROR ⇒ CRITICAL）高
        fh_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(name)s - %(funcName)s - %(message)s')
        fh.setFormatter(fh_formatter)

        # コンソールハンドラ作成・設定
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG) # 【ログレベル】 低（DEBUG ⇒ INFO ⇒ WARNING ⇒ ERROR ⇒ CRITICAL）高
        ch_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
        ch.setFormatter(ch_formatter)

        # ハンドラ追加
        logger.addHandler(fh)
        logger.addHandler(ch)
        return logger

#   ■getloggername()
#   呼び出し元メソッドを上位から順に取得、ピリオド（.）区切りで文字列連結して返却する。
#   返却値:呼び出し関係にある全メソッド名称
    def getloggername(self):
        loggername = ''
        last = len(inspect.stack()) - 1
        for i in range(1,last):
            if loggername == '':
                loggername = inspect.stack()[i].function
            else:
                loggername = inspect.stack()[i].function + '.' + loggername
        return loggername

#   ■gethighloggername()
#   呼び出し元メソッド名を上位から順に取得、ピリオド（.）区切りで文字列連結して返却する。※gethighloggername()を呼び出したメソッド名は除く
#   返却値:呼び出し関係にある全メソッド名称（自身以外
    def gethighloggername(self):
        loggername = ''
        last = len(inspect.stack()) - 1
        for i in range(2,last):
            if loggername == '':
                loggername = inspect.stack()[i].function
            else:
                loggername = inspect.stack()[i].function + '.' + loggername
        return loggername

