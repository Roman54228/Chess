
import pygame as p
from Chess import ChessView

class GameState():
    def __init__(self):
        #имена фигур в матрице соответствуют названию .png файлов для прогрузки картинки
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        #через этот словарь будем получать доступные ходы для каждой из фигур
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}

        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove #смена игроков
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.balckKingLocation = (move.endRow, move.endCol)



    '''
    отмена последнего хода
    '''

    def undoMove(self):
        if len(self.moveLog) != 0: #убедиться что ход был
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # switch turns back
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)



    def getValidMoves(self): #ходы которые не подставляют под шах и мат
        moves = self.getAllPossibleMoves()
        return moves #( пока не готово, просто возвращает всевозоможные ходы

    """
    Determine if the current player is in check
    """


    def getAllPossibleMoves(self):#возвращает список всевозможных ходов
        moves = []#заполняется экземплярами класса Move()
        for r in range(len(self.board)): #число строк
            for c in range(len(self.board[r])): #число столбцов
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)

        return moves


    '''
    Get all pawn moves for the pawn located at row, col and add these moves to the list
    '''
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: #ход белых
            if self.board[r-1][c] == "--":
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0: #атаковать налево
                if self.board[r-1][c-1][0] == 'b': #вражеская фигура
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 <= 7: # атаковать направо
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))

        else:
            if self.board[r+1][c] == "--":
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0: #атаковать налево
                if self.board[r+1][c-1][0] == 'w': #вражеская фигура
                    moves.append(Move((r, c), (r + 1 , c - 1), self.board))
            if c + 1 <= 7: # aтаковать направо
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))



    '''
    Все допустимые ходы ферзя, находящегося в row, col  добавляем эти экземпляры класса Move в список moves
    '''
    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break





    #Ходы слона
    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    #Ходы коня
    def getKnightMoves(self, r, c, moves):
        knighMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knighMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r,c), (endRow, endCol), self.board))


    #Ходы королевы
    def getQueenMoves(self, r, c, moves):
        self.getBishopMoves(r, c, moves)
        self.getRookMoves(r, c, moves)

    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1,-1), (1,1), (-1,1), (1,-1), (-1, 0), (1, 0), (0, 1), (0, -1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in kingMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))


#Аргументы - это клетка с которой начинаем ходить, клетка в которую хотим перейти и доска
class Move():

    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                  "5": 3, "6": 2, "7": 1, "8": 0}

    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        #print(self.moveID)


    '''
    Overriding the equal method
    '''

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


    #логирование ходов
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]



class Playing:
    view = ChessView.View()
    gs = GameState()
    def play(self, gs, view):
        running = True
        sqSelected = ()  # клетка не выбрана, сохраняем клики ввиде кортежа (tuple: (row, col))
        playerClicks = []  # сохраняем два клика в список [(6,4), (4,4)]
        validMoves = gs.getValidMoves()
        moveMade = False  # флаг, отслеживаем был ли сделан ход
        a1 = () #пустой кортеж, нужен для подсвечивания

        while running:
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
                #клик мышки заносится в очередь
                elif e.type == p.MOUSEBUTTONDOWN:

                    location = p.mouse.get_pos() #(x,y) координаты курсора
                    col = location[0]//view.SQ_SIZE
                    row = location[1]//view.SQ_SIZE
                    if sqSelected == (row, col): #игрок кликнул на ту эже клетку
                        sqSelected = () #в этом случае очистим кортеж
                        playerClicks = [] #и очистим список кликов
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                        if gs.board[sqSelected[0]][sqSelected[1]] != "--":
                            a1 = sqSelected
                        else:
                            a1 = ()
                    if len(playerClicks) == 2: #после второго клика
                        move = Move(playerClicks[0], playerClicks[1], gs.board)

                        #a1 = playerClicks[0]

                        print(move.getChessNotation())#выводим логи ходов в консоль

                        if move in validMoves:#если move в списке доступных ходов, то совершаем такой ход
                            print(validMoves)
                            gs.makeMove(move)
                            moveMade = True
                            sqSelected = () #очищаем все
                            playerClicks = []
                        else:
                            playerClicks = [sqSelected]
                #контроль клавиатуры
                elif e.type == p.KEYDOWN:
                    if e.key == p.K_z: #возврат хода, при нажатии клавиши z
                        gs.undoMove()
                        moveMade = True
            if moveMade:
                validMoves = gs.getValidMoves()
                moveMade = False


            view.drawGameState(view.screen, gs, a1, validMoves)
            view.clock.tick(15)
            p.display.flip()
        #print(IMAGES)
