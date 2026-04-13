# Simply printing string based on range -
print("My Name is...")
for i in range(5):
    print("What (" + str(i) + ")")

# How about arithmatic progression now -
total = 0
for num in range(101):
    total = total + num
print(total)

# Starting, stopping and stepping in ranges -
for i in range(12, 16):
    print(i)

for i in range(0, 10, 2):
    print(i)

for i in range(5, -1, -1):
    print(i)
