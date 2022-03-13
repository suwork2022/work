from email import message
import smtplib
import logging
from logcontrol import LogControl 
import propertys as pr
lg = LogControl()

class MailControl:
#   ■SendOutlookMail(mailmessage)
#   メールを送信する。
#   引数1[mailmessage]:メール本文を指定
#   その他設定はproperty.pyにて。
    def SendOutlookMail(self,mailmessage):
        loggername = lg.getloggername()
        logger = logging.getLogger(loggername)
        logger.info(' □MailControl SendOutlookMail start')
        
        msg = message.EmailMessage()
        msg.set_content(mailmessage)
        msg['Subject'] = pr.p_mail_sub
        msg['From'] = pr.p_from_email
        msg['To'] = pr.p_to_email
        
        server = smtplib.SMTP(pr.p_smtp_host, pr.p_smtp_port)
        server.starttls()
        server.login(pr.p_username, pr.p_password)
        server.send_message(msg)
        server.quit()
        logger.info(' □MailControl SendOutlookMail end')
        return
