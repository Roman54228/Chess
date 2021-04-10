"""
This class is responsible for storing all the information about the current state of a chess game.
It will also be responsible for determining the valid moves at the current time.
It will also keep a move log.
"""
import pygame as p
from Chess import ChessView

class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

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
        self.whiteToMove = not self.whiteToMove #swap players
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.balckKingLocation = (move.endRow, move.endCol)



    '''
    Undo the last move made
    '''

    def undoMove(self):
        if len(self.moveLog) != 0: #make sure there was a move
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # switch turns back
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)


    '''
    All moves considering checks
    '''

    def getValidMoves(self):
        moves = self.getAllPossibleMoves()
        """"#1) generate all possible moves
        moves = self.getAllPossibleMoves()
        #2) for each move, make the move
        for i in range(len(moves) - 1, -1, -1): #when removing from that list go backward through that list
            self.makeMove(moves[i])
            #3) generate all oponents moves
            #4) for each of opponents moves, see if they can attack your king
            self.whiteToMove = not self.whiteToMove

            if self.inCheck():
                moves.remove(moves[i]) #5) if they do attack your king, not a valid move
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0: #either checkmate or stalemate
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False"""

        return moves #for now we dont carry about valid moves

    """
    Determine if the current player is in check
    """

    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])



    """
    Determine if the enemy can attack the same square r, c
    """
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove #switch to opponent turn
        oppMoves =  self.getAllPossibleMoves()
        for move in oppMoves:
            if move.endRow == r and move.endCol == c: #square is under attack
                self.whiteToMove = not self.whiteToMove #switch turn back
                return True
        return False
    '''
    All moves without considering checks
    '''

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): #number of rows
            for c in range(len(self.board[r])): #number of cols in a given row
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)

        return moves


    '''
    Get all pawn moves for the pawn located at row, col and add these moves to the list
    '''
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: #white pawn move
            if self.board[r-1][c] == "--":
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0: #attack to the left
                if self.board[r-1][c-1][0] == 'b': #enemy piece
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 <= 7: # attack to the right
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))

        else:
            if self.board[r+1][c] == "--":
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0: #attack to the left
                if self.board[r+1][c-1][0] == 'w': #enemy piece
                    moves.append(Move((r, c), (r + 1 , c - 1), self.board))
            if c + 1 <= 7: # attack to the right
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))



    '''
    Get all pawn moves for the rook located at row, col and add these moves to the list
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
        print(self.moveID)


    '''
    Overriding the equal method
    '''

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False



    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]



class Playing:
    view = ChessView.View()
    gs = GameState()
    def play(self, gs, view):
        WIDTH = HEIGHT = 512  # 400 is another option
        DIMENSION = 8  # dimensions of a chess board 8x8
        SQ_SIZE = HEIGHT // DIMENSION
        MAX_FPS = 15
        running = True
        sqSelected = ()  # no square is selected, keep track of the last click of the user (tuple: (row, col))
        playerClicks = []  # keep track of player clock list of two tuple [(6,4), (4,4)]
        validMoves = gs.getValidMoves()
        moveMade = False  # flag variable for when a move is made
        a1 = ()

        while running:
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
                #mouse handler
                elif e.type == p.MOUSEBUTTONDOWN:

                    location = p.mouse.get_pos() #(x,y) location of mouse
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if sqSelected == (row, col): #the user clicked the same square
                        sqSelected = () #deselect
                        playerClicks = [] #clear player clicks
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected) #append for both 1st and 2nd clicks
                        if gs.board[sqSelected[0]][sqSelected[1]] != "--":
                            a1 = sqSelected
                        else:
                            a1 = ()
                    if len(playerClicks) == 2: #after 2nd click
                        move = Move(playerClicks[0], playerClicks[1], gs.board)

                        #a1 = playerClicks[0]
                        print(a1)
                        #print(move.getChessNotation())

                        if move in validMoves:
                            gs.makeMove(move)
                            moveMade = True

                            sqSelected = () #reset player clicks
                            playerClicks = [] #reset
                        else:
                            playerClicks = [sqSelected]
                #key handler
                elif e.type == p.KEYDOWN:
                    if e.key == p.K_z: #undo when z is pressed
                        gs.undoMove()
                        moveMade = True
            if moveMade:
                validMoves = gs.getValidMoves()
                moveMade = False


            view.drawGameState(view.screen, gs, a1)
            view.clock.tick(15)
            p.display.flip()
        #print(IMAGES)