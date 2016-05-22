#!/usr/bin/env python
# coding=utf-8

from models import SecondHand, database
import feedparser
import urllib2
import re
from time import mktime, sleep
from datetime import datetime
from sqlalchemy import desc
from sqlalchemy.orm.exc import NoResultFound
from bs4 import BeautifulSoup

TEST = False 

class Parser:
    def __init__(self,):
        self.feed = 'feed://www.cubbs.org/forum.php?mod=rss&fid=41&auth=0'
        self.db = database()
        self.ltid = None

    def getFeed(self):
        fparser = feedparser.parse(self.feed)
        return fparser

    def formatdate(self, rawdate):
        date = datetime.fromtimestamp(mktime(rawdate))
        return date

    def coarseParse(self, feeds):
        # update the latest thread, avoid duplicates
        self.getLatest()

        print '# new feeds', len(feeds.entries)
        
        rawforms = []
        for i in feeds.entries:
            rf = {'link': None, 'tid': None, 'uid': None, 'content': None, 'postdate': None}
            
            rf['link'] = i['link']
            rf['tid'] = int(rf['link'].split('=')[-1])

            rf['postdate'] = self.formatdate(i['published_parsed'])

            if rf['tid'] > self.ltid:
                rawforms.append(rf)

        return rawforms
        
    def getLatest(self):
        """retrieve latest form in database, tid is mono increasing"""
        try:
            self.ltid = self.db.session.query(SecondHand.tid).order_by(desc(SecondHand.tid)).first()[0]
        except (NoResultFound, TypeError):
            self.ltid = 0

    def getContent(self, fullcontent):
        # TODO: potential in eliminating blank lines
        soup = BeautifulSoup(fullcontent)
        content = soup.find_all("table")[6]

        return content.text

    def getUid(self, fullcontent):
        ure = re.compile(r'mod=space&amp;uid=(\d+)')
        uid = re.findall(ure, fullcontent)
        if not uid:
            return None
        return uid[0]

    def fineParse(self, rf):
        link = rf['link']

        req = urllib2.Request(link)
        for i in range(10):
            try:
                response = urllib2.urlopen(req)
                fullcontent = response.read()
                break
            except urllib2.HTTPError, e:
                print 'server could not fulfill the request'
                print e
                sleep(10)
            except urllib2.URLError, e:
                print 'connection failed'
                print e
                sleep(10)

        rf['content'] = self.getContent(fullcontent) 
        rf['uid'] = self.getUid(fullcontent)

    def makeForm(self, parsed):
        form = SecondHand()

        form.tid = parsed['tid']
        form.uid = parsed['uid']
        form.content = parsed['content']
        form.postdate = parsed['postdate']
        
        return form

    def run(self):
        """provide interface with processor in this return method"""
        # feed fetch from RSS
        feeds = self.getFeed()
        
        # coarse parsing
        rawforms = self.coarseParse(feeds)

        # fine granularity parsing
        forms = []
        for rf in rawforms:
            if self.ltid < rf['tid']:
                self.fineParse(rf)
                f = self.makeForm(rf)
                forms.append(f)

        # commit & return
        if not TEST:
            self.db.session.add_all(forms)
            self.db.session.commit()
            
            print "# forms submitted", len(forms)

        else:
            print forms

        return forms

if __name__ == '__main__':
    p = Parser()
    p.run()
