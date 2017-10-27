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

'''
    What are some of the edge cases?
    1. Start on the gold (glitter)
        a. Pick the gold up
        b. Climb out
    2. Start with a stench
        a. Shoot arrow to figure out where Wumpus is
    3. Start with a breeze
        a. Climb out since you don't want to risk losing -1000 points
    4. Wumpus is on the Gold

'''

import random

from Agent import Agent


class MyAI ( Agent ):
    
    def __init__ ( self ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        self.dir = 'e'
        self.goal_dir = 'e'
        self.position = (0,0)
        self.wanted_position = (0,0)
        self.orientation_history = [
            (self.position, self.dir)
        ]
        self.backward = False
        self.turning = False
        self.move_count = 0
        self.gold_obtained = False
        self.wumpus_dead = False
        self.can_shoot = True # always a boolean
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def getAction( self, stench, breeze, glitter, bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        '''
        print(self.position, self.dir)
        stateArr = [stench, breeze, glitter, bump, scream]
        print(stateArr)
        '''

        if(self.turning):
            return self.change_dir(self.goal_dir)

        '''
        if(self.backtrack):
            if(self.turn_counter < 2):
                return self.turn_left()
            else:
                return self.move_forward()
        '''
        is_dangerous = True if breeze or stench else False

        if(glitter):
            self.got_gold()
            return self.grab()
            #on the coordinate where Gold is
        
        # If you have the gold and you're at the beginning, just climb.
        if(self.has_gold() and self.get_position() == (0,0) ):
            return self.climb()
        
        if(scream): 
            self.wumpus_dead = True

        if(is_dangerous):
            if(self.get_move_count() == 0):
                if(breeze):
                    self.inc_move_count()
                    return self.climb()
                elif(stench):
                    self.shoot()
            else:
                self.goal_dir = self.oppdir(self.dir)
                return self.change_dir(self.goal_dir)
        # if (we're on the first block AND there's no immediate unsafe dangers)
        #    move forward
        elif(self.get_move_count() == 0):
            self.inc_move_count()
            return self.move_forward()
    
        if(bump):
            self.goal_dir = self.oppdir(self.dir)
            return self.change_dir(self.goal_dir)
        

        if(scream and self.wumpus_dead == False): 
            self.wumpus_dead = True
            #'Wumpus is dead (only percieved on following turn)
        return self.move_forward()
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    # ======================================================================
    # YOUR CODE BEGINS
    # ======================================================================
    def get_dir(self):
        return self.dir

    def get_position(self):
        return self.position

    def get_move_count(self):
        return self.move_count

    def inc_move_count(self):
        self.move_count += 1
    
    def oppdir(dir_s):
        if(dir_s == 'e'):
            return 'w'
        if(dir_s == 's'):
            return 'n'
        if(dir_s == 'w'):
            return 'e'
        if(dir_s == 'n'):
            return 's'

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
        print((self.position, self.dir))
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
        if(backward):
            self.turn_counter += 1
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
        if(backward):
            self.turn_counter += 1
        return Agent.Action.TURN_RIGHT
    
    def climb(self):
        return Agent.Action.CLIMB

    def has_gold(self):
        if self.gold_obtained:
            return True
        return False

    def got_gold(self):
        self.gold_obtained = True

    def can_shoot(self):
        if self.can_shoot:
            return True
        return False

    def shoot(self):
        if(self.can_shoot):
            self.can_shoot = False
        else:
            print("Can't shoot!")
        return Agent.Action.SHOOT

    def grab(self):
        return Agent.Action.GRAB

    def shoot(self):
        if(self.can_shoot == True):
            self.can_shoot = False
            return Agent.Action.SHOOT
        else:
            print("Can't shoot!")

    def get_next_position(self, old_pos, direc):
        pos = old_pos
        new_pos = (0,0)
        if(direc == 's'):
            new_pos = (pos[0], pos[1] - 1)
        if(direc == 'n'):
            new_pos = (pos[0], pos[1] + 1)
        if(direc == 'e'):
            new_pos = (pos[0] + 1, pos[1])
        if(direc == 'w'):
            new_pos = (pos[0] - 1, pos[1])
        return new_pos
    
 

    def change_dir(self, goal_dir):
        if self.dir == goal_dir:
            self.turning = False   
        else:
            self.turning = True
            if(oppdir(self.dir) == goal_dir):
                return self.turn_left()
            elif(self.dir == 'e' and goal_dir == 'n'):
                return self.turn_left()
            elif(self.dir == 'e' and goal_dir == 's'):
                return self.turn_right()
            elif(self.dir == 'w' and goal_dir == 'n'):
                return self.turn_right()
            elif(self.dir == 'w' and goal_dir == 's'):
                return self.turn_left()
            elif(self.dir == 'n' and goal_dir == 'e'):
                return self.turn_right()
            elif(self.dir == 'n' and goal_dir == 'w'):
                return self.turn_left()
            elif(self.dir == 's' and goal_dir == 'e'):
                return self.turn_right()
            elif(self.dir == 's' and goal_dir == 'w'):
                return self.turn_left()
    

    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================
