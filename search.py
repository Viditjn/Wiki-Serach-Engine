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



def main():
    offsetDict = {'T':{},'B':{},'C':{},'L':{}}
    weightQuery = {'T':4,'B':1,'C':2,'L':1}
    titleoff = {}
    for word in offsetDict:
        filename = word + '.txt'
        with open(filename,'r') as f:
            for line in f:
                l = line.split(' : ')
                offsetDict[word][l[0]] = int(l[1])
        # print(word,len(offsetDict[word]))
    # print(offsetDict[:10])
    with open('titleoff.txt','r') as f:
        for line in f:
            l = line.split()
            titleoff[l[0]] = l[1]
    # print(len(titleoff))
    while True:
        try:
            query = raw_input("Type Query Here : ")
            Stime = time.time()
            query = query.split()
            scoreDict = defaultdict(float)
            for word in query:
                if re.search(r'[T|B|C|L|I]:',word[:2]):
                    wo = word.split(':')
                    # print (wo)
                    woRd = dictModule(wo[1].lower()).keys()[0]
                    #print ("hi : ",woRd)
                    fp = open(wo[0]+'temp.txt','r')
                    try:
                        #print(offsetDict[wo[0]][woRd])
                        fp.seek(offsetDict[wo[0]][woRd])
                        data = fp.readline()
                        #print(data)
                        data = data.split(':')[1].split()
                        # print(len(data))
                        for i in range(0,len(data),2):
                            scoreDict[data[i]] += float(data[i+1])*float(weightQuery[wo[0]])
                        # print (scoreDict[data[i]])
                    except Exception , e:
                        print(e)
                        pass
                    fp.close()
                else:
                    try :
                        words = dictModule(word.lower()).keys()[0]
                        # print("hello :", words)
                        #print (scoreDict)
                        for w in offsetDict:
                            #print(w)
                            fp = open(w+'temp.txt','r')
                            try:
                                fp.seek(offsetDict[w][words])
                                data = fp.readline()
                                #print(data)
                                data = data.split(':')[1].split()
                                for i in range(0,len(data),2):
                                    scoreDict[data[i]] += float(data[i+1])*weightQuery[w]
                            except:
                                pass
                            fp.close()
                    except:
                        pass
                    #print(scoreDict)
            sorted_x = sorted(scoreDict.items(), key=operator.itemgetter(1))[::-1]
            print(sorted_x[:10])
            f = open('title.txt','r')
            resultCo = 0
            for i in range(len(sorted_x[:])):
                ind = (sorted_x[i][0])
                #print ((ind),sorted_x[i][1])
                try :
                    f.seek(int(titleoff[ind]))
                    print(f.readline().strip())
                    resultCo += 1
                except:
                    pass
                if resultCo >= 10:
                    break
            f.close()
            print(time.time()-Stime)
        except KeyboardInterrupt,SystemExit:
            print("Good Bye!")
            break
        #break

main()
