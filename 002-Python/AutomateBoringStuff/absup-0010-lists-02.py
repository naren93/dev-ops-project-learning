# Trying to manipulate a string
name = 'Zophie a cat'
print('Name = ' + name)
try :
    name[7] = 'the'
except TypeError :
    print("'str' does not support this assignment.")

# String manipulation - 
newName = name[:7] + 'the' + name[8:]
print('New name = ' + newName)

# Tuple -
eggs = ('hello', 42, 0.5)
print(eggs)
print(eggs[0])
print(eggs[1:3])
print(len(eggs))

try:
    eggs[1]=99
except TypeError :
    print("TUPLES are IMMUTABLE LISTS")
print(type(eggs))
print(type(name))

# Conversion of type -
eggs = list(eggs)
print(eggs)
print(type(eggs))

# Reference of the list -
spam = 42
cheese = spam
spam = 100
print("The value of cheese = " + str(cheese))
print("The value of spam = " + str(spam))

spam = [0,1,2,3,4,5,6]
cheese = spam
cheese[1] = 'Hello'
print("The value of cheese = ", cheese)
print("The value of spam = ", spam)

# Passing the reference -
def eggs(list01):
    list01.append('Adding list information')

spam=[1,2,3,4]
print("Spam =", spam)
eggs(spam)
print("Unmodified spam =",spam)

# Copy Module -
import copy
spam = ['A','B','C','D']
cheese = copy.copy(spam)
cheese[1]=42
print('Spam = ', spam)
print('Cheese = ', cheese)
curd = copy.deepcopy(spam) # Usually used to copy list of lists
curd[1]=100
print('Spam = ', spam)
print('Curd = ', curd)

