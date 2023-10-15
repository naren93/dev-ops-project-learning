myCat = {
    'size' : 'fat',
    'color' : 'grey',
    'disposition' : 'loud'
}
print(myCat)
print('My cat is very', myCat['disposition'], end='. ')
print('My cat has ' + myCat['color'] + ' fur.')

spam = {
    12345 : 'Luggage combination',
    42 : 'The answer'
}

# Lists Vs Dictionaries -
spam = ['Cats', 'Dogs', 'Mouse']
bacon = ['Dogs', 'Cats', 'Mouse']
print("For Lists ", spam == bacon)
eggs = {
    'name':'Zophie',
    'species':'cat',
    'age':8
}
bacon = {
    'species':'cat',
    'age':8,
    'name':'Zophie'
}
print("Dictionary ", eggs==bacon)

# Birthdays.py
birthdays = {
    'Alice':'Apr 1',
    'Bob':'Dec 12',
    'Carol':'Mar 4',
}
while False:
    print("Enter a name (blank to quit):")
    name = input()
    if name=='' :
        break;

    if name in birthdays:
        print(birthdays[name] + ' is the birthday of ' + name)
    else:
        print("I do not have the birthday information of " + name)
        print("What is their birthday ?")
        bday = input()
        birthdays[name] = bday
        print("Birthday has been updated!")

# keys(), values(), items()

spam = {
    'color':'red',
    'age':'42'
}
for v in spam.values():
    print(v)

for u in spam.keys():
    print(u)

for u,v in spam.items():
    print('Keys: '+ u + " Value: " + v)
print(spam.keys())
print(list(spam.keys()))
print(spam.items())

# Check whether a key or a value exists in a dictionary -
spam = {
    'name':'Zophie',
    'age':7
}
print('Is Name present in the dictionary - ' + str('name' in spam.keys()))
print('Is Zophie present in the dictionary - ' + str('Zophie' in spam.values()))

# Get Method -
picnicItems = {
    'apples':5,
    'cups':2
}
print('I am bringing ' + str(picnicItems.get('cups',0)) + ' cups to the picnic.')
print('I am bringing ' + str(picnicItems['cups']) + ' cups to the picnic.')
print('I am bringing ' + str(picnicItems.get('oranges',0)) + ' oranges to the picnic.')
try :
    print('I am bringing ' + str(picnicItems['oranges']) + ' oranges to the picnic.')
except KeyError:
    print("Orange is not a key.")

# Set Default values -
spam = {
    'name':'Pooka',
    'age':5
}
spam.setdefault('color', 'black')
print(spam)
spam.setdefault('color', 'white')
print(spam)

# Loops -
import pprint
message = 'It was a bright cold day in April, and the clocks were striking thirteen.'
count = {}
for character in message:
    count.setdefault(character, 0)
    count[character] = count[character] + 1
print(count)
pprint.pprint(count)
