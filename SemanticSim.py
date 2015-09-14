__author__ = 'samipc'

# compute the simlirity distance between the main keyword and the targeted tag using WordNet based metric.
import enchant
import os, csv, urllib, re
import numpy as np
from nltk.corpus import wordnet as wn


##initialization##
file_path = r'/home/samipc/Desktop/trainingSetFilter/'
dest_path = r'/media/sf_Documents/featuresMatrice/DistMeasureScores/new_scores2/'

dist_measure = ['wup', 'path', 'lch'] # similarity measures (is the word related to a given    word or not)
selectedMeasure = dist_measure[0]

words = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle',	'bus',	'car',	'cat',	'chair',	'cow',	'dog',	'horse',
         'motorbike',	'person',	'sheep',	'sofa',	'train', 'tv']

for c in range(0, len(words)):

    cls = words[c]
    terms = 'https://api.flickr.com/services/rest/?method=flickr.tags.getRelated&api_key=19e853d2dd08ceca4f3d409d7ce06ab1&tag='+ cls + '&format=rest'
    resp3 = urllib.urlopen(terms)
    result3 = resp3.read()

    findAlltgs = re.findall('<tag>\w+</tag>',result3)
    flgTerms = [w.replace('<tag>', '') for w in findAlltgs]
    flgTerms = [w.replace('</tag>', '') for w in flgTerms]

    if cls is 'motorbike':
        cls2 = 'motorcycle'
        cls1 = wn.synset(cls2 + '.n.01')
    else:
        cls1 = wn.synset(cls + '.n.01')

    tg_path = file_path + cls + '/tags/'
    path, dirs, files = os.walk(tg_path).next()
    file_count = len(files)
    scores = []
    scores2 = []

    for t in range(1, file_count):
        file_name = tg_path + 'tag_' + str(t) + '.csv'
        file_csv = open(file_name, 'rb')
        spamreader = csv.reader(file_csv, quoting=csv.QUOTE_ALL)
        scores2 = []

        for row in spamreader:
            tgs = row
            dist = []
            tagC = []
            for k in range(0, len(tgs)):
                tg = tgs[k]
                d = enchant.Dict("en_US")
                chk = d.check(tg)
                if chk is True:
                    if not tg.isdigit():
                        try:

                            if tg is not cls:
                                if tg not in tagC:
                                    if tg not in flgTerms:
                                        tgSim = wn.synset(tg + '.n.01')
                                        out = cls1.wup_similarity(tgSim)
                                        dist.append(out)
                                        tagC.append(tg)
                        except:
                            pass

            del tgs
            del spamreader
            del row

            scores2.append(dist)
        if not os.path.exists(str(dest_path + '/'+ selectedMeasure + '/')):
            os.makedirs(dest_path + '/' + selectedMeasure + '/')

        file_name = dest_path + '/' + selectedMeasure + '/' + (cls + '_Img_' + str(t) + '_TgListScore.csv')
        my_file = open(file_name, 'wb')
        wr = csv.writer(my_file, quoting=csv.QUOTE_ALL)
        wr.writerow(scores2)
        print(scores2)
        del scores2

