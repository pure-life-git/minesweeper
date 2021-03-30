# - - - - - - - - - - - - - - - - - - - - - - #
# theo goodman                                #
# thrgoodm@ucsc.edu                           #
# programming assignment 5                    #
# - - - - - - - - - - - - - - - - - - - - - - #
# given a positive number from the user, this #
# program lists all prime numbers less than   #
# or equal to the number                      #
# - - - - - - - - - - - - - - - - - - - - - - #

# creates an array with true and false values
# corresponding to whether the index is a prime
# or composite number
def makeSieve(n):
    s = [True for i in range(n+1)]
    s[0] = False
    s[1] = False
    p=2
    while p**2 <= n:
        if s[p] == True:
            for i in range(p*2, n+1, p):
                s[i] = False
        
        p += 1
        
    return s

# Takes the boolean list returned by makeSieve and creates a list with the corresponding prime indices
def getPrimes(n):
    p = []
    s = makeSieve(n)
    # checks each value in the returned list and appends the index if it is true
    for i in range(n+1):
        if s[i] == True:
            p.append(i)
    #print(p)
    return p

if __name__=='__main__':
    print()
    num = int(input('Enter a positive integer: '))
    if num <= 0:
        positive = False
        while positive == False:
            num = int(input('Please enter a positive integer: '))
            if num > 0:
                positive = True
    print()
    p = getPrimes(num)
    print('There are', len(p), 'prime numbers less than or equal to', str(num) +':')
    print()
    if len(p) >= 1:
        for i in range(len(p)):
            print(p[i], end=' ')
            if (i+1) % 10 == 0 and i != 0:
                print('\n', end='')
        print()
    print()