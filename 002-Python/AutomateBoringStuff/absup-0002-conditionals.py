name = "Alice"
password = "swordfish"
age = 2000
if(name == 'Mary') :
    print("Hello Mary!")
    if(password == "swordfish"):
        print("Access granted.")
    else :
        print("Wrong Password.")
elif (age < 12) :
    print("You are not Mary, kiddo.")
elif (age > 100) :
    print("You are not Alice, Grannie");
elif (age > 2000):
    print("Unlike you Alice is not a immortal vampire.")
else :
    print("Who are you again?")