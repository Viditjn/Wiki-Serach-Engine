from __future__ import print_function
import sys
import os
import time
from collections import *
import xml.etree.ElementTree as etree
from parser import *
import bz2
import heapq
import operator
import math

vocabList = set()
fileNumber = 0
countPage = -1
offsetDict = {'T':{},'B':{},'C':{},'L':{}}
offsetTitle = {}
off = 0

def strip_tag_name(t):
    idx = k = t.rfind("}")
    if idx != -1:
        t = t[idx + 1:]
    return t

def createIndex(XML_PATH):
    try :
        os.remove('title.txt')
    except:
        pass
    global fileNumber
    global countPage
    ctemp = 0
    TDict = defaultdict(str)
    BDict = defaultdict(str)
    CDict = defaultdict(str)
    # IDict = defaultdict(str)
    LDict = defaultdict(str)
    titleStore = defaultdict(str)
    pagesPerFile = 10000
    prevPage = 0
    for event, elem in etree.iterparse(XML_PATH, events=('start', 'end')):
        tname = strip_tag_name(elem.tag)
        if event == 'start' :
            if tname == 'page':
                titleDict = defaultdict()
                bodyDict = defaultdict()
                categoryDict = defaultdict()
                #infoDict = defaultdict()
                linkDict = defaultdict()
                temp = defaultdict(bool)
                countPage += 1

        else:
            if tname=='title':
                try:
                    ctemp+=1
                    #   print (elem.text)
                    titleStore[countPage] = str(countPage) + ' ' + (elem.text).encode('utf-8')
                    titleDict = titleField(elem.text)
                except:
                    import pdb
                    pdb.set_trace()
                    pass

            elif tname == 'text':
                try :
                    linkDict, bodyDict, categoryDict, infoDict = textTagProcessing(elem.text)
                except:
                    pass
            elif tname == 'page':
                info = '|d' + str(countPage)
                if titleDict:
                    for word in titleDict:
                        TDict[word] += info + 't' + str(titleDict[word])

                if bodyDict:
                    for word in bodyDict:
                        BDict[word] += info + 'b' + str(bodyDict[word])

                if categoryDict:
                    for word in categoryDict:
                        CDict[word] += info + 'c' + str(categoryDict[word])

                # if infoDict:
                #     for word in infoDict:
                #         IDict[word] += info + 'i' + str(infoDict[word])

                if linkDict:
                    for word in linkDict:
                        LDict[word] += info + 'l' + str(linkDict[word])

                elem.clear()

        if countPage % pagesPerFile == 0 and countPage != 0 and countPage != prevPage:
            #vocabList = set(list(vocabList)+indexDict.keys())
            prevPage = countPage
            writeTitle(titleStore)
            #print('len : ',len(titleStore))
            # writeIndexPart(indexDict,fileNumber)
            writeIndexPart(TDict,fileNumber,'T')
            writeIndexPart(BDict,fileNumber,'B')
            writeIndexPart(CDict,fileNumber,'C')
            #writeIndexPart(IDict,fileNumber,'I')
            writeIndexPart(LDict,fileNumber,'L')
            TDict = defaultdict(str)
            BDict = defaultdict(str)
            CDict = defaultdict(str)
            #IDict = defaultdict(str)
            LDict = defaultdict(str)
            titleStore = defaultdict(str)
            fileNumber += 1
    if BDict:
        writeIndexPart(TDict,fileNumber,'T')
        writeIndexPart(BDict,fileNumber,'B')
        writeIndexPart(CDict,fileNumber,'C')
        #writeIndexPart(IDict,fileNumber,'I')
        writeIndexPart(LDict,fileNumber,'L')
        #print(len(titleStore))
        writeTitle(titleStore)
        TDict = defaultdict(str)
        BDict = defaultdict(str)
        CDict = defaultdict(str)
        #IDict = defaultdict(str)
        LDict = defaultdict(str)
        titleStore = defaultdict(str)
        fileNumber += 1

    mergeFiles('T')
    mergeFiles('B')
    mergeFiles('C')
    mergeFiles('L')
    #mergeFiles('I')
    print(ctemp,countPage)
    # return indexDict

def writeTitle(titleStore):
    global off
    fileName = 'title.txt'
    f = open(fileName,'a')
    for word in sorted(titleStore):
        print(titleStore[word],file=f)
        offsetTitle[word] = off
        off += len(titleStore[word])+1
    f.close()
    #print('off : ',len(offsetTitle))

def writeIndexPart(indexWord,fileNumber,tag):
    fileName = str(fileNumber)+ tag + '.txt'
    f = open(fileName,'w')
    for word in sorted(indexWord):
        D = word+':'+indexWord[word]
        print(D,file=f)
    f.close()

offset = {'T':0,'B':0,'C':0,'L':0}

def mergeFiles(tag):                                                 #merge multiple primary indexes
    try :
        os.remove(tag+'temp.txt')
    except:
        pass
    listOfWords={}
    indexFile={}
    topOfFile={}
    flag=[0]*fileNumber
    data=defaultdict(list)
    heap=[]
    countFinalFile=0
    offsetSize = 0
    for i in xrange(fileNumber):
        fileName = str(i) + tag + '.txt'
        indexFile[i]= open(fileName, 'rb')
        flag[i]=1
        topOfFile[i]=indexFile[i].readline().strip()
        listOfWords[i] = topOfFile[i].split(':')
        if listOfWords[i][0] not in heap:
            heapq.heappush(heap, listOfWords[i][0])

    count=0
    while any(flag)==1:
        temp = heapq.heappop(heap)
        count+=1
        for i in xrange(fileNumber):
            if flag[i]:
                if listOfWords[i][0]==temp:
                    data[temp].extend(listOfWords[i][1:])
                    if count==1000000:
                        oldCountFile=countFinalFile
                        countFinalFile, offsetSize = writeFinalIndex(data, countFinalFile,tag)
                        if oldCountFile!=  countFinalFile:
                            data=defaultdict(list)

                    topOfFile[i]=indexFile[i].readline().strip()
                    if topOfFile[i]=='':
                            flag[i]=0
                            indexFile[i].close()
                            os.remove(str(i)+tag+'.txt')
                    else:
                        listOfWords[i] = topOfFile[i].split(':')
                        if listOfWords[i][0] not in heap:
                            heapq.heappush(heap, listOfWords[i][0])
    countFinalFile, offsetSize = writeFinalIndex(data, countFinalFile,tag)


def writeFinalIndex(data,countFinalFile,tag):
    #offset = 0
    global offset
    fileName = tag + 'temp.txt'
    f = open(fileName,'a')
    for word in sorted(data):
        offsetDict[tag][word] = offset[tag]
        D = word+':'
        scoreD = D
        for i in data[word]:
            D += i
        scoreD += getScore(D,tag)
        print(scoreD,file=f)
        offset[tag] += len(scoreD)+1
    f.close()
    return countFinalFile+1,0

def getScore(D,tag):
    global totalDocs
    docData = D.split(':')[1].split('|')
    totalDocHavingWord = len(docData)-1
    s = ''
    for doc in docData:
        if doc:
            temp = re.split("[a-zA-Z]",doc)
            try :
                if tag=='T' or tag=='B':
                    s += temp[1] + ' ' + str(round(round(math.log(countPage*1.0/totalDocHavingWord,10),2)*round(1+math.log(int(temp[2]),10),2),2)) + ' '
                else:
                    s += temp[1] + ' ' + str(round(1+math.log(int(temp[2]),10),2)) + ' '
            except:
                print(doc)
                print(temp)
    return s


def writeIndex():
    arg = sys.argv
    XML_PATH = arg[1]
    #f = open(arg[2],'w')
    createIndex(XML_PATH)
    for word in offsetDict:
        filename = word + '.txt'
        f = open(filename,'w')
        for w in sorted(offsetDict[word]):
            print(w + ' : ' + str(offsetDict[word][w]),file=f)
        f.close()
    filename = 'titleoff.txt'
    f = open(filename,'w')
    for w in offsetTitle:
        print(w,file=f)
    f.close()
    # for word in sorted(indexWord):
    #     D = word+':'+indexWord[word]
    #     print(D,file=f)
    # f.close()

writeIndex()
