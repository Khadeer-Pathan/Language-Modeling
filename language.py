"""
Language Modeling Project
Name: Pathan Khadeer Ahmed Khan
Roll No: 2022501003
"""

import language_tests as test

project = "Language" # don't edit this

### WEEK 1 ###

'''
loadBook(filename)
#1 [Check6-1]
Parameters: str
Returns: 2D list of strs
'''
def loadBook(filename):
    f = open(filename, "r")
    lines = f.read()
    line = lines.split("\n")
    corpus = []
    for row in line:
        if row != "":
            col = row.split(" ")
            corpus.append(col)
    f.close()
    return corpus


'''
getCorpusLength(corpus)
#2 [Check6-1]
Parameters: 2D list of strs
Returns: int
'''
def getCorpusLength(corpus):
    # corpuslength = 0
    # for i in corpus:
    #     for j in i:
    #         corpuslength +=1
    corpuslength = sum([len(i) for i in corpus])
    return corpuslength


'''
buildVocabulary(corpus)
#3 [Check6-1]
Parameters: 2D list of strs
Returns: list of strs
'''
def buildVocabulary(corpus):
    unigramslist = []
    # for i in corpus:
    #     for j in i:
    #         if j not in unigramslist:
    #             unigramslist.append(j)
    # sorted(unigramslist)
    [unigramslist.append(j) for i in corpus for j in i if j not in unigramslist]
    return unigramslist


'''
countUnigrams(corpus)
#4 [Check6-1]
Parameters: 2D list of strs
Returns: dict mapping strs to ints
'''
def countUnigrams(corpus):
    unigramsdict = {}
    for i in corpus:
        for j in i:
            if j not in unigramsdict:
                unigramsdict[j] = 1
            else:
                unigramsdict[j] += 1
    
    return unigramsdict


'''
getStartWords(corpus)
#5 [Check6-1]
Parameters: 2D list of strs
Returns: list of strs
'''
def getStartWords(corpus): 
    getstartwordslist = []
    [getstartwordslist.append(i[0]) for i in corpus if i[0] not in getstartwordslist]
    return getstartwordslist


'''
countStartWords(corpus)
#5 [Check6-1]
Parameters: 2D list of strs
Returns: dict mapping strs to ints
'''
def countStartWords(corpus):
    getstartwordslist = getStartWords(corpus)
    tempstartlist = [i[0] for i in corpus]
    countstartwordsdict = {}
    for i in getstartwordslist:
        countstartwordsdict[i] = tempstartlist.count(i)
    return countstartwordsdict


'''
countBigrams(corpus)
#6 [Check6-1]
Parameters: 2D list of strs
Returns: dict mapping strs to (dicts mapping strs to ints)
'''
def countBigrams(corpus):
    countbigramsdict = {}
    for i in range(len(corpus)):
        for j in range(len(corpus[i])-1):
            v1,v2 = corpus[i][j], corpus[i][j+1]
            # print(v1, v2)
            if v1 not in countbigramsdict:
                countbigramsdict[v1] = {}
                if v2 not in countbigramsdict[v1]:
                    countbigramsdict[v1][v2] = 1
            else:
                if v2 not in countbigramsdict[v1]:
                    countbigramsdict[v1][v2] = 1
                else:
                    countbigramsdict[v1][v2] += 1

    return countbigramsdict


### WEEK 2 ###

'''
buildUniformProbs(unigrams)
#1 [Check6-2]
Parameters: list of strs
Returns: list of floats
'''
def buildUniformProbs(unigrams):
    uniformproblist = []
    [uniformproblist.append(1/len(unigrams)) for i in unigrams]
    return uniformproblist


'''
buildUnigramProbs(unigrams, unigramCounts, totalCount)
#2 [Check6-2]
Parameters: list of strs ; dict mapping strs to ints ; int
Returns: list of floats
'''
def buildUnigramProbs(unigrams, unigramCounts, totalCount):
    unigramproblist = []
    for i in range(len(unigrams)):
        if unigrams[i] in unigramCounts:
            unigramproblist.append(unigramCounts[unigrams[i]]/totalCount)
        else:
            unigramproblist.append(0)
    return unigramproblist


'''
buildBigramProbs(unigramCounts, bigramCounts)
#3 [Check6-2]
Parameters: dict mapping strs to ints ; dict mapping strs to (dicts mapping strs to ints)
Returns: dict mapping strs to (dicts mapping strs to (lists of values))
'''
def buildBigramProbs(unigramCounts, bigramCounts):
    bigramprobsdict = {}
    wlst = []
    plst = []
    for i in bigramCounts:
        wlst.append([key for key in bigramCounts[i].keys()])
        plst.append([value/unigramCounts[i] for value in bigramCounts[i].values()])
        for j in range(len(wlst)):
            tempdict = {"words":wlst[j],"probs":plst[j]}
        bigramprobsdict[i] = tempdict
    return bigramprobsdict


'''
getTopWords(count, words, probs, ignoreList)
#4 [Check6-2]
Parameters: int ; list of strs ; list of floats ; list of strs
Returns: dict mapping strs to floats
'''
def getTopWords(count, words, probs, ignoreList):
    # print(count); print(words); print(probs), print(ignoreList)
    tempdict = {words[i]:probs[i] for i in range(len(words))}
    sortedtempdict = {k:v for k,v in sorted(tempdict.items(), key=lambda v:v[1], reverse=True)}
    topwordsdict = {}
    for k in sortedtempdict:
        if k not in ignoreList:
            if len(topwordsdict)<count:
                topwordsdict[k] = sortedtempdict[k]
    return topwordsdict


'''
generateTextFromUnigrams(count, words, probs)
#5 [Check6-2]
Parameters: int ; list of strs ; list of floats
Returns: str
'''
from random import choices
def generateTextFromUnigrams(count, words, probs):
    sentenceswithunigrams = ""
    for i in range(count):
        sentenceswithunigrams = sentenceswithunigrams + choices(words, weights=probs)[0] + " "
    # print(sentenceswithunigrams)
    return sentenceswithunigrams


'''
generateTextFromBigrams(count, startWords, startWordProbs, bigramProbs)
#6 [Check6-2]
Parameters: int ; list of strs ; list of floats ; dict mapping strs to (dicts mapping strs to (lists of values))
Returns: str
'''
def generateTextFromBigrams(count, startWords, startWordProbs, bigramProbs):
    # print(count); print(startWords); print(startWordProbs); 
    # print(bigramProbs)
    sentenceswithbigrams = ""
    tstr = ""
    for j in range(count):
        if tstr == "" or tstr == ".":
            tstr = choices(startWords, weights=startWordProbs)[0]
            sentenceswithbigrams = sentenceswithbigrams + tstr + " "
        else:
            tstr = choices(bigramProbs[tstr]["words"], weights=bigramProbs[tstr]["probs"])[0]
            sentenceswithbigrams = sentenceswithbigrams + tstr + " "
    # print(sentenceswithbigrams)
    return sentenceswithbigrams


### WEEK 3 ###

ignore = [ ",", ".", "?", "'", '"', "-", "!", ":", ";", "by", "around", "over",
           "a", "on", "be", "in", "the", "is", "on", "and", "to", "of", "it",
           "as", "an", "but", "at", "if", "so", "was", "were", "for", "this",
           "that", "onto", "from", "not", "into" ]

'''
graphTop50Words(corpus)
#3 [Hw6]
Parameters: 2D list of strs
Returns: None
'''
def graphTop50Words(corpus):
    uniqueWords = buildVocabulary(corpus)
    unigramCounts = countUnigrams(corpus)
    length = getCorpusLength(corpus)
    unigramProbs = buildUnigramProbs(uniqueWords, unigramCounts, length)
    topwordsdict = getTopWords(50, uniqueWords, unigramProbs, ignore)
    barPlot(topwordsdict, "Probable Top 50 Words")
    return


'''
graphTopStartWords(corpus)
#4 [Hw6]
Parameters: 2D list of strs
Returns: None
'''
def graphTopStartWords(corpus):
    startWords = getStartWords(corpus)
    startWordCounts = countStartWords(corpus)
    length = getCorpusLength(corpus)
    startWordProbs = buildUnigramProbs(startWords, startWordCounts, length)
    topstartwordsdict = getTopWords(50, startWords, startWordProbs, ignore)
    barPlot(topstartwordsdict, "Probable 50 Top Start Words")
    return


'''
graphTopNextWords(corpus, word)
#5 [Hw6]
Parameters: 2D list of strs ; str
Returns: None
'''
def graphTopNextWords(corpus, word):
    unigramCounts = countUnigrams(corpus)
    bigramCounts = countBigrams(corpus)
    bigramProbs = buildBigramProbs(unigramCounts, bigramCounts)
    topnextwordsdict = getTopWords(10, bigramProbs[word]["words"], bigramProbs[word]["probs"], ignore)
    barPlot(topnextwordsdict, "Probable 10 Top Words")
    return


'''
setupChartData(corpus1, corpus2, topWordCount)
#6 [Hw6]
Parameters: 2D list of strs ; 2D list of strs ; int
Returns: dict mapping strs to (lists of values)
'''
def setupChartData(corpus1, corpus2, topWordCount):
    uniqueWords_1 = buildVocabulary(corpus1)
    unigramCounts_1 = countUnigrams(corpus1)
    length_1 = getCorpusLength(corpus1)
    unigramProbs_1 = buildUnigramProbs(uniqueWords_1, unigramCounts_1, length_1)
    topwordsdict_1 = getTopWords(topWordCount, uniqueWords_1, unigramProbs_1, ignore)

    uniqueWords_2 = buildVocabulary(corpus2)
    unigramCounts_2 = countUnigrams(corpus2)
    length_2 = getCorpusLength(corpus2)
    unigramProbs_2 = buildUnigramProbs(uniqueWords_2, unigramCounts_2, length_2)
    topwordsdict_2 = getTopWords(topWordCount, uniqueWords_2, unigramProbs_2, ignore)

    topwordslist = []
    [topwordslist.append(i) for i in topwordsdict_1 if i not in topwordslist]
    [topwordslist.append(i) for i in topwordsdict_2 if i not in topwordslist]    

    topwordsprobslist_1 = []
    topwordsprobslist_2 = []
    for i in topwordslist:
        if i in topwordsdict_1:
            topwordsprobslist_1.append(topwordsdict_1[i])
        else:
            topwordsprobslist_1.append(0)
        
        if i in topwordsdict_2:
            topwordsprobslist_2.append(topwordsdict_2[i])
        else:
            topwordsprobslist_2.append(0)
    
    topwordsdict = {"topWords":topwordslist, "corpus1Probs":topwordsprobslist_1, "corpus2Probs":topwordsprobslist_2}
    return topwordsdict


'''
graphTopWordsSideBySide(corpus1, name1, corpus2, name2, numWords, title)
#6 [Hw6]
Parameters: 2D list of strs ; str ; 2D list of strs ; str ; int ; str
Returns: None
'''
def graphTopWordsSideBySide(corpus1, name1, corpus2, name2, numWords, title):
    topwordsdict = setupChartData(corpus1, corpus2, numWords)
    sideBySideBarPlots(topwordsdict["topWords"], topwordsdict["corpus1Probs"], topwordsdict["corpus2Probs"], name1, name2, title)
    return


'''
graphTopWordsInScatterplot(corpus1, corpus2, numWords, title)
#6 [Hw6]
Parameters: 2D list of strs ; 2D list of strs ; int ; str
Returns: None
'''
def graphTopWordsInScatterplot(corpus1, corpus2, numWords, title):
    topwordsdict = setupChartData(corpus1, corpus2, numWords)
    scatterPlot(topwordsdict["corpus1Probs"], topwordsdict["corpus2Probs"], topwordsdict["topWords"], title)
    return


### WEEK 3 PROVIDED CODE ###

"""
Expects a dictionary of words as keys with probabilities as values, and a title
Plots the words on the x axis, probabilities as the y axis and puts a title on top.
"""
def barPlot(dict, title):
    import matplotlib.pyplot as plt

    names = []
    values = []
    for k in dict:
        names.append(k)
        values.append(dict[k])

    plt.bar(names, values)

    plt.xticks(rotation='vertical')
    plt.title(title)

    plt.show()

"""
Expects 3 lists - one of x values, and two of values such that the index of a name
corresponds to a value at the same index in both lists. Category1 and Category2
are the labels for the different colors in the graph. For example, you may use
it to graph two categories of probabilities side by side to look at the differences.
"""
def sideBySideBarPlots(xValues, values1, values2, category1, category2, title):
    import matplotlib.pyplot as plt

    w = 0.35  # the width of the bars

    plt.bar(xValues, values1, width=-w, align='edge', label=category1)
    plt.bar(xValues, values2, width= w, align='edge', label=category2)

    plt.xticks(rotation="vertical")
    plt.legend()
    plt.title(title)

    plt.show()

"""
Expects two lists of probabilities and a list of labels (words) all the same length
and plots the probabilities of x and y, labels each point, and puts a title on top.
Note that this limits the graph to go from 0x0 to 0.02 x 0.02.
"""
def scatterPlot(xs, ys, labels, title):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()

    plt.scatter(xs, ys)

    # make labels for the points
    for i in range(len(labels)):
        plt.annotate(labels[i], # this is the text
                    (xs[i], ys[i]), # this is the point to label
                    textcoords="offset points", # how to position the text
                    xytext=(0, 10), # distance from text to points (x,y)
                    ha='center') # horizontal alignment can be left, right or center

    plt.title(title)
    plt.xlim(0, 0.02)
    plt.ylim(0, 0.02)

    # a bit of advanced code to draw a y=x line
    ax.plot([0, 1], [0, 1], color='black', transform=ax.transAxes)

    plt.show()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":
    # test.testLoadBook()
    # test.testGetCorpusLength()
    # test.testBuildVocabulary()
    # test.testCountUnigrams()
    # test.testGetStartWords()
    # test.testCountStartWords()
    # test.testCountBigrams()

    # print("\n" + "#"*15 + " WEEK 1 TESTS " +  "#" * 16 + "\n")
    # test.week1Tests()
    # print("\n" + "#"*15 + " WEEK 1 OUTPUT " + "#" * 15 + "\n")
    # test.runWeek1()

    ## Uncomment these for Week 2 ##
    # test.testBuildUniformProbs()
    # test.testBuildUnigramProbs()
    # test.testBuildBigramProbs()
    # test.testGetTopWords()
    # test.testGenerateTextFromUnigrams()
    # test.testGenerateTextFromBigrams()

    # print("\n" + "#"*15 + " WEEK 2 TESTS " +  "#" * 16 + "\n")
    # test.week2Tests()
    # print("\n" + "#"*15 + " WEEK 2 OUTPUT " + "#" * 15 + "\n")
    # test.runWeek2()


    ## Uncomment these for Week 3 ##
    print("\n" + "#"*15 + " WEEK 3 OUTPUT " + "#" * 15 + "\n")
    test.runWeek3()
    # test.testSetupChartData()