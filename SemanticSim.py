# compute the simlirity distance between the main keyword and the targeted tag using WordNet based metric.
import enchant
import os, csv, urllib, re
import numpy as np
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet
import nltk
from nltk.collocations import *

bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()


##initialization##
file_path = r'/home/samipc/Desktop/trainingSetFilter/'
dest_path = r'/media/sf_Documents/featuresMatrice/DistMeasureScores/GroundTruthTAG/'

dist_measure = ['wup', 'path', 'lch']  # similarity measures (is the word related to a given    word or not)
selectedMeasure = dist_measure[2]

words = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 'dog', 'horse',
         'motorbike', 'person', 'sheep', 'sofa', 'train', 'tv']
print selectedMeasure
for c in range(0, len(words)):

    cls = words[c]
    print(cls)

    '''# Ngrams with 'creature' as a member
    creature_filter = lambda *w: 'creature' not in w
    print creature_filter
    ## Bigrams
    finder = BigramCollocationFinder.from_words(
       nltk.corpus.genesis.words('english-web.txt'))
    print(finder)
    # only bigrams that appear 3+ times
    finder.apply_freq_filter(3)
    # only bigrams that contain 'creature'
    print finder.apply_ngram_filter(creature_filter)
    # return the 10 n-grams with the highest PMI
    print finder.nbest(bigram_measures.likelihood_ratio, 10)'''

    # query the search engine using the class name to get the related terms
    terms = 'https://api.flickr.com/services/rest/?method=flickr.tags.getRelated&api_key=9a7d65ff0d5468de279ef2fc2601a115&tag=' + cls + '&format=rest'
    resp3 = urllib.urlopen(terms)
    result3 = resp3.read()
    # find words that lays between a given expression
    findAlltgs = re.findall('<tag>\w+</tag>', result3)
    flgTerms = [w.replace('<tag>', '') for w in findAlltgs]
    flgTerms = [w.replace('</tag>', '') for w in flgTerms]
  

    if cls is 'motorbike':
        cls2 = 'motorcycle'
        cls1 = wn.synset(cls2 + '.n.01')
    else:
        cls1 = wn.synset(cls + '.n.01')

    # read all the csv file in a directory 
    tg_path = file_path + cls + '/tags/'
    path, dirs, files = os.walk(tg_path).next()
    file_count = len(files)

    for t in range(1, file_count):
        file_name = tg_path + 'tag_' + str(t) + '.csv'
        file_csv = open(file_name, 'rb')
        spamreader = csv.reader(file_csv, quoting=csv.QUOTE_ALL)
        # iterate over the content of all the cvs files (word vectors)
        for row in spamreader:
            tgs = row
            dist = []  # initalize each time to you iterate because you need to make sure it is empty list
            tagC = []  # accumlate a tag list so that can be used to check for repeated words.
            for k in range(0, len(tgs)):
                tg = tgs[k]  # access the word in a tag list

                if wordnet.synsets(tg):  # check if the word is an ENglish word
                    if tg.isalnum() is True:  # avoid words with a combination of numerica and strings
                        if sorted(tg) != sorted(cls):  # skip word that is similiar to the class name.
                            if tg not in tagC:  # check for non existed words
                                if len(tg) > 2:  # check for  word length greater than 2 chars
                                    if tg in flgTerms:  # check if the given word is in a list 
                                        try:
                                            tgSim = wn.synset(tg + '.n.01')  # get the first synset in WOrdNet
                                            out = cls1.lch_similarity(tgSim)  # compute the distance
                                            dist.append(out)  # store the distance to the list
                                            tagC.append(tg)  # store the word to a tag list
                                        except:
                                            pass

            del tgs
            del spamreader
            del row

        if not os.path.exists(str(dest_path + '/' + selectedMeasure + '/')):
            os.makedirs(dest_path + '/' + selectedMeasure + '/')

        file_name = dest_path + '/' + selectedMeasure + '/' + (cls + '_Img_' + str(t) + '_RelatedTerms_TgListScore.csv')
        my_file = open(file_name, 'wb')
        wr = csv.writer(my_file, quoting=csv.QUOTE_ALL)
        wr.writerow(dist)
        wr.writerow(tagC)
        print(tagC)
        print(dist)
        del dist
        del tagC
