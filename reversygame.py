# "Реверси" или "Отелло"

import random
import sys


def drawBoard(board):
    # Вывести игровое поле переданное этой функции. Ничего не возвращать.
    HLINE = ' +---+---+---+---+---+---+---+---+'
    VLINE = ' | | | | | | | | |'

    print(' 1 2 3 4 5 6 7 8')
    print(HLINE)
    for y in range(8):
        print(VLINE)
        print(y+1, end=' ')
        for x in range(8):
            print('| %s' % (board[x][y]), end=' ')
        print('|')
        print(VLINE)
        print(HLINE)

def resetBoard(board):
    # Зачищает переданную доску, за исключением исходного положения.
    for x in range(8):
        for y in range(8):
            board[x][y] = ' '

    # Исходные фрагменты:
    board[3][3] = 'X'
    board[3][4] = 'O'
    board[4][3] = 'O'
    board[4][4] = 'X'


def getNewBoard():
    # Создает новую структуру данных на чистой доске.
    board = []
    for i in range(8):
        board.append([' '] * 8)

    return board


def isValidMove(board, tile, xstart, ystart):
    # Возвращает значение False, если ход игрока по пробелу xstart, ystart недействителен.
    # Если это допустимый ход, возвращает список пробелов, которые стали бы принадлежать игроку, если бы он сделал ход здесь.
    if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
        return False

    board[xstart][ystart] = tile # временно установит фишку на доску.

    if tile == 'X':
        otherTile = 'O'
    else:
        otherTile = 'X'

    tilesToFlip = []
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection # первый шаг в сторону
        y += ydirection # первый шаг в сторону
        if isOnBoard(x, y) and board[x][y] == otherTile:
            # Рядом с нашей фишкой находится фишка, принадлежащая другому игроку.
            x += xdirection
            y += ydirection
            if not isOnBoard(x, y):
                continue
            while board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not isOnBoard(x, y): # выйдите из цикла while, затем продолжите в цикле for
                    break
            if not isOnBoard(x, y):
                continue
            if board[x][y] == tile:
                # Есть фишки, которые нужно перевернуть. Двигайтесь в обратном направлении, пока не дойдем до исходного места, отмечая все фрагменты по пути.
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append([x, y])

    board[xstart][ystart] = ' ' # восстановите пустое пространство
    if len(tilesToFlip) == 0: # Если ни одина фишка не была перевернута, это недопустимый ход.
        return False
    return tilesToFlip


def isOnBoard(x, y):
    # Возвращает значение True, если координаты расположены на доске.
    return x >= 0 and x <= 7 and y >= 0 and y <=7


def getBoardWithValidMoves(board, tile):
    # Возвращает новую доску с пометкой допустимых ходов, которые может сделать данный игрок.
    dupeBoard = getBoardCopy(board)

    for x, y in getValidMoves(dupeBoard, tile):
        dupeBoard[x][y] = '.'
    return dupeBoard


def getValidMoves(board, tile):
    # Возвращает список [x,y] допустимых ходов для данного игрока на данной доске.
    validMoves = []

    for x in range(8):
        for y in range(8):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append([x, y])
    return validMoves


def getScoreOfBoard(board):
    # Определите счет, подсчитав количество фишек. Возвращает словарь с ключами "X" и "O".
    xscore = 0
    oscore = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == 'X':
                xscore += 1
            if board[x][y] == 'O':
                oscore += 1
    return {'X':xscore, 'O':oscore}


def enterPlayerTile():
    # Позволить игроку ввести выбранную фишку.
    # Возвращает список с фишкой игрока в качестве первого элемента и фишкой компьютера в качестве второго.
    tile = ''
    while not (tile == 'X' or tile == 'O'):
        print('Do you want to be X or O?')
        tile = input().upper()

    # Первый элемент в списке — фишка игрока, второй элемент — фишка компьютера.
    if tile == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']


def whoGoesFirst():
    # Случайно выбрать, кто ходит первым.
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'


def playAgain():
    # Эта функция возвращает значение True, если игрок хочет играть снова, в противном случае она возвращает значение False.
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')


def makeMove(board, tile, xstart, ystart):
    # Поместить фишку на игровое поле в позицию xstart, ystart и перевернуть какую-либо фишку противника.
    # Вернуть False, если это недопустимый ход; вернуть True, если допустимый.
    tilesToFlip = isValidMove(board, tile, xstart, ystart)

    if tilesToFlip == False:
        return False

    board[xstart][ystart] = tile
    for x, y in tilesToFlip:
        board[x][y] = tile
    return True


def getBoardCopy(board):
    # Сделать копию списка board и вернуть ее.
    dupeBoard = getNewBoard()

    for x in range(8):
        for y in range(8):
            dupeBoard[x][y] = board[x][y]

    return dupeBoard


def isOnCorner(x, y):
    # Вернуть True, если указанная позиция находится в одном из четырех углов.
    return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)


def getPlayerMove(board, playerTile):
    # Позволить игроку ввести свой ход.
    # Вернуть ход в виде [x, y] (или вернуть строки 'подсказка' или 'выход').
    DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
    while True:
        print('Введите свой ход, или введите quit, чтобы завершить игру, или hints, чтобы отключить/включить подсказки.')
        move = input().lower()
        if move == 'quit':
            return 'quit'
        if move == 'hints':
            return 'hints'

        if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
            x = int(move[0]) - 1
            y = int(move[1]) - 1
            if isValidMove(board, playerTile, x, y) == False:
                continue
            else:
                break
        else:
            print('Это недопустимый ход. Введите номер столбца (1-8) и номер ряда (1-8).')
            print('К примеру, значение 81 перемещает в верхний правый угол.')

    return [x, y]


def getComputerMove(board, computerTile):
    # Учитывая данное игровое поле и данную фишку компьютера, определить,
    # куда сделать ход, и вернуть этот ход в виде списка [x, y].
    possibleMoves = getValidMoves(board, computerTile)

    # Сделать случайным порядок ходов
    random.shuffle(possibleMoves)

    # Всегда делать ход в угол, если это возможно.
    for x, y in possibleMoves:
        if isOnCorner(x, y):
            return [x, y]

    # Найти ход с наибольшим возможным количеством очков.
    bestScore = -1
    for x, y in possibleMoves:
        dupeBoard = getBoardCopy(board)
        makeMove(dupeBoard, computerTile, x, y)
        score = getScoreOfBoard(dupeBoard)[computerTile]
        if score > bestScore:
            bestMove = [x, y]
            bestScore = score
    return bestMove


def showPoints(playerTile, computerTile):
    # Выводит текущий результат.
    scores = getScoreOfBoard(mainBoard)
    print('Ваш счет: %s. Счет компьютера: %s.' % (scores[playerTile], scores[computerTile]))



print('Добро пожаловать в Реверси!')

while True:
    # Очистить доску и игру.
    mainBoard = getNewBoard()
    resetBoard(mainBoard)
    playerTile, computerTile = enterPlayerTile()
    showHints = False
    turn = whoGoesFirst()
    print('Кнопка ' + turn + ' будет нажата первой.')

while True:
    if turn == 'player':
        # Очередь игрока.
        if showHints:
            validMovesBoard = getBoardWithValidMoves(mainBoard, playerTile)
            drawBoard(validMovesBoard)
        else:
            drawBoard(mainBoard)
        showPoints(playerTile, computerTile)
        move = getPlayerMove(mainBoard, playerTile)
        if move == 'quit':
            print('Спасибо за игру!')
            sys.exit() # завершение работы программы
        elif move == 'hints':
            showHints = not showHints
            continue
        else:
            makeMove(mainBoard, playerTile, move[0], move[1])

        if getValidMoves(mainBoard, computerTile) == []:
            break
        else:
            turn = 'computer'

    else:
        # Очередь компьютера.
        drawBoard(mainBoard)
        showPoints(playerTile, computerTile)
        input('Нажмите Enter, чтобы увидеть ход компьютера.')
        x, y = getComputerMove(mainBoard, computerTile)
        makeMove(mainBoard, computerTile, x, y)

        if getValidMoves(mainBoard, playerTile) == []:
            break
        else:
            turn = 'player'

    # Отображение итогового результата.
    drawBoard(mainBoard)
    scores = getScoreOfBoard(mainBoard)
    print('X набрал %s очков. O набрал %s очков.' % (scores['X'], scores['O']))
    if scores[playerTile] > scores[computerTile]:
        print('Вы опередили компьютер на % очков! Поздравляю!' % (scores[playerTile] - scores[computerTile]))
    elif scores[playerTile] < scores[computerTile]:
        print('Вы проиграли. Компьютер опередил вас на %s очков.' % (scores[computerTile] - scores[playerTile]))
    else:
        print('Игра закончилась вничью!')

    if not playAgain():
        break
