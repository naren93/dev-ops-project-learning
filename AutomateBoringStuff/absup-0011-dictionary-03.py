def displayInventory(inventory):
    print("Inventory -")
    total = 0
    for i in inventory.keys():
        print(inventory[i], i)
        total = inventory[i] + total
    print("Total number of items = " + str(total))

stuff = {'rope': 1, 'torch': 6, 'gold coin': 42, 'dagger': 1, 'arrow': 12}

displayInventory(stuff)
print("=================")

# convert list into dicitionary -
dragonLoot = ['gold coin', 'dagger', 'gold coin', 'gold coin', 'ruby']
inv = {'gold coin': 42, 'rope': 1}

def addToInventory(inventory, addItems):
    for i in addItems:
        if i not in inventory:
            inventory[i]=0
        inventory[i]=inventory[i]+1
    return inventory

inv = addToInventory(inv, dragonLoot)
displayInventory(inv)
