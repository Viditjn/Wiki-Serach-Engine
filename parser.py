import re
from collections import defaultdict
from Stemmer import Stemmer

stopWord = defaultdict(bool)
stopWordPath = 'Stop_words.txt'

def tokenize(txt):
    txt = re.split("[^a-zA-Z]",txt)
    txt = [word.encode('utf-8') for word in txt]
    return txt

with open(stopWordPath,'r') as stopword:
    for line in stopword:
        for w in re.split('[ , \"\n]+',line):
            if w:
                stopWord[w] = True

def stopWordRemoval(wordsList):
    temp = []
    for word in wordsList:
        if not stopWord[word]:
            temp.append(word)
    return temp

def stem(wordsList):
    stemmer = Stemmer("english")
    stemmed_word = []
    for word in wordsList:
        if word:
            stemmed_word.append(stemmer.stemWord(word))
    return stemmed_word

def createDictionary(wordsList):
    temp = defaultdict(int)
    for word in wordsList:
        temp[word]+=1
    return temp

def dictModule(txt):
    words = tokenize(txt);
    words = stem(words)
    words = stopWordRemoval(words)
    words = createDictionary(words)
    return words

def externalLinks(txt):
    links=[]
    lines = txt.split("==external links==")
    dictLink = defaultdict()
    if len(lines)>1:
        lines=lines[1].split("\n")
        for i in xrange(len(lines)):
            if '* [' in lines[i] or '*[' in lines[i]:
                word=""
                temp=lines[i].split(' ')
                word=[key for key in temp if 'http' not in temp]
                #word=' '.join(word).encode('utf-8')
                links.extend(word)
        dictLink = dictModule(' '.join(links))
    return dictLink

def findFields(txt):
    lines = txt.split("\n")
    body = []
    category = []
    info = []
    for i in xrange(len(lines)):
        if "[[category" in lines[i]:
            line = txt.split("[[category:")
            if line > 1:
                category.extend(line[1:-1])
                line = line[-1].split("]]")
                category.extend(line)

        # elif '{{infobox' in lines[i] or '{{ infobox' in lines[i] or '{{Infobox' in lines[i] or '{{ Infobox' in lines[i]:
        #     flag=lines[i].count('{{')-lines[i].count('}}')
        #     info.append(lines[i])
        #     i+=1
        #     while flag>0 and i<nlines :
        #         if '{{' in lines[i]:
        #             count=lines[i].count('{{')
        #             flag+=count
        #         if '}}' in lines[i]:
        #             count=lines[i].count('}}')
        #             flag-=count
        #         info.append(lines[i])
        #         i+=1
        #     i-=1

        else: #"[[category" not in lines[i]:
            body.append(lines[i])
    # import pdb
    # print len(category)
    # pdb.set_trace()
    category = dictModule(' '.join(category))
    body = dictModule(' '.join(body))
    info = dictModule(' '.join(body))
    return body,category,info

def titleField(txt):
    txt = txt.lower()
    return dictModule(txt)

def textTagProcessing(txt):
    txt = txt.lower()
    link = externalLinks(txt)
    body, category, info = findFields(txt)
    return link, body, category, info
