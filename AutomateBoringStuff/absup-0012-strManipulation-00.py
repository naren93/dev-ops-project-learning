# Quote based manipulation -
spam = "That is Alice's cat."
print(spam)

# Escape sequence
spam = 'Say hi to Bob\'s mother.'
print(spam)

# String manipulated by escape sequence
print("Hello there!\nHow are you?\nI\'m doing fine.")

# Raw String -
print(r'That is Carol\'s cat.')

# Triple quotes -
print('''Dear Alice,
Eve's cat has been arrested for catnapping, cat burglary, and extortion.
Sincerely,
Bob''')

# Managing them with escape sequence -
print('Dear Alice,\n\nEve\'s cat has been arrested for catnapping, cat burglary, and extortion.\n\nSincerely,\nBob')

# Indexing and splicing -
spam = 'Hello World'
fizz = spam[:5]
print(fizz)

# In and not in operations with strings -
print(('h' in "hello"))
print(('a' in "hello"))
print(('a' not in "hello"))
print(('h' not in "hello"))

# Upper, Lower, Is Upper , Is Lower -
print(spam.upper())
print(spam.lower())

print('How are you?')
feeling = "Im feeling good"
if 'good' in feeling.lower():
    print('I feel good too.')
else:
    print('I hope the rest of your day is good.')

print(('HELLO'.isupper()))
print(('HELLO'.islower()))

# Other isX functions -
print(('hello'.isalpha()))
print(('hello123'.isalpha()))
print(('hello123'.isalnum()))
print(('hello'.isalnum()))
print(('123'.isdecimal()))
print(('     '.isspace()))
print(('This Is Title Case'.istitle()))
print(('This Is Title Case 123'.istitle()))
print(('This Is not Title Case'.istitle()))
print(('This Is NOT Title Case Either'.istitle()))

# Validate Input -
while True:
    print('Enter your age:')
    age = input()
    if age.isdecimal():
        break
    print('Please enter a number for your age.')
while True:
    print('Select a new password (letters and numbers only):')
    password = input()
    if password.isalnum():
        break
    print('Passwords can only have letters and numbers.')
