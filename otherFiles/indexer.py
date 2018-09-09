from __future__ import print_function
import sys
import os
import time
from collections import *
import xml.etree.ElementTree as etree
from parser import *

def strip_tag_name(t):
    #print(t)
    #t = elem.tag
    idx = k = t.rfind("}")
    if idx != -1:
        t = t[idx + 1:]
    return t

def createIndex(XML_PATH):
    countPage = 0
    indexDict = defaultdict(str)
    for event, elem in etree.iterparse(XML_PATH, events=('start', 'end')):
        tname = strip_tag_name(elem.tag)
        if event == 'start' :
            if tname == 'page':
                countPage += 1
                titleDict = defaultdict()
                bodyDict = defaultdict()
                categoryDict = defaultdict()
                linkDict = defaultdict()
                temp = defaultdict(bool)

        else:
            if tname=='title':
                #try:
                titleDict = titleField(elem.text)
                #except:
                #    pass

            elif tname == 'text':
                #try :
                linkDict, bodyDict, categoryDict = textTagProcessing(elem.text)
                # except:
                #     pass
            elif tname == 'page':
                #print(titleDict)
                info = '|d' + str(countPage)
                if titleDict:
                    for word in titleDict:
                        indexDict[word] += info + 't' + str(titleDict[word])
                        temp[word] = True
                if bodyDict:
                    for word in bodyDict:
                        if not temp[word]:
                            indexDict[word] += info + 'b' + str(bodyDict[word])
                            temp[word] = True
                        else:
                            indexDict[word] += 'b' + str(bodyDict[word])
                if indexDict:
                    for word in categoryDict:
                        if not temp[word]:
                            indexDict[word] += info + 'c' + str(categoryDict[word])
                            temp[word] = True
                        else:
                            indexDict[word] += 'b' + str(categoryDict[word])
                if linkDict:
                    for word in linkDict:
                        if not temp[word]:
                            indexDict[word] += info + 'l' + str(linkDict[word])
                            temp[word] = True
                        else:
                            indexDict[word] += 'b' + str(linkDict[word])

                elem.clear()
                #print (indexDict)
    return indexDict

def writeIndex():
    arg = sys.argv
    XML_PATH = arg[1]
    f = open(arg[2],'w')
    indexWord = createIndex(XML_PATH)
    for word in sorted(indexWord):
        # ind = ''
        # ind = '|'.join(indexWord[word])
        D = word+':'+indexWord[word]
        print(D,file=f)
    f.close()

writeIndex()
