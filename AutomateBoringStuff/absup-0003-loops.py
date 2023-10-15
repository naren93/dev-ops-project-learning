spam = 0
while (spam < 5):
    print("Hello, World.")
    spam+=1

# Annoying while loops -
name = ""
while (name != 'Ram') :
    print("please type your name...")
    name = input()
print("Thank you!")

# With break statements -
while True :
    print("Please enter your name - ")
    name = input()
    if (name == 'Ram') :
        break
print("Thank you!")

# Ask for name and password -
while True :
    print("Who are you?")
    name = input()
    if name != 'Ram':
        continue
    print("Hello, Ram. What is the password?")
    password = input()
    if password == 'swordfish' :
        break;
print("Access granted.")

# Working with Truthy and Falsey statements -
name =""
while not name :
    print("Enter your name -")
    name = input()
print("How many guests will you have ?")
numOfGuests = int(input())
if numOfGuests :
    print("Be sure you have enough room for all guests.")
print("Done")