#   Project 2 for COMP10001
#   Author: Lucas Berezy - 588236
#
#   Content based video search system.


# oh look, a great big pile of imports. this is going to be fun...
import matplotlib
from pylab import *
import cPickle as pickle
import csv
from collections import defaultdict
from operator import itemgetter
import math

def make_index(datafile, picklefile):
    '''Takes a datafile containing video descriptions 'pickles' two 
    dictionaries to be stored in picklefile.

    1.  Dictionary of video URL and words in description, where words in
        description is a dictionary of the words and their integer frequencies.
        i.e.    {'videoURL': {'word': freq, __TOTAL__: total_freq}

    2.  Dictionary of words with value as total occurance of word in
        description of all videos.
        i.e.    {'word': total_occurance, __TOTAL__: total_in_all_videos}

    Each dictionary contains a __TOTAL__ entry containing the sum total of
    the other freq/total values in that dictionary. videoURL is a composition
    of videoID and start time'''


    def make_videoURL(videoID, start_time, \
        baseURL  = 'http://www.youtube.com/watch?v='):
        '''Composes videoID and start time into videoURL. Default: youtube.'''
        return '{}{}#t={}s'.format(str(baseURL),str(videoID), str(start_time))

    data = csv.reader(open(datafile,"rb"))
    
    first_dict  = {}
    second_dict = defaultdict(int)  # for incrementing

    for line in data:
        videoID     = line[0]   # video ID is first element
        start_time  = line[1]   # start time is second element
        description = line[-1]  # description text is last element
        videoURL    = make_videoURL(videoID, start_time)    # compose videoURL

        if videoURL not in first_dict.keys():   # set up a new sub-dict for new
            first_dict[videoURL] = defaultdict(int)
        
        for word in description.split():    # word frequencies 
            word = strip_punct(word)
            # not super efficient, but eh      
            first_dict[videoURL][word] += 1 # fill {word: freq} dict.
            second_dict[word] += 1
            first_dict[videoURL]['__TOTAL__'] += 1  # should increment variable
            # and store once to avoid hashing every time
                   
    second_dict['__TOTAL__'] = sum(second_dict.values())

    # write out picklefile
    output = open(picklefile,"wb")
    pickle.dump(first_dict,output)
    pickle.dump(second_dict,output)
    output.close()
    return first_dict, second_dict

#def word_frequency(word, word_string):
#   '''Returns the integer number of occurances of a word in a split string.'''
#    return int(word_string.split().count(word))



def strip_punct(word):
    '''Returns word with punctuation (',.:;!?-'"()[]{}') stripped from
    left and right of word, retaining any punctuation in the middle.'''
    __PUNCT__ = ''',.:;!?-'"()[]{}'''
    return word.lower().rstrip(__PUNCT__).lstrip(__PUNCT__)


def word_freq_graph(index_fname,graph_fname,word):
    '''Generates a histogram of a given word's frequency in index_fname'''

    matplotlib.use('Svg')
    tf = pickle.load(open(index_fname))
    word = strip_punct(word)
    # return a list containing frequency of word found in description for
    # each document only if frequency > 0.
    x = [tf[doc][word] for doc in tf.keys() if tf[doc][word] > 0]
    if x == []:   # handle word-not-found
        return None
    # matplotlib stuff - plot, label and save
    hist(x, bins = len(x))
    title('Histogram of word frequencies in video description')
    xlabel('Frequency of word in descriptions for a given video')
    ylabel('Number of videos')
    savefig(graph_fname)    # does savefig do its own file opening/closing?

def score(f_dt, f_d):
    '''Frequency of term in document/total words in document.'''
    return f_dt/float(f_d)

def single_word_search(index_fname,word):
    '''From index pickle file and a search word, returns a list of video URLs
    ranked in decrecing order of 'relevance score'. In the case of score ties,
    the video URLs are sorted in increasing lexicographic order. The relevance
    score is defined in the local score function.'''

    results = []
    tf = pickle.load(open(index_fname))
    word = strip_punct(word)
    if not word in tf:  # stop
        return []
    for document in tf:
        if word in tf[document]:
            f_dt = tf[document][word]
            f_d  = tf[document]['__TOTAL__']
            if f_d != 0:
                results.append((score(f_dt, f_d), document))
    
    # was using key = lambda x: x[0], but found out about itemgetter.
    # itemgetters are cool or something and Timsort being a stable sorting
    # algorithm is super handy too!
    
    # sort by document (videoURL) (Tuple index 1)
    results.sort(key = itemgetter(1))    
    # then reverse sort by score (Tuple index 0)
    results.sort(key = itemgetter(0) , reverse=True)
    # peel off list of video URLs
    results = [x[1] for x in results]
    return results

def search(index_fname,query):
    '''Searches index_fname with words in query string and returns an ordered
    list of video URLs ranked in decreasing order of 'relevance score'. In the
    case of score collisions, items are sub-ranked by video URL. Only videos
    with non-zero relevance scores are included in returned list.'''

    def relevance_score(tf, df):
        '''Returns w_dt as per spec.'''


        return
    results = []
    tf = pickle.load(open(index_fname))
    df = pickle.load(open(index_fname))
    query_words = [strip_punct(x) for x in query.split()]
            
    N = 0 # total number of documents in collection
    for word in query_words:
        # compute w_dt
        f_t = 0
        for document in tf:
            N += 1
            if word in tf[document]:
                f_dt = tf[document][word]
                f_d  = tf[document]['__TOTAL__']
                if f_d != 0:
                    results.append((score(f_dt, f_d), document))
    return

def rr(query,doc_ranking,qrels):
    return
