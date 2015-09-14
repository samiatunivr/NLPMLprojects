__author__ = 'samipc'

# given words download a set of predefined images and their corresponding tag lists. The script searches FLICK for images u
# using a single or a compound query and return n images.
import urllib
import cStringIO
import string
import re
import os
import csv
from PIL import Image
from stop_words import get_stop_words

numpages = 10

file_path = r'/home/samipc/Desktop/Flickr/'
save_name = 'img_'

words = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 'dog', 'horse',
         'motorbike', 'person', 'sheep', 'sofa', 'train', 'tv']  # keywords to be downloaded

cachedStopWords = get_stop_words('english') # get the stop words so that we can avoid to have them in our class dict

print'Downloading... \n '

for k in range(0, len(words)):
    word = words[k]
    print(word)

    counter = 1
    key_path1 = file_path + '/' + word + '/imgs'
    key_path2 = file_path + '/' + word + '/tags'
    if not os.path.exists(str(key_path1)):
        os.makedirs(key_path1)
    if not os.path.exists(str(key_path2)):
        os.makedirs(key_path2)

    link3 = ' https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=9a7d65ff0d5468de279ef2fc2601a115&tags=' + word + '&per_page=500&sort=relevance&tag_mode=all';
    resp = urllib.urlopen(link3)
    result = resp.read()
    pages = re.findall(r'pages="\d+"', result) # do some search here (search for number of pages)
    pg = pages[0].replace('"', '')
    pg = pg.replace('pages=', '') # cool, found & replace a pattern with empty   holes   so you can fit it.
    if numpages > pg:
        numpages = pg
    if numpages < pg:
        for p in range(1, 9):
            link = 'https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=9a7d65ff0d5468de279ef2fc2601a115&tags='+word+'&page='+str(p)+'&per_page=500&format=rest&sort=relevance&tag_mode=all'
            resp2 = urllib.urlopen(link)
            result2 = resp2.read()
            ids = re.findall(r'photo id="\d+"', result2)

            # get all the ids of the images for a given a keyword
            all_ids = []
            for i in range(0, len(ids)):
                out = string.replace(ids[i],'photo id="', '')
                out = string.replace(out, '"', '')
                all_ids.append(out)

           # get the info of each image using its id.
            all_ids = list(set(all_ids))
            urls = []

            for j in range(0, len(all_ids)):
                try:
                    im_id = all_ids[j]
                    link2 = 'https://api.flickr.com/services/rest/?method=flickr.photos.getSizes&api_key=9a7d65ff0d5468de279ef2fc2601a115&photo_id=' + str(
                        im_id)
                    link3 = 'https://api.flickr.com/services/rest/?method=flickr.photos.getInfo&api_key=9a7d65ff0d5468de279ef2fc2601a115&photo_id=' + str(
                        im_id) + '&format=rest'
                    res1 = urllib.urlopen(link3)
                    info1 = res1.read()
                    res = urllib.urlopen(link2)
                    info = res.read()
                    im_link = re.findall(r'source="[^"]+"', info) # find image urls
                    takeMe = im_link[6] # take only images with a medium size (if not exist skip (thanx to TRY function))
                    keepMe = string.replace(takeMe, 'source="', '')
                    readMe = string.replace(keepMe, '"', '')

                    if readMe:
                        im_file = cStringIO.StringIO(urllib.urlopen(readMe).read())
                        im = Image.open(im_file)
                        tags = re.findall(u'raw="\w+', info1)
                        tg_len = len(tags)
                        im.save(key_path1 + '/' + (save_name + str(counter)), 'JPEG', quality=30);
                        urls.append(readMe)
                        tgList = [];

                        # textual  word extraction (Extract only tags that satisfy the constrains: ENGLISH WORDS, NOT DIGIT, etc)
                        for t in range(0, tg_len):
                            tg_img = string.replace(tags[t], 'raw="', '')
                            tg_img = tg_img.split()
                            for wc in range(0, len(tg_img)):
                                tgc = tg_img[wc]
                                if tgc not in cachedStopWords:
                                    tgList.append(tgc.lower())
                                    del tgc
                        file_name = key_path2 + '/' + ("tag_" + str(counter) + '.csv')
                        myfile = open(file_name, 'wb')
                        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                        wr.writerow(tgList)
                        counter += 1
                        if counter >= 300:
                            break
                except:
                    pass

    fl = open(file_path + '/' + word + '/urllist.txt', 'w')
    for readMe in urls:
        fl.write(readMe + '\n')
    fl.close()
