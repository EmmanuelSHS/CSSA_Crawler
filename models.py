#!/usr/bin/env python
# coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.schema import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mysql import INTEGER, TEXT, DATETIME
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import smtplib


Base = declarative_base()

USR = 'program'
PWD = 'passwordforprogram'
HOST = 'localhost'
DB = 'forum'
EXPIRE_ON_COMMIT = True


class database:
    def __init__(self):
        self.engine = create_engine('mysql+mysqlconnector://'+USR+':'+PWD+'@'+HOST+'/'+DB, pool_recycle=3600)
        Session = sessionmaker(bind=self.engine,expire_on_commit = EXPIRE_ON_COMMIT, autoflush = False)
        self.session = Session()


class SecondHand(Base):
    __tablename__ = 'secondhand'
    tid = Column(INTEGER, primary_key=True)
    uid = Column(INTEGER, primary_key=True)
    postdate = Column(DATETIME)
    content = Column(TEXT)
    def __repr__(self):
        return "<thread='{0}'>".format(self.tid)

#####################################

LINKHEAD = "http://www.cubbs.org/forum.php?mod=viewthread&tid=" 

class SendEmail:
    def __init__(self, res):
        self.sender = 'emmanuel.wang.93@gmail.com'
        self.receiver = ['clochard93@gmail.com']
        self.subject = "Updated Threads w Keywords"
        self.content = str(datetime.datetime.now()) + self.contentMaker(res)
        self.smtpserver = "smtp.gmail.com:587"
        self.password = "public200240"

        self.sendEmail()

    def sendEmail(self):
        msgRoot = MIMEMultipart('related')
        msgRoot["To"] = ','.join(self.receiver)
        msgRoot["From"] = self.sender
        msgRoot['Subject'] =  self.subject
        msgText = MIMEText(self.content,'html','utf-8')
        msgRoot.attach(msgText)
        smtp = smtplib.SMTP(self.smtpserver)
        smtp.starttls()
        smtp.login(self.sender, self.password)
        smtp.sendmail(self.sender, self.receiver, msgRoot.as_string())
        smtp.quit()

    def contentMaker(self, res):
        content = '\n'
        for f in res:
            content += LINKHEAD+str(f.tid)+'\n'
        return content


if __name__ == '__main__':
    t1 = database()
    t2 = SecondHand()

