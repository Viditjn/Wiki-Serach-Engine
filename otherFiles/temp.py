from __future__ import print_function
from Stemmer import Stemmer
import re
import sys
import os
import time
from collections import *
import xml.etree.ElementTree as etree
reload(sys)
sys.setdefaultencoding('utf-8')


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
numVar = 4
tagNum = {'title':0,'text':1,'category':2,'links':3}
tagName = {0:'t',1:'b',2:'c',3:'l'}
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
            if tname == 'text':
                tmpword = re.findall("\[\[Category:(.*?)\]\]",str(elem.text))
                if tmpword :
                    for tmp in tmpword :
                        tmp = tmp.lower()
                        tmp = re.split("[^a-zA-Z]",tmp)
                        #stemword = ps.stemWord(tmp)
                        for tmp1 in tmp:
                            if tmp1:
                                w = stemmer.stemWord(tmp1)
                                if w not in stopWord:
                                    if w not in tempFreq:
                                        tempFreq[w] = [0,0,0,0]
                                    tempFreq[w][2] += 1
                da = elem.text
                if da:
                    tmpword = da.split("==External links==")
                    if len(tmpword)>1:
                        lines = tmpword[1].split('\n')
                        for line in lines:
                            line = line.lower()
                            if "* [" in line or "*[" in line:
                                words = re.split(r'[^A-Za-z]+', line)
                                for word in words:
                                    if word:
                                        if word != 'http' and word not in stopWord:
                                            w = stemmer.stemWord(word)
                                            if w not in tempFreq:
                                                tempFreq[w] = [0,0,0,0]
                                            tempFreq[w][3] += 1
            data = re.split("[^a-zA-Z]",data)
            for word in data:
                if word:
                    word = word.lower()
                    if word not in stopWord :
                        w = stemmer.stemWord(word)
                        if w not in tempFreq:
                            tempFreq[w] = [0,0,0,0]
                        tempFreq[w][tagNum[tname]] += 1

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
