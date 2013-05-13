#   Project 2 for COMP10001
#   Author: Lucas Berezy - 588236
#
#   Content based video search and statistics 'system'.
#
#   The spec and test cases being updated every 5 minutes before the due date
#   made this project extra fun.


import matplotlib
matplotlib.use('Svg')
from pylab import * # because using python like matlab is awlways fun
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

    2.  Dictionary of words with value as total number of videos containing
        word in description.
        i.e.    {'word': total_occurance, __TOTAL__: total_docs_in_collection}

    Each dictionary contains a __TOTAL__ entry containing the sum total of
    the other freq/total values in that dictionary or total documents in
    collection. videoURL is a composition of videoID and start time.'''

    csv_file = open(datafile, "rb")
    data = csv.reader(csv_file)
    
    first_dict  = {}
    second_dict = defaultdict(int)  # for incrementing

    for line in data:
        videoID     = line[0]   # video ID is first element
        start_time  = line[1]   # start time is second element
        description = line[-1]  # description text is last element
        videoURL    = make_videoURL(videoID, start_time)    # compose videoURL
        words       = [strip_punct(word) for word in description.split()]
        
        if videoURL not in first_dict:   # set up a new sub-dict for new doc
            first_dict[videoURL] = defaultdict(int)

        for word in words:    # for first_dict
            first_dict[videoURL][word] += 1 # fill {word: freq} dict.
            first_dict[videoURL]['__TOTAL__'] += 1
    csv_file.close()

    # kinda slow, but I'm tired and lazy
    for document in first_dict:
        for word in first_dict[document]:
            if word == '__TOTAL__':
                continue
            second_dict[word] += 1
        second_dict['__TOTAL__'] += 1

    # write out picklefile
    output = open(picklefile, "wb")
    pickle.dump(first_dict, output)
    pickle.dump(second_dict, output)
    output.close()
    return

#def word_frequency(word, word_string):
#   '''Returns the integer number of occurances of a word in a split string.'''
#    return int(word_string.split().count(word))

def make_videoURL(videoID, start_time, \
    baseURL  = 'http://www.youtube.com/watch?v='):
    '''Composes videoID and start time into videoURL. Default: youtube.'''

    return '{}{}#t={}s'.format(str(baseURL),str(videoID), str(start_time))

def strip_punct(word):
    '''Returns word with punctuation (',.:;!?-'"()[]{}') stripped from
    left and right of word, retaining any punctuation in the middle.'''

    __PUNCT__ = ''',.:;!?-'"()[]{}'''
    return word.lower().rstrip(__PUNCT__).lstrip(__PUNCT__)


def word_freq_graph(index_fname,graph_fname,word):
    '''Generates a histogram of a given word's frequency in index_fname'''
    
    picklefile = open(index_fname, "rb")
    tf = pickle.load(picklefile)
    picklefile.close()

    word = strip_punct(word)
    # return a list containing frequency of word found in description for
    # each document only if frequency > 0.
    x = [tf[doc][word] for doc in tf]
    #if x == []:   # handle word-not-found
    #    return None
    # matplotlib stuff - plot, label and save
    yscale('log')   
    xlim(0, max(x)+1) #FIX THIS
    hist(x, bins = max(x)+1)
    title('Histogram of "{}" frequencies in video description'.format(word))
    xlabel('Frequency of "{}" in descriptions for a given video'.format(word))
    ylabel('Number of videos')
    savefig(graph_fname)    # does savefig do its own file opening/closing?
    return


def single_word_search(index_fname,word):
    '''From index pickle file and a search word, returns a list of video URLs
    ranked in decrecing order of 'relevance score'. In the case of score ties,
    the video URLs are sorted in increasing lexicographic order. The relevance
    score is defined in the local score function.'''

    def score(f_dt, f_d):
        '''Frequency of term in document/total words in document.'''

        return f_dt/float(f_d)

    picklefile = open(index_fname, "rb")
    tf = pickle.load(picklefile)    # load first dictionary from pickle
    picklefile.close()

    results = []
    word = strip_punct(word)
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
    # peel off list of video URLs with rank > 0
    results = [x[1] for x in results if x[0] > 0]
    return results

def search(index_fname,query):
    '''Searches index_fname with words in query string and returns an ordered
    list of video URLs ranked in decreasing order of weighted 
    'relevance score'. In the case of score collisions, items are sub-ranked by
    video URL. Only videos with non-zero relevance scores are included in 
    returned list.'''

    def calc_wdt(word):
        '''Calculates relevance score (w_dt) for a term as per the 
        specification. On that, tf and df
        can be accessed due to the scope of this function declaration without
        supplying it as a function argument, but that just gets confusing.'''

        result = 0
        if word in tf[document]:
            f_dt = tf[document][word]   # frequency of word in document
            f_d  = tf[document]['__TOTAL__']    # total freq. of words in doc
            # number of documents in collection containing word
            # go go last minute spec changes, making my life easier and stuff!
            #f_t  = sum(1 for doc in tf if str(word) in tf[doc])
            f_t  = df[word]
            result = float(f_dt) / f_d * math.log(float(N) / (f_t + 1))
        return result

    pickle_file =  open(index_fname, "rb")
    tf = pickle.load(pickle_file)   # 1st dictionary (with sub-dicts)
    df = pickle.load(pickle_file)   # 2nd dictionary
    pickle_file.close()

    query_words = [strip_punct(x) for x in query.split()]
    results = []    # sorted list of 0 videoURLs

    # if there are no applicable query words
    if len(query_words) == 0:
        return results  # a list of no videos, ranked by no rank

    # total number of documents in collection minus __TOTAL__ entry
    N = df['__TOTAL__']
    for document in tf: # compute the document score
        # sum of relevance score for each term in query
        sum_wdt = sum(calc_wdt(word) for word in query_words)
        # sum squares of relevance values
        sum_square_wdt = \
        sum(calc_wdt(word)**2 for word in query_words)
        if sum_wdt > 0:
            # score each document
            score = float(sum_wdt)/math.sqrt(sum_square_wdt)
            results.append((score,document))

    # sort by document (videoURL) (Tuple index 1)
    results.sort(key = itemgetter(1))    
    # then reverse sort by score (Tuple index 0)
    results.sort(key = itemgetter(0) , reverse=True)
    # peel off list of video URLs with rank > 0
    results = [x[1] for x in results if x[0] > 0]
    return results

def rr(query,doc_ranking,qrels):
    ''' Given a query string, a ranked list of documents and a query-relation
    file, returns the reciprocal-rank of a the ranked list of documents.'''

    qrels_file = open(qrels, "rb")
    qrels_csv = csv.reader(qrels_file)
    

    qrels_dict = defaultdict(list)

    # build dictionary of lists for each query string in qrel file
    for line in qrels_csv:
        q_string = line[0]
        videoID = line[1]
        start_time = line[2]
        videoURL = make_videoURL(videoID, start_time)
        qrels_dict[q_string].append(videoURL) # should preserve ordering
    qrels_file.close()

    result = 0
    for doc in doc_ranking:
        if query not in qrels_dict: # return 0.0 if query not found
            break
        if doc in qrels_dict[query]: # qrel match found!
            result += 1
            break
        result += 1 # increment the rank and keep searching

    if result > 0:
        return float(1)/result
    return 0    # test harness doesn't like 0.0

def batch_evaluate(index_fname, queries, qreal, output_fname):
    ''' Generates a/an HTML page containing a table of (query, number of 
        results returned, reciprocal-rank (and mean)), a bar graph of the
        reciprocal-rank for each query and a bar graph of mean-reciprocal-rank
        for queries of different length.'''
    def html_document(body, title = ''):
        '''Returns an html template string and inserts body/title into it.'''
        
        DOC_TEMPLATE =   """<!DOCTYPE html>
        <html>
        <head><title>{title}</title></head>
        <body>{body}</body>
        </html>"""
        return DOC_TEMPLATE.format(title = str(title), body = str(body))

    def html_row(entries):
        '''Returns html table row given list of column entries.'''
        assert type(entries) == list
        output = '<tr>\n'
        for item in entries
            output.append('<td>{item}</td>'.format(item = item))
        output.append('\n</tr>')   

    queries = [strip_punct(query) for query in queries]
    reciprocal_ranks = [] # tally RRs for averaging
    body = """<table>\n     \t<tr color="grey">\n     \t\t<th>Query</th>\n     \t\t<th>No. Results</th>\n     \t\t<th>Reciprocal Rank</th>\n     \t\t<th></th>
    \t<tr color="grey">\n     \t\t<th>Query</th>\n     \t\t<th>No. Results</th>\n     \t\t<th>Reciprocal Rank</th>\n     \t\t<th></th>
    \t\t<th>Query</th>\n     \t\t<th>No. Results</th>\n     \t\t<th>Reciprocal Rank</th>\n     \t\t<th></th>
    \t\t<th>No. Results</th>\n     \t\t<th>Reciprocal Rank</th>\n     \t\t<th></th>
    \t\t<th>Reciprocal Rank</th>\n     \t\t<th></th>
    \t\t<th></th>
    \t</tr>"""   # compose html body as string concatenation

    #now to add the rows to the table
    for query in queries:
        results = search(index_fname, query)
        num_results = len(results)
        rr = rr(query, results, qrel)
        reciprocal_ranks.append(rr)
        html_row = 
        body.append
    #add the final row with mean RR and close table

    # add in bar plot of RR for each query





    html_file = open(output_fname,"wb")
    html_file.write(html_document(body, "batch_evaluate results")) # i'm boring
    html_file.close() 
    return
