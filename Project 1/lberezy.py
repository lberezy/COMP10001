def kinda_fermat(a,b,c):
    for n in range (2,11):
        if(a**n+b**n==c**n):
            return n
    return False
    
def unique_long_words(text,wordlen):
    '''Given a string and wordlen, returns the count of unique words in
    string that are greater than or equal to wordlen.'''
    #makes each word in text lowercase then stores each unique word as an
    #element of a set.
    words = set(word.lower() for word in (text.split()))
    count = 0
    for i in words:
        if(len(i)>=wordlen):
            count+=1
    return counteturn count