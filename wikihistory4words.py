#!/usr/bin/env python

##########################################################################
#                                                                        #
#  This program is free software; you can redistribute it and/or modify  #
#  it under the terms of the GNU General Public License as published by  #
#  the Free Software Foundation; version 2 of the License.               #
#                                                                        #
#  This program is distributed in the hope that it will be useful,       #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of        #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
#  GNU General Public License for more details.                          #
#                                                                        #
##########################################################################

import sys
import os
from datetime import date
from random import random
import nltk

## PROJECT LIBS
from sonet.mediawiki import HistoryPageProcessor, explode_dump_filename, \
     getTranslations, getTags
from sonet import lib

## DJANGO
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_wikinetwork.settings'
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PROJECT_ROOT+'/django_wikinetwork')
from django_wikinetwork.wikinetwork.models import WikiWord
from django.db import transaction


class HistoryWordsPageProcessor(HistoryPageProcessor):
    words = None
    counter_words = 0
    counter_desired_words = None
    counter_first = None
    _check_creation = True
    _creation = None

    def __init__(self, **kwargs):
        super(HistoryWordsPageProcessor, self).__init__(**kwargs)
        self.tokenizer = nltk.PunktWordTokenizer()
        self.stopwords = frozenset(nltk.corpus.stopwords.words('italian'))

        self.counter_desired_words = nltk.FreqDist()

    def process_text(self, elem):
        if self._skip:
            return

        try:
            text = elem.text.encode('utf-8')
        except AttributeError: ##TODO:increment revision count?
            ## this tag is empty
            return
        tokens = self.tokenizer.tokenize(nltk.clean_html(text.lower()))

        ##TODO: togliere questo limite sulla lunghezza?
        text = [t for t in tokens if len(t) > 2 and
                         t not in self.stopwords]
        self.counter_words += len(text)

        self.counter_desired_words.update(text)

        self.count += 1
        if not self.count % 100000:
            print 'PAGES:', self.counter_pages, 'REVS:', self.count
            sys.exit(0)

    def process_timestamp(self, elem):
        if self._skip or not self._check_creation: return

        timestamp = elem.text
        year = int(timestamp[:4])
        month = int(timestamp[5:7])
        day = int(timestamp[8:10])
        revision_time = date(year, month, day)
        if self._creation is None:
            self._creation = revision_time
        elif (revision_time - self._creation).days > 7:
            self.counter_first = self.counter_desired_words.copy()
            self._check_creation = False


    def save(self):
        #print '-'*10, self._type+":", self._title.encode('utf-8'), '-'*10

        data = dict((k, v) for k, v in
                    ((word, self.counter_desired_words.freq(word))
                    for word in self.words) if v > 0)
        #for word in self.words:
        #    print word, self.counter_desired_words.freq(word)
        #print data
        del self.counter_desired_words
        ww = WikiWord(
            title=self._title,
            lang=self.lang,
            desired=self._desired,
            talk=(self._type == 'talk')
        )
        if data:
            ww.data = data
        if self.counter_first:
            data_first = dict((k, v) for k, v in
                              ((word, self.counter_first.freq(word))
                               for word in self.words) if v > 0)
            if data_first:
                ww.data_first = data_first
        elif data:
            ww.data_first = data
        ##ww.save()
        self.counter_pages += 1

        self.counter_desired_words = nltk.FreqDist()
        self._check_creation = True
        self._creation = None


def get_lines_in_list(fn):
    with open(fn) as f:
        lines = f.readlines()

    return [l.decode('latin-1') for l in [l.strip() for l in lines]
            if l and not l[0] == '#']


def main():
    import optparse

    p = optparse.OptionParser(usage="usage: %prog [options] file desired_list acceptance_ratio")
    _, files = p.parse_args()

    if not files:
        p.error("Give me a file, please ;-)")

    xml = files[0]
    desired_pages_fn = files[1]
    desired_words_fn = files[2]
    threshold = float(files[3])

    desired_pages = get_lines_in_list(desired_pages_fn)
    desired_words = [w.lower() for w in get_lines_in_list(desired_words_fn)]

    lang, _, _ = explode_dump_filename(xml)

    deflate, _lineno = lib.find_open_for_this_file(xml)

    if _lineno:
        src = deflate(xml, 51)
    else:
        src = deflate(xml)

    translation = getTranslations(src)
    tag = getTags(src, tags='page,title,revision,'+ \
                  'minor,timestamp,redirect,text')

    src.close()
    src = deflate(xml)

    processor = HistoryWordsPageProcessor(tag=tag, lang=lang)
    processor.talkns = translation['Talk']
    processor.threshold = threshold
    processor.set_desired(desired_pages)
    processor.words = desired_words

    print "BEGIN PARSING"
    processor.start(src)


if __name__ == "__main__":
    import cProfile as profile
    profile.run('main()', 'mainprof')
    #main()