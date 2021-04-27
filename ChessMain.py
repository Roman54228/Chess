
'''def play(gs, view):
    running = True
    sqSelected = ()  # no square is selected, keep track of the last click of the user (tuple: (row, col))
    playerClicks = []  # keep track of player clock list of two tuple [(6,4), (4,4)]
    validMoves = gs.getValidMoves()
    moveMade = False  # flag variable for when a move is made

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
'''

import pygame as p
from Chess import ChessEngine, ChessView

def main():
    """p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))"""
    view = ChessView.View()
    gs = ChessEngine.GameState()
    pl = ChessEngine.Playing()

    pl.play(gs, view)



if __name__ == "__main__":
    main()