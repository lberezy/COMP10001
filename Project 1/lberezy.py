def kinda_fermat(a,b,c):
    """Attempts to validate (non-exhaustively) Fermat's last theorem...kinda_
    Trys exponents from 2 to 10 for Fermat equality given a,b,c. Returns the
    exponent if the equality holds, otherwise returns False."""

    for n in range (2,11):
        if(a**n+b**n==c**n):
            return n        #function returns n if equality holds (smallest n) 
    return False

def strip_punc(word):
    """Function used to strip given set of punctuation from right of word"""

    punc = """,.:;!?'"-"""      #punctuation to strip (as per requirement)
    return word.rstrip(punc)    #strip punc from right until alphabet character

    
def unique_long_words(text,wordlen):
    """Returns the count of unique words in
    string that are greater than or equal to wordlen."""

    #makes each word in text lowercase and strips punctuation
    #then stores each unique word as a unique element of a set.
    words = set(strip_punc(word.lower()) for word in (text.split()))
    count = 0
    for i in words:             #check each word
        if(len(i)>=wordlen):    #if >= wordlen, increment total count
            count+=1
    return count

def is_symmetric(word):
    """returs word if word is symmetric else returns false"""
    for i in range(len(word)/2+1):
        #if(not(word[i]==alphabet[i] && word[::-])): #extend this function

def symmetric_words(text):
    """Returns sorted list of symmetric words from given text. A symmetric
    word is one in which the outermost letter pairs are equidistant across
    the alphabet."""

    #makes each word in text lowercase and strips punctuation
    #then stores each unique word as a unique element of a set.
    from string import ascii_lowercase #why not
    alphabet = ascii_lowercase
    words = set(strip_punc(word.lower()) for word in (text.split()))
    for word in words:
        for i in range(len(word)/2+1):
            if(not(word[i]==alphabet[i] && word[::-]))

    return


def least_vowel_words(text):
    """Returns sorted list whose elements satisfy the condition of having
    the lowest vowel proportion of all the words in the given text."""

    #makes each word in text lowercase and strips punctuation
    #then stores each unique word as a unique element of a set.
    words = set(strip_punc(word.lower()) for word in (text.split()))
    return