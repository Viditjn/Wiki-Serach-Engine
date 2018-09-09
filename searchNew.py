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


championList = 10000

def createWordBnry(tag):
    listStart = {}
    dirName = os.getcwd()
    dirName += '/DATA/Merged/' + tag + '/offset.txt'
    i = 1
    with open(dirName) as f:
        for line in f:
            listStart[i] = line.strip()
            i += 1
    return listStart

def bnry(start,end,target,listStart):
    if start < 0:
        return start
    if end > len(listStart):
        return end
    if listStart[start] == target:
        return start
    if listStart[end] == target:
        return end

    if(start==end):
        return end
    mid = (end + start)/2
    if listStart[mid] <= target and listStart[mid+1] > target:
        return mid
    if listStart[mid] >= target:
        return bnry(start,mid-1,target,listStart)
    else:
        return bnry(mid+1,end,target,listStart)

def getTitleDict():
    titleDict = {}
    with open('./DATA/Merged/titles.txt','r') as f:
        for line in f:
            try :
                l = line.split('-')
                titleDict[int(l[0])] = l[1].strip()
            except:
                pass
    return titleDict

def getData(fileNo,tag,target):
    dirName = os.getcwd()
    dirName += '/DATA/Merged/' + tag + '/' + tag.lower() + str(fileNo) + '.txt'
    with open(dirName) as f:
        for line in f:
            try:
                if line.split(':')[0] == target:
                    return line
            except:
                pass
    return

def calScore(da):
    global championList
    data = {}
    dat = da.split(':')[1]
    dat = dat.split('|')
    i = 0
    for d in dat:
        d = d.split(',')
        data[int(d[0])] = float(1 + math.log(int(d[1]),10))
        # i+=1
        # if i>championList:
        #     break
    return data

def main():
    titleDict = getTitleDict()
    offsetDict = {'Title':{},'Body':{},'Category':{},'Links':{},'Infobox':{},'References':{}}
    weightQuery = {'Title':3,'Body':1,'Category':2,'Links':1,'Infobox':2,'References':2}
    tagDict = {'T':'Title','B':'Body','C':'Category','L':'Links','I':'Infobox','R':'References'}
    for word in offsetDict:
        offsetDict[word] = createWordBnry(word)

    while True:
        try:
            query = raw_input("Type Query Here : ")
            Stime = time.time()
            query = query.split()
            scoreDict = defaultdict(float)
            for word in query:
                if re.search(r'[T|B|C|L|I|R]:',word[:2]):
                    wo = word.split(':')
                    woRd = dictModule(wo[1].lower()).keys()[0]
                    try:
                        fileNo = bnry(1,len(offsetDict[tagDict[wo[0]]]),woRd,offsetDict[tagDict[wo[0]]])
                        da = getData(fileNo,tagDict[wo[0]],woRd)
                        data = calScore(da)
                        for d in data:
                            scoreDict[d] += float(data[d])*float(weightQuery[tagDict[wo[0]]])
                    except Exception , e:
                        print(e)
                        pass
                else:
                    try :
                        woRd = dictModule(word.lower()).keys()[0]
                        for w in offsetDict:
                            try:
                                fileNo = bnry(1,len(offsetDict[w]),woRd,offsetDict[w])
                                da = getData(fileNo,w,woRd)
                                data = calScore(da)
                                for d in data:
                                    scoreDict[d] += float(data[d])*float(weightQuery[w])
                            except Exception , e:
                                print(e)
                                pass
                    except:
                        pass
                    #print(scoreDict)
            sorted_x = sorted(scoreDict.items(), key=operator.itemgetter(1))[::-1]
            print(sorted_x[:10])
            resultCo = 0
            for i in range(len(sorted_x[:])):
                ind = (sorted_x[i][0])
                try :
                    print(titleDict[ind])
                    resultCo += 1
                except:
                    pass
                if resultCo >= 10:
                    break
            print(time.time()-Stime)
        except KeyboardInterrupt,SystemExit:
            print("Good Bye!")
            break
        #break

main()
