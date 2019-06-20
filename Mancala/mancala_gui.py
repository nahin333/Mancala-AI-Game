from mancala_board import MancalaBoard
from player import Player
import tkinter as tk
class MancalaWindow:
    """# A very simple GUI for playing the game of Mancala."""

    def __init__(self, master, p1, p2):
        self.CUPW = 75
        self.HEIGHT = 400
        self.BOARDW = 700
        self.PAD = 0
        self.game = MancalaBoard()
        self.p1 = p1
        self.p2 = p2
        self.BINW = self.BOARDW / self.game.NCUPS

        self.turn = p1
        self.wait = p2
        self.root = master
        
        frame = tk.Frame(master)
        frame.pack()

        # Create the board
        self.makeBoard( frame )
        
        displayStr = "Welcome to Mancala"
            
        self.status = tk.Label(frame, text=displayStr)
        self.status.pack(side=tk.BOTTOM)
        
        self.frame = frame
        
    def enableBoard(self):
        """ Allow a human player to make moves by clicking"""
        for i in [0, 1]:
            for j in range(self.game.NCUPS):
                self.cups[i][j].bind("<Button-1>", self.callback)

    def disableBoard(self):
        """ Prevent the human player from clicking while the computer thinks"""
        for i in [0, 1]:
            for j in range(self.game.NCUPS):
                self.cups[i][j].unbind("<Button-1>")

    def makeBoard( self, frame ):
        """ Create the board """
        boardFrame = tk.Frame(frame)
        boardFrame.pack(side=tk.TOP)

        self.button = tk.Button(frame, text="Start New Game", command=self.newgame)
        self.button.pack(side=tk.BOTTOM)

        gamef = tk.Frame(boardFrame)
        topRow = tk.Frame(gamef)
        bottomRow = tk.Frame(gamef)
        topRow.pack(side=tk.TOP)
        bottomRow.pack(side=tk.TOP)
        tmpCups = []
        tmpCups2 = []

        binW = self.BOARDW/self.game.NCUPS
        binH = self.HEIGHT/2

        for i in range(self.game.NCUPS):
            c = tk.Canvas(bottomRow, width=binW, height=binH)
            c.pack(side=tk.LEFT)
            tmpCups += [c]
            c = tk.Canvas(topRow, width=binW, height=binH)
            c.pack(side=tk.LEFT)
            tmpCups2 += [c]

        self.cups = [tmpCups, tmpCups2]
        self.p1cup = tk.Canvas(boardFrame, width=self.CUPW, height=self.HEIGHT)
        self.p2cup = tk.Canvas(boardFrame, width=self.CUPW, height=self.HEIGHT)

        self.p2cup.pack(side=tk.LEFT)
        gamef.pack(side=tk.LEFT)
        self.p1cup.pack(side=tk.LEFT)

        self.drawBoard()


    def drawBoard( self ):
        """ Draw the board on the canvas """
        self.p2cup.create_oval(self.PAD, self.PAD, self.CUPW, 0.9*self.HEIGHT, width=2 )
        binW = self.BOARDW/self.game.NCUPS
        binH = self.HEIGHT/2
        for j in [0, 1]:
            for i in range(self.game.NCUPS):
                
                self.cups[j][i].create_rectangle(self.PAD, self.PAD, binW, binH)
        self.p1cup.create_oval(self.PAD, self.PAD+0.1*self.HEIGHT, self.CUPW, self.HEIGHT, width=2 )
        

    def newgame(self):
        """ Start a new game between the players """
        self.game.reset()
        self.turn = self.p1
        self.wait = self.p2
        s = "Player " + str(self.turn) + "'s turn"
        if self.turn.type != Player.HUMAN:
            s += " Please wait..."
        self.status['text'] = s
        self.resetStones()
        self.continueGame()

    # Board must be disabled to call continueGame
    def continueGame( self ):
        """ Find out what to do next.  If the game is over, report who
            won.  If it's a human player's turn, enable the board for
            a click.  If it's a computer player's turn, choose the next move."""
        self.root.update()
        if self.game.gameOver():
            if self.game.hasWon(self.p1.num):
                self.status['text'] = "Player " + str(self.p1) + " wins"
            elif self.game.hasWon(self.p2.num):
                self.status['text'] = "Player " + str(self.p2) + " wins"
            else:
                self.status['text'] = "Tie game"
            return
        if self.turn.type == Player.HUMAN:
            self.enableBoard()
        else:
            move = self.turn.chooseMove( self.game )
            playAgain = self.game.makeMove( self.turn, move )
            if not playAgain:
                self.swapTurns()
            self.resetStones()
            self.continueGame()

    def swapTurns( self ):
        """ Change whose turn it is"""
        temp = self.turn
        self.turn = self.wait
        self.wait = temp
        statusstr = "Player " + str(self.turn) + "\'s turn "
        if self.turn.type != Player.HUMAN:
            statusstr += "Please wait..."
        self.status['text'] = statusstr
        
        
    def resetStones(self):
        """ Clear the stones and redraw them """
        # Put the stones in the cups
        for i in range(len(self.game.P2Cups)):
            index = (len(self.game.P2Cups)-i)-1
            self.clearCup(self.cups[1][index])
            # put the number of stones at the top of the canvas
            self.cups[1][index].create_text(self.BINW/2, 0.05*self.HEIGHT, text=str(self.game.P2Cups[i]), tag="num")
        for i in range(len(self.game.P1Cups)):
            # put the number of stones at the bottom of the canvas
            self.clearCup(self.cups[0][i])
            self.cups[0][i].create_text(self.BINW/2, 0.05*self.HEIGHT, text=str(self.game.P1Cups[i]), tag="num")
        self.clearCup(self.p1cup)
        self.clearCup(self.p2cup)
        self.p2cup.create_text(self.CUPW/2, 10, text=str(self.game.scoreCups[1]), tag="num")
        self.p1cup.create_text(self.CUPW/2, 10+0.1*self.HEIGHT, text=str(self.game.scoreCups[0]), tag="num")
        
    
    def clearCup( self, cup ):
        """ Clear the stones in the given cup"""
        titems = cup.find_withtag("num")
        stones = cup.find_withtag("stone")
        cup.delete(titems)
        cup.delete(stones)
            

    def callback(self, event):
        """ Handle the human player's move"""
        # calculate which box the click was in
        moveAgain = True
        self.disableBoard()
        if self.turn.num == 1:
            for i in range(len(self.cups[0])):
                if self.cups[0][i] == event.widget:
                    if self.game.legalMove( self.turn, i+1 ):
                        moveAgain = self.game.makeMove( self.turn, i+1 )
                        if not moveAgain:
                            self.swapTurns()
                        self.resetStones()
        else:
            for i in range(len(self.cups[1])):
                if self.cups[1][i] == event.widget:
                    index = self.game.NCUPS - i
                    if self.game.legalMove( self.turn, index ):
                        moveAgain = self.game.makeMove( self.turn, index )
                        if not moveAgain:
                            self.swapTurns()
                        self.resetStones()
        if moveAgain:
            self.enableBoard()
        else:
            self.continueGame()
            
    def mainloop(self):
        self.frame.mainloop()
        

def startGame(p1, p2):
    """ Start the game of Mancala with two players """
    root = tk.Tk()

    app = MancalaWindow(root, p1, p2)

    app.mainloop()
   
player1 = Player(1,Player.HUMAN)
player2 = Player(2,Player.ABPRUNE)
startGame(player1,player2)