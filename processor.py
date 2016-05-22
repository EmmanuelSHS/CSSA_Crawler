#!/usr/bin/env python
# coding=utf-8


class Processor:
    """
    a processor find useful threads with keywords
    """
    def __init__(self, KEYWORDS, forms):
        self.keywords = KEYWORDS
        self.forms = forms

    def run(self):
        res = []

        for f in self.forms:
            for word in self.keywords:
                if word in f.content:
                    res.append(f)

        return res
