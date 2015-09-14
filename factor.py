__author__ = 'samipc'

#Explanantion of the algorithm

# the algorithms works by dividing a given  number leaving no reminder
# lets say we have a n  = 6, then 3 is a factor of n because 3 is exactly divided into 6(6/3 %(reminder) = 0)

# compute the factor of a given number
def factor(n):
    factors = [i for i in range(1, n+1) if n % i == 0] # the loop starts from  1 to void errors,
    return factors

print factor(6)

output = [1, 2, 3, 6]
