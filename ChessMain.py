"""
This is pur main drive file. It will be responsible for handling user input
and displaying the current GameState object
"""
import pygame as p
from Chess import ChessEngine, ChessView



WIDTH = HEIGHT = 512 #400 is another option
DIMENSION = 8#dimensions of a chess board 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

'''
Initialize a global dictionary of images.This will be called only once in the main
'''

"""def loadImages():
    pieces = ["wp", "wR", "wN", "wB", "wQ", "wK", "bp", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
        #Note: we can access an image by saying 'IMAGES['wp']'
"""
'''The main driver for our code. This will handle user input and updating the graphics'''

def main():
    """p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))"""
    view = ChessView.View()
    gs = ChessEngine.GameState()

    running = True
    sqSelected = () #no square is selected, keep track of the last click of the user (tuple: (row, col))
    playerClicks = [] #keep track of player clock list of two tuple [(6,4), (4,4)]
    validMoves = gs.getValidMoves()
    moveMade = False #flag variable for when a move is made
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
                if len(playerClicks) == 2: #after 2nd click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
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


        view.drawGameState(view.screen, gs)
        view.clock.tick(MAX_FPS)
        p.display.flip()
        #print(IMAGES)


"""def drawGameState(screen, gs):
    drawBoard(screen)#draw squares on the screen
    drawPieces(screen, gs.board) #draw pieces on the top of those squares
    '''
    draw squares on the board. the left top is always light
    '''
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

    '''
    draw the pieces on the board using the current GameState.board
    '''
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": #not empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


"""




if __name__ == "__main__":
    main()