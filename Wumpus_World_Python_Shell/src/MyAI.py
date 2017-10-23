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
        self.dir = 'e'
        self.position = (0,0)
        self.orientation_history = [
            (self.position, self.dir)
        ]
        self.can_shoot = True # always a boolean
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def getAction( self, stench, breeze, glitter, bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================

        if(glitter):
            return Agent.Action.GRAB
        if(stench):
            return
            #next to Wumpus
        if(breeze): 
            if(len(self.orientation_history) == 0):
                return Agent.Action.CLIMB
            return
            #next to Pit
        if(bump) :
            

            pass
            #hit a wall
        if(scream): 
            pass
            #'Wumpus is dead (only percieved on following turn)
        
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================
    def oppdir(dir_s):
        if(dir_s == 'e'):
            return 'w'
        if(dir_s == 's'):
            return 'n'
        if(dir_s == 'w'):
            return 'e'
        if(dir_s == 'n'):
            return 's'
    # ======================================================================
    # YOUR CODE BEGINS
    # ======================================================================
    def get_dir(self):
        return self.dir

    def get_position(self):
        return self.position


    # Return the first and last moves that happened in the move history
    def get_latest(self):
        return self.orientation_history[-1]

    def get_first(self):
        return self.orientation_history[0]

    def move_forward(self):
        #updates the position and orientation history
        if(self.dir == 'e'):
            self.position = (self.position[0] + 1, self.position[1])
        if(self.dir == 'w'):
            self.position = (self.position[0] - 1, self.position[1])
        if(self.dir == 'n'):
            self.position = (self.position[0], self.position[1] + 1)
        if(self.dir == 's'):
            self.position = (self.position[0], self.position[1] - 1)
        self.orientation_history.append((self.position, self.dir))
        return Agent.Action.FORWARD

    def turn_left(self):
        if(self.dir == 'e'):
            self.dir = 'n'
        if(self.dir == 'w'):
            self.dir = 's'
        if(self.dir == 'n'):
            self.dir = 'w'
        if(self.dir == 's'):
            self.dir = 'e'
        self.orientation_history.append((self.position, self.dir))
        return Agent.Action.TURN_LEFT


    def turn_right(self):
        if(self.dir == 'e'):
            self.dir = 's'
        if(self.dir == 'w'):
            self.dir = 'n'
        if(self.dir == 'n'):
            self.dir = 'e'
        if(self.dir == 's'):
            self.dir = 'w'   
        self.orientation_history.append((self.position, self.dir))
        return Agent.Action.TURN_RIGHT
    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================