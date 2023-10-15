import sys
def collatz(num):
    while(num != 1) :
        if num % 2 == 0:
            num =  num // 2
        else :
            num = 3 * num + 1
        print(num)
    return True

try :
    i=int(input("Enter number to be collatzed - "))
except ValueError:
    print("The entered input is not an integer... Please re-run")
    sys.exit()

collatz(i)
