def kinda_fermat(a,b,c):
    """Attempts to validate (non-exhaustively) Fermat's last theorem...kinda.

    Trys exponents from 2 to 10 for Fermat equality given a,b,c. Returns the
    (smallest) exponent if the equality holds, otherwise returns False.
    """

    for n in range (2,11):
        if(a**n+b**n==c**n):
            return n        # function returns smallest n if equality holds 
    return False


def strip_punc(word):
    """Strips basic punctuation from right of string."""

    punc = """,.:;!?'"-"""      # punctuation to strip (as per requirement)
    return word.rstrip(punc)    # strip punc from right until alpha character

    
def unique_long_words(text,wordlen):
    """Counts words in text that are greater than or equal to wordlen."""

    # makes each word in text lowercase and strips punctuation
    # then stores each unique word as a unique element of a set.
    words = set(strip_punc(word.lower()) for word in (text.split()))
    count = 0   # current count of words >= wordlen
    for i in words:
        if(len(i)>=wordlen):
            count+=1
    return count
    # or in one line for those interested:
    #def func(text,wordlen):return len(filter(lambda x: len(x)>=wordlen,\
    #set(word.lower().rstrip(""",.:;!?'"-""") for word in text.split())))
    # and there's probably a more concise way too, but I don't know python well


def symmetric_words(text):
    """Returns sorted list of symmetric words from given text.

    A symmetric word is one in which the outermost letter pairs are 
    equidistant across the alphabet.
    """

    def is_symmetric(word):
        """returns word if word is symmetric else returns false"""
        from string import ascii_lowercase as myalphabet # grab ascii alphabet
        word_reverse = word[::-1]       # a reversed copy will come in handy
        # iterate over each letter in word up to half way point
        for i in range(0,len(word)/2):
            # returns false if symmetric property doesn't hold
            # note the +1 and len() hackishness to help with 0-index list
            if(not(myalphabet.find(word[i])+1) \
             == (len(myalphabet) - myalphabet.find(word_reverse[i]))):
                return False
        return word

    # makes each word in text lowercase and strips punctuation
    # then stores each unique word as a unique element of a set.
    words_symmetric = []       # where the words will be put
    words = set(strip_punc(word.lower()) for word in (text.split()))
    if words == []:
        return []   # handle empty list early
    for word in words:
        if(is_symmetric(word)):
            words_symmetric.append(word)
    words_symmetric.sort()
    return words_symmetric


def least_vowel_words(text):
    """Returns sorted list whose elements satisfy the condition of having
    the lowest vowel proportion of all the words in the given text.

    The algorithm used is not computationally efficient and can be improved,
    but computing power is cheap.
    """

    def vowel_ratio(word):
        '''Calculates vowel ('aeiou') ratio of string as float.'''

        vowels = 'aeiou'    # check for English vowels
                            # could import locale and do it that way...
                            # don't trust IVLE enough
        # sums the number of vowels in the word, divides by len(word)
        # division by zero (should be) already handled by this stage
        return sum(word.count(x) for x in vowels)/float(len(word))

    # makes each word in text lowercase and strips punctuation
    # then stores each unique word as a unique element of a set.
    words = [strip_punc(word.lower()) for word in text.split()]
    words = filter(None,words) # filter out null strings
    if words == []:
        return []   # handle empty lists early
    # calculate minimum vowel ratio for words in the list    
    min_ratio = min([vowel_ratio(word) for word in words])
    # leave only lowest vowel ratio words
    result = \
    [word for word in words if vowel_ratio(word) == min_ratio]
    result.sort()
    return result