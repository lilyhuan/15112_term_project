#file for category processing, finding words related to a category,
#and graphical analysis
import nltk as n
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
#wordnet information from https://www.cs.princeton.edu/courses/archive/fall06/cos226/assignments/wordnet.html


#lemma information from https://www.datacamp.com/community/tutorials/stemming-lemmatization-python
def findSynonyms(word):
    synonyms = set()
    for syn in wn.synsets(word):
        for lem in syn.lemmas():
            synonyms.add(lem.name())
    return list(synonyms)

#sentence tokenizing and tagging information from https://www.nltk.org/book/ch05.html and http://sapir.psych.wisc.edu/programming_for_psychologists/cheat_sheets/Text-Analysis-with-NLTK-Cheatsheet.pdf
def tagWord2(sentence):
    d = {"NN":"n", "VB":"v"}
    tokens = n.word_tokenize(sentence)
    tagged = n.pos_tag(tokens)
    simplePOSTag = []
    for (word, pos) in tagged:
        simplePOS = d[pos]
        simplePOSTag.append((word, simplePOS))
    return simplePOSTag

#sentence tokenizing and tagging information from https://www.nltk.org/book/ch05.html
def relatedWord(word, category):
    tagged = tagWord2(word)
    searchWords = []
    for (word, pos) in tagged:
        searchWords.append(word + "." + pos + ".01")
    for categ in category:
        synset = set(wn.synsets(categ))
        for syn in synset:
            for searchWord in searchWords:
                print(searchWord)
                try:
                    word = wn.synset(searchWord)
                    common = syn.lowest_common_hypernyms(word)
                    for i in range(len(common)):
                        if common != []:
                            if common[i].name() == syn.name():
                                return categ
                        else:
                            break
                except:
                    continue

def wordsInCategory(category):
    sets = wn.synsets(category)
    checkSet = sets[0]
    names = checkSet.hyponyms()
    nameResult = []
    for name in names:
        nameResult.append(name.name())
    result = set()
    for item in nameResult:
        stopPoint = item.index(".")
        result.add(item[:stopPoint])
    return sorted(result)

#word nets and lemma information from https://www.nltk.org/book/ch02.html
def cleanList(lst): #cleans list, removes articles, punctuation
    removePOS = {"DT", "IN", "EX", "TO", "PDT", "PRP", "PRP$", "CC"}
    stopWords = set(stopwords.words("english"))
    result = []
    lem = WordNetLemmatizer()
    for (word, pos) in lst:
        if pos not in removePOS:
            if word.isalpha():
                if word not in stopWords:
                    lower = word.lower()
                    lemmatized = lem.lemmatize(lower)
                    result.append(lemmatized)
    return result

def countWords(lst):
    d = dict()
    for word in lst:
        if word in d:
            d[word] += 1
        else:
            d[word] = 1
    return d

#vader sentiment information from https://medium.com/analytics-vidhya/simplifying-social-media-sentiment-analysis-using-vader-in-python-f9e6ec6fc52f
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import numpy as np
#sentiment command information from http://www.nltk.org/howto/sentiment.html

def makeDict(lst): #for frequency graph
    d = dict()
    for word in lst:
        if word in d:
            d[word] += 1
        else:
            d[word] = 1
    return d

def dictToTuple(dict): #for frequency graph
    result = []
    for key in dict:
        result.append((dict[key], key))
    return result

def cleanTextStr(str):
    stopWords = set(stopwords.words("english"))
    cleanList = []
    tokens = n.word_tokenize(str)
    for word in tokens:
        if word not in stopWords:
            if word.isalpha():
                cleanList.append(word.lower())
    return cleanList

# numpy array information from https://likegeeks.com/numpy-array-tutorial/
def mostFrequentWordsGraph(lst):
    masterLst= []
    for item in lst:
        masterLst.extend(n.word_tokenize(item))
    taggedLst = n.pos_tag(masterLst)
    cleanLst = cleanList(taggedLst)
    wordDict = makeDict(cleanLst)
    tupleList = dictToTuple(wordDict)
    finalTupList = sorted(tupleList)[::-1]
    x = np.array([])
    y = np.array([])
    my_xticks = []
    xCount = 1
    for i in range(0, 10): #finalTupList
        num = finalTupList[i][0]
        word = finalTupList[i][1]
        y = np.append(y, [num])
        x = np.append(x, [xCount])
        xCount += 1
        my_xticks.append(word)
    return(x, y, my_xticks)

#returns dictionary: each sentence is key, maps to sentiment
#takes in list of entries ie ["A sentence.", "A multi. Sentence."]
#sentiment command information from http://www.nltk.org/howto/sentiment.html
def sentimentAnalysis(lst):
    masterLst = []
    for elem in lst:
        sentences = n.sent_tokenize(elem)
        masterLst.extend(sentences)
    SIA = SentimentIntensityAnalyzer()
    result = dict()
    for sentence in masterLst:
        score = SIA.polarity_scores(sentence)
        result[sentence] = score["compound"]
    return result

def sentimentGraph(paragraph):
    dictOfScore = sentimentAnalysis(paragraph)
    x = np.array([])
    y = np.array([])
    xNum = 1
    for key in dictOfScore:
        x = np.append(x, [xNum])
        xNum += 1
        y = np.append(y, [(dictOfScore[key])])
    return(x, y)

#Graph details from https://matplotlib.org/users/pyplot_tutorial.html#working-with-multiple-figures-and-axes
def graphAll(lst):
    plt.figure(1)
    plt.subplot(211)
    (x, y, my_xticks) = mostFrequentWordsGraph(lst)
    plt.xticks(x, my_xticks, rotation=45)
    plt.plot(x, y)
    plt.title("10 Most Frequent Words")
    plt.xlabel("Words")
    plt.ylabel("Count")
    plt.tight_layout()

    plt.subplot(212)
    (sx, sy) = sentimentGraph(lst)
    plt.plot(sx,sy)
    plt.title("Sentiment Analysis")
    plt.xlabel("Sentence Number")
    plt.ylabel("Degree of Sentiment")
    plt.tight_layout()

    plt.show()

