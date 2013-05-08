#   Project 2 for COMP10001
#   Author: 588236


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

    import csv, cPickle as pickle
    from collections import defaultdict
    data = csv.reader(datafile)
    header = data.next()

    first_dict  = {defaultdict(int)}
    second_dict = defaultdict(int)  # for incrementing
    for line in data:
        videoID     = line[0]   # video ID is first element
        start_time  = line[1]   # start time is second element
        description = line[-1]  # description text is last element
        descriptions.append(description)
        videoURL    = make_videoURL(videoID, start_time)
        word_freq   = {}        # words in description and frequency

        for word in description.split():    # fill out word: freq dict.
            frequency = word_freq(word,description) # frequency of word
            word_freq[word] = frequency     # frequency for current word
            
            second_dict[word] += frequency  # add frequency in this line
        
        word_freq['__TOTAL__']  = sum(word_freq.values()) # not the best for performance
        first_dict[videoURL]    = words_freq # store video url and assoc. dict.
        
    second_dict['__TOTAL__'] = sum(second_dict.values())


    # write out picklefile
    output = open(picklefile,"w")
    pickle.dump(first_dict,output)
    pickle.dump(second_dict,output)
    output.close()

def word_freq(word, word_string):
    '''Returns the integer number of occurances of a word in a string.'''
    return int(word_string.count(word))

def make_videoURL(videoID, start_time, \
    baseURL  = 'http://www.youtube.com/watch?v='):
    '''Composes videoID and start time into videoURL. Defaults to youtube.'''
    return str(baseURL) + str(videoID) + str(start_time)

def strip_punct(word):
    '''Returns word with punctuation (',.:;!?-'"()[]{}') stripped from
    left and right of word, retaining any punctuation in the middle.'''
    __PUNCT__ = ''',.:;!?-'"()[]{}'''
    return word.lower().rstrip(__PUNCT__).lstrip(__PUNCT__)