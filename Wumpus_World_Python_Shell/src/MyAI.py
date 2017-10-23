# ======================================================================
# FILE:        MyAI.py
#
# AUTHOR:      Abdullah Younis
#
# DESCRIPTION: This file contains your agent class, which you will
#              implement. You are responsible for implementing the
#              'getAction' function and any helper methods you feel you
#              need.
#
# NOTES:       - If you are having trouble understanding how the shell
#                works, look at the other parts of the code, as well as
#                the documentation.
#
#              - You are only allowed to make changes to this portion of
#                the code. Any changes to other portions of the code will
#                be lost when the tournament runs your code.
# ======================================================================

from Agent import Agent
from collections import defaultdict

class MyAI ( Agent ):
    #

    def __init__ ( self ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        self.canShoot = 1
        self.moves = [] 
        self.dir = 'e'
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def getAction( self, stench, breeze, glitter, bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================

        if(glitter):
            self.moves.append('G')
            return Agent.Action.GRAB
        if(stench):
            return
            #next to Wumpus
        if(breeze): 
            if(len(self.moves) == 0):
                return Agent.Action.CLIMB
            return
            #next to Pit
        if(bump) :
            

            pass
            #hit a wall
        if(scream): 
            pass
            #'Wumpus is dead (only percieved on following turn)

        return Agent.Action.FORWARD
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================
    def oppdir(string a)
    {
        if(a == 'e'):
            return 'w'
        if(a == 's'):
            return 'n'
        if(a == 'w'):
            return 'e'
        if(a == 'n'):
            return 's'
    }
    # ======================================================================
    # YOUR CODE BEGINS
    # ======================================================================
    def getDir():
        return self.dir
    
    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================