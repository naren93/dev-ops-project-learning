import random, sys;

# Using the random module -
for i in range(5):
    print(random.randint(1, 10))

# using the sys.exit

while True:
    print("Type exit to exit...")
    response = input()
    if response == 'exit':
        sys.exit()
    print('You typed ' + response + '.')

