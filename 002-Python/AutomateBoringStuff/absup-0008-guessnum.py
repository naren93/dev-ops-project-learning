import random;

print("I am thinking of a number from 1 to 20")
r=random.randint(1, 20)
print("Take a guess...")

for i in range(6):
    guess = int(input())
    if(guess > r):
        print("Your guess is too high. Try again... " + str(5-i) + " guesses left.")
    elif(guess < r):
        print("Your guess is too low. Try again... " + str(5-i) + " guesses left.")
    else :
        print("You have guessed it correctly, you have guessed it in " + str(i) + " attempt(s).")
        break;
    if(i==5):
        print("You have exceeded the number of guesses. Game Over!")

