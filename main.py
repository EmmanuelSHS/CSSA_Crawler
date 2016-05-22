#!/usr/bin/env python
# coding=utf-8

from parser import Parser
from processor import Processor
from models import SendEmail
import time


def main():
    KEYWORDS = [u'空调']

    # parser forms
    parser = Parser()
    forms = parser.run()

    # process commited forms via Processor
    processor = Processor(KEYWORDS, forms)
    res = processor.run()

    # send email
    if res:
        sender = SendEmail(res)
        print "email sent"
    else:
        print "no required form now", time.time()


if __name__ == '__main__':
    while True:
        main()
        time.sleep(7200)

