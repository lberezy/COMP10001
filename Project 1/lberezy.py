def kinda_fermat(a,b,c):
    """Attempts to validate (non-exhaustively) Fermat's last theorem...kinda.

    Trys exponents from 2 to 10 for Fermat equality given a,b,c. Returns the
    (smallest) exponent if the equality holds, otherwise returns False.
    """

    for n in range (2,11):
        if(a**n+b**n==c**n):
            return n        # function returns n if equality holds (smallest n) 
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
    count = 0
    for i in words:             # check each word
        if(len(i)>=wordlen):    # if >= wordlen, increment total count
            count+=1
    return count



def symmetric_words(text):
    """Returns sorted list of symmetric words from given text.

    A symmetric word is one in which the outermost letter pairs are 
    equidistant across the alphabet.
    """


    def is_symmetric(word):
        """returns word if word is symmetric else returns false"""
        from string import ascii_lowercase as myalphabet # grab ascii alphabet
        word_reverse = word[::-1]
        for i in range(0,len(word)/2):
            # check
            if(not(myalphabet.find(word[i])+1) \
             == (len(myalphabet) - myalphabet.find(word_reverse[i]))):
                return False
        return word

    # makes each word in text lowercase and strips punctuation
    # then stores each unique word as a unique element of a set.
    words_symmetric = []
    words = set(strip_punc(word.lower()) for word in (text.split()))
    if words == []:
        return []
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
        vowels = 'aeiou'
        return sum(word.count(x) for x in vowels)/float(len(word))

    # makes each word in text lowercase and strips punctuation
    # then stores each unique word as a unique element of a set.
    words = [strip_punc(word.lower()) for word in text.split()]
    #words = [word for word in words if word != '']
    words = filter(None,words) # filter out null strings
    if words == []:
        return []
    min_ratio = min([vowel_ratio(word) for word in words])
    result = \
    [word for word in words if vowel_ratio(word) == min_ratio]
    result.sort()
    return result