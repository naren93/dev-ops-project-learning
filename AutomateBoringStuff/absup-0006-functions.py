# Simple function -
def hello():
    print("Howdy!")
    print("Hello!")
    print("Hello there!!")

hello()

# Function with parameters -
def hie(name):
    print("Hello, " + name + "!")

hie('naren')
hie('ram')

# Functions that return values -
import random;

def getAnswer(ansNumber):
    if ansNumber == 1:
        return "It is certain"
    elif ansNumber == 2:
        return "It is decidedly so."
    elif ansNumber == 3:
        return "Yes"
    elif ansNumber == 5:
        return "Reply hazey try again!"
    elif ansNumber == 6:
        return "Ask again"
    elif ansNumber == 7:
        return "Concentrate and ask again."
    elif ansNumber == 8:
        return "Outlook is not so good."
    elif ansNumber == 9:
        return "Very doubtful."
    else :
        return "Invalid."

fortune = getAnswer(random.randint(1, 9))
while fortune != "It is certain" :
    print(fortune)
    fortune = getAnswer(random.randint(1, 9))
print(fortune)

# Functions with args and kwargs - (a,b,*args,**kwargs)
def solution(operation=""):
    if operation == 'add':
        return("1 + 1 = " + str(1+1))
    elif operation == 'multiply':
        return("2 * 2 = " + str(2*2))
    else :
        return "INVALID"

print(solution(operation="add"))

def solution0(a, b, operation=""):
    if operation == 'add':
        return(str(a) + " + " + str(b) + " = " + str(a+b))
    elif operation == 'multiply':
        return(str(a) + " * " + str(b) + " = " + str(a*b))
    else :
        return "INVALID"

print(solution0(100, 200, operation="add"))
print(solution0(100, 200))

# Local and Global scope and statements

eggs = 1000
def spam():
    global eggs
    return eggs
def ham():
    eggs=100
    return eggs
def bam():
    return eggs
print(str(spam()) + " because of the global statement.")
print(str(ham()) + " because of the local scope.")
print(str(bam()) + " now what do we have here...")
