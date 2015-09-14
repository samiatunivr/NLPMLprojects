__author__ = 'samipc'
# Anagrams is two or more words having the same characters but ordered differetly.
# To solve this, first is to sort the characters alphebetically of the words  and then perform comparison.
# Example, give two  words, w1,w2 where w1 = 'olleh' & w2 = 'hello', if sorted(w1) is equal to sorted(w2) return
#  'words are equal' (Simple Algorithm (Y/N))

def anagram(w1,w2):
    if sorted(w1) == sorted(w2):
        print 'words are equal'
    else:
        print 'words are not FRIENDS (fight for equality)'

anagram('rac','care')
