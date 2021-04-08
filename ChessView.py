import pygame as p
from Chess import ChessEngine

class View():


    def __init__(self):
        p.init()
        self.screen = p.display.set_mode((View.WIDTH, View.HEIGHT))
        self.clock = p.time.Clock()
        self.screen.fill(p.Color("white"))
        self.loadImages()
    WIDTH = HEIGHT = 512  # 400 is another option
    DIMENSION = 8  # dimensions of a chess board 8x8
    SQ_SIZE = HEIGHT // DIMENSION
    MAX_FPS = 15
    IMAGES = {}

    def loadImages(self):
        self.pieces = ["wp", "wR", "wN", "wB", "wQ", "wK", "bp", "bR", "bN", "bB", "bQ", "bK"]
        for piece in self.pieces:
            View.IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (View.SQ_SIZE, View.SQ_SIZE))
    '''
    responsible for all graphics in the game
    '''

    def  drawGameState(self, screen, gs):
        self.drawBoard(self.screen, gs)  # draw squares on the screen
        self.drawPieces(self.screen, gs.board)  # draw pieces on the top of those squares
        '''
        draw squares on the board. the left top is always light
        '''


    def drawBoard(self, screen, gs):
        self.colors = [p.Color("white"), p.Color("gray")]



        for r in range(View.DIMENSION):
            for c in range(View.DIMENSION):
                self.color = self.colors[((r + c) % 2)]
                p.draw.rect(self.screen, self.color, p.Rect(c * View.SQ_SIZE, r * View.SQ_SIZE, View.SQ_SIZE, View.SQ_SIZE))

                if gs.whiteToMove:
                    p.draw.rect(self.screen, p.Color("green"), p.Rect(0 * View.SQ_SIZE, 0 * View.SQ_SIZE, View.SQ_SIZE, View.SQ_SIZE))
                else:
                    p.draw.rect(self.screen, p.Color("magenta"), p.Rect(0 * View.SQ_SIZE, 0 * View.SQ_SIZE, View.SQ_SIZE, View.SQ_SIZE))


        '''
        draw the pieces on the board using the current GameState.board
        '''


    def drawPieces(self, screen, board):
        for r in range(View.DIMENSION):
            for c in range(View.DIMENSION):
                self.piece = board[r][c]
                if self.piece != "--":  # not empty square
                    screen.blit(View.IMAGES[self.piece], p.Rect(c * View.SQ_SIZE, r * View.SQ_SIZE, View.SQ_SIZE, View.SQ_SIZE))


    def running(self):
        pass
