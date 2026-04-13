catNames = []
while True :
    print("Enter the name of cat or press enter to stop input feed -")
    name = input()
    if name == '':
        break;
    catNames = catNames + [name] # List concat

print("The name of cats you have entered are - ")
for i in catNames:
    print("    " + i)

supplies = ['pens', 'staplers', 'flame-throwers', 'binders', 'glue']
for i in range(len(supplies)):
    print("Index " + str(i+1) + " in supplies is " + supplies[i])

print('The list of SUPPLIES contain "pens" ' + str('pens' in supplies))
print('The list of SUPPLIES does not contain "pens" ' + str('pens' not in supplies))


