import pygame as p
from Chess import ChessEngine

class View():
    WIDTH = HEIGHT = 512  # 512 либо 400
    DIMENSION = 8  # доска 8x8
    SQ_SIZE = HEIGHT // DIMENSION
    MAX_FPS = 15
    IMAGES = {}


    def __init__(self):

        p.init()
        self.screen = p.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = p.time.Clock()
        self.screen.fill(p.Color("white"))
        self.loadImages()



    def loadImages(self):
        self.pieces = ["wp", "wR", "wN", "wB", "wQ", "wK", "bp", "bR", "bN", "bB", "bQ", "bK"]
        for piece in self.pieces:
            View.IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (View.SQ_SIZE, View.SQ_SIZE))
    '''
    responsible for all graphics in the game
    '''

    def  drawGameState(self, screen, gs, a1, validMoves):
        self.drawBoard(self.screen, gs, a1)  # рисует клетки на доске
        self.drawPieces(self.screen, gs.board)  # рисует фигуры поверх клеток
        self.highLight(self.screen, gs, validMoves, a1)
        '''
        draw squares on the board. the left top is always light
        '''

    def highLight(self, screen, gs, validmoves, a1):
        if a1 != ():
            r, c = a1
            s = p.Surface((self.SQ_SIZE, self.SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            for move in validmoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*self.SQ_SIZE, move.endRow*self.SQ_SIZE))
                    #p.draw.rect(self.screen, p.Color("green"), p.Rect(move.endCol * View.SQ_SIZE, move.endRow * View.SQ_SIZE, View.SQ_SIZE, View.SQ_SIZE))


    def drawBoard(self, screen, gs, a1):
        self.colors = [p.Color("white"), p.Color("gray")]




        for r in range(View.DIMENSION):
            for c in range(View.DIMENSION):
                self.color = self.colors[((r + c) % 2)]
                p.draw.rect(self.screen, p.Color(self.color), p.Rect(r * View.SQ_SIZE, c * View.SQ_SIZE, View.SQ_SIZE, View.SQ_SIZE))
                if gs.whiteToMove:
                    p.draw.rect(self.screen, p.Color("green"), p.Rect(0 * View.SQ_SIZE, 0 * View.SQ_SIZE, View.SQ_SIZE, View.SQ_SIZE))

                else:
                    p.draw.rect(self.screen, p.Color("red"), p.Rect(0 * View.SQ_SIZE, 0 * View.SQ_SIZE, View.SQ_SIZE, View.SQ_SIZE))
                if len(a1) != 0:
                    p.draw.rect(self.screen, p.Color("yellow"), p.Rect(a1[1] * View.SQ_SIZE, a1[0] * View.SQ_SIZE, View.SQ_SIZE, View.SQ_SIZE))










        '''
        draw the pieces on the board using the current GameState.board 
        '''

    def highlight(self, screen, sqSelected):
        #p.draw.rect(self.screen, p.Color("blue"), p.Rect(sqSelected[0] * self.SQ_SIZE, sqSelected[1] * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))
        screen.blit(p.Rect(sqSelected * self.SQ_SIZE, sqSelected * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE), )


    def drawPieces(self, screen, board):
        for r in range(View.DIMENSION):
            for c in range(View.DIMENSION):
                self.piece = board[r][c]
                if self.piece != "--":  # not empty square
                    screen.blit(View.IMAGES[self.piece], p.Rect(c * View.SQ_SIZE, r * View.SQ_SIZE, View.SQ_SIZE, View.SQ_SIZE))






