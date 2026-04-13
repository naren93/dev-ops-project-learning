myPets = ['Zoey', 'Pooka', 'Fat-tail']
print('Enter pet name - ')
name = 'Harry'
if name not in myPets :
    print("I do not have a pet named " + name)
else :
    print(name + " is my pet." )

cat = ['fat', 'black', 'loud']
size, color, disposition = cat
print(size, color, disposition, cat)

# Augmented assignment operator -
i=1
i+=1
print(i)
i*=1
print(i)
i-=1
print(i)
i/=1
print(i)
i%=1
print(i)

# Index -
spam = ['Hello', 'Howdy', 'Hi', 'Heya']
print("Index of the word 'Hello' in the list " + str(spam.index('Hello')))
print("Index of the word 'Hi' in the list " + str(spam.index('Hi')))

# Adding values -
ham = ['cat', 'dog', 'bat']
ham.append('mouse')
print(ham)
ham.insert(1, 'chicken')
print(ham)
ham.insert(-1, 'duck')
print(ham)
ham.remove('duck')
print(ham)
try :
    ham.remove('tiger')
except ValueError :
    print("'Tiger' does not exist in list of ham.")

# List sort -
spam = [1,2,3,4,'Alice','Bob']
try :
    print(spam.sort())
except TypeError :
    print("'<' not supported between instances of 'str' and 'int'")
spam = ['Alice', 'ant', 'Bob', 'badgers', 'Carol', 'cats']
spam.sort()
print(spam)
spam=['a', 'Z', 'A', 'z']
spam.sort(key=str.lower)
print(spam)

# Magic 8 Ball -
import random
messages = ['it is certain',
            'it is decidedly so',
            'Yes definitely',
            'Reply hazey try again',
            'Ask again later',
            'Concentrate and ask again',
            'My reply is no good',
            'Outlook is not good',
            'Very doubtful']
print(messages[random.randint(0, len(messages)-1)])
