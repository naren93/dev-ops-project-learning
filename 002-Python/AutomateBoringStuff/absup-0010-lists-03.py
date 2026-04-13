# Given list -
spam = ['apples', 'bananas', 'tofu', 'cat']

# List conversion to string
def listConvert(given):
    str = ''
    for i in range(0, len(given)):
        if(i == len(given)-1):
            str = str + ' and ' + given[i]
        elif(i==0):
            str = str + given[i]
        else :
            str = str + ', ' + given[i]
    # Return statement
    return str

print(listConvert(spam))

grid = [['.', '.', '.', '.', '.', '.'],
    ['.', 'O', 'O', '.', '.', '.'],
    ['O', 'O', 'O', 'O', '.', '.'],
    ['O', 'O', 'O', 'O', 'O', '.'],
    ['.', 'O', 'O', 'O', 'O', 'O'],
    ['O', 'O', 'O', 'O', 'O', '.'],
    ['O', 'O', 'O', 'O', '.', '.'],
    ['.', 'O', 'O', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.']]

# for i in grid:
#     for j in i:
#         print(j, end='')
#     print(end='\n')
# Love your lists
for j in range(0, len(grid[1])):
    for i in range(0,len(grid)):
        print(grid[i][j], end='')
    print(end='\n')
