# the divide by 0 error -
def spam(divideby):
    try :
        return 42/divideby
    except ZeroDivisionError :
        return('Error : Invalid Argument.')

print(spam(2))
print(spam(12))
print(spam(0))
print(spam(1))

