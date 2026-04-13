theBoard = {'top-L': ' ', 'top-M': ' ', 'top-R': ' ',
    'mid-L': ' ', 'mid-M': ' ', 'mid-R': ' ',
    'low-L': ' ', 'low-M': ' ', 'low-R': ' '
}

def printBoard(board):
    print(board['top-L'] + '|' + board['top-M'] + '|' + board['top-R'])
    print('-+-+-')
    print(board['mid-L'] + '|' + board['mid-M'] + '|' + board['mid-R'])
    print('-+-+-')
    print(board['low-L'] + '|' + board['low-M'] + '|' + board['low-R'])

def toeCheck(board, turn):
    if (board['top-L'] == board['top-R']) and (board['top-L'] == board['top-M']) and (board['top-L']!=' '):
        return 'W'
    elif (board['mid-L'] == board['mid-R']) and (board['mid-L'] == board['mid-M']) and (board['mid-L']!=' '):
        return 'W'
    elif (board['low-L'] == board['low-R']) and (board['low-L'] == board['low-M']) and (board['low-L']!=' '):
        return 'W'
    elif (board['top-L'] == board['low-R']) and (board['top-L'] == board['mid-M']) and (board['top-L']!=' '):
        return 'W'
    elif (board['low-L'] == board['top-R']) and (board['low-L'] == board['mid-M']) and (board['low-L']!=' '):
        return 'W'
    else :
        return 'D'

turn = 'x'
for i in range(9):
    printBoard(theBoard)
    print('Turn for ' + turn + '. Make a move on which space - ')
    move = input()
    theBoard[move]=turn
    if (toeCheck(theBoard, turn) == 'W'):
        print(turn + ' wins.')
        break;
    else:
        if i==8:
            print('This match is a draw.')
        else :
            if turn=='x':
                turn = 'o'
            else :
                turn = 'x'

