#from nltk.stem.porter import PorterStemmer
from __future__ import print_function
from Stemmer import Stemmer
import re
import sys
import os
import time
from collections import *
import xml.etree.ElementTree as etree


def strip_tag_name(t):
    t = elem.tag
    idx = k = t.rfind("}")
    if idx != -1:
        t = t[idx + 1:]
    return t

stemmer = Stemmer("english")
stopWord = defaultdict(bool)
arg=sys.argv
indexWord = defaultdict(list)
tempFreq = defaultdict(list)
FILE_XML_PATH = arg[1]
stopWordPath = 'Stop_words.txt'
co = 0
countPage = 0
start_time = time.time()
#for the field query
numVar = 2
tagNum = {'title':0,'text':1}
tagName = {0:'t',1:'b'}
tags = {'title','text'}
# print sys.argv
with open(stopWordPath,'r') as stopword:
    for line in stopword:
        for w in re.split('[ , \"\n]+',line):
            if w:
                stopWord[w] = True

for event, elem in etree.iterparse(FILE_XML_PATH, events=('start', 'end')):
    tname = strip_tag_name(elem.tag)
    if event == 'start' :
        if tname == 'page':
            countPage += 1
            tempFreq.clear()

    else:
        if tname in tags:
            data = elem.text
            if not data:
                continue
            try :
                data = re.split("[^a-zA-Z]",data)
                for word in data:
                    if word:
                        word = word.lower()
                        if word not in stopWord :
                            w = stemmer.stemWord(word)
                            if w not in tempFreq:
                                tempFreq[w] = [0,0]
                            tempFreq[w][tagNum[tname]] += 1
            except :
                pass

        elif tname == 'page':
            try :
                for word in tempFreq:
                    info = 'd' + str(countPage)
                    for i in range(numVar):
                        temp = tempFreq[word]
                        if temp[i] != 0:
                            info = str(info) + str(tagName[i]) + str(temp[i])
                    indexWord[word].append(info)
            except:
                pass

            elem.clear()

#print len(indexWord)
f = open(arg[2],'w')
for word in sorted(indexWord):
    ind = ''
    ind = '|'.join(indexWord[word])
    D = word+':'+ind
    print(D,file=f)

f.close()
