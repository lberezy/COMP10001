def kinda_fermat(a,b,c):
    for n in range (2,11):
        if(a**n+b**n==c**n):
            return n
    return False