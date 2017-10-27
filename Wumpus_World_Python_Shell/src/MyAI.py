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
import random

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
        self.has_gold = False
        self.wumpus_dead = False
        self.can_shoot = True # always a boolean
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def getAction( self, stench, breeze, glitter, bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        print(self.position, self.dir)
        stateArr = [stench, breeze, glitter, bump, scream]
        print(stateArr)

        if(self.turning):
            return self.change_dir(self.goal_dir)

        is_dangerous = True if breeze or stench else False

        if(glitter):
            self.has_gold = True
            return self.grab()
            #on the coordinate where Gold is
        if(scream): 
            self.wumpus_dead = True
'''
        if(stench):
            x = random.randint(0,2)
            if(x == 0):
                self.move_forward()
            if(x == 1):
                self.turn_left()
            if(x == 2):
                self.turn_right()
            #next to Wumpus

        if(breeze): 
            x = random.randint(0,2)
            if(len(self.orientation_history) == 0):
                return Agent.Action.CLIMB
            else:
                if(x == 0):
                    self.move_forward()
                if(x == 1):
                    self.turn_left()
                if(x == 2):
                    self.turn_right()
            #next to Pit
'''
        if(is_dangerous):
            if(self.get_move_count() == 0):
                if(breeze):
                    self.inc_move_count()
                    return self.climb()
                elif(stench):
                    self.shoot()
            else:
                return self.move_back()

        #if (we're on the first block AND there's no immediate unsafe dangers)
        #   move forward
        elif(self.get_move_count() == 0):
            self.inc_move_count()
            return self.move_forward()
    
        if(bump):
            self.goal_dir = self.oppdir(self.dir)
            return self.change_dir(self.goal_dir)
        

        return self.move_forward()
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

    def get_move_count(self):
        return self.move_count

    def inc_move_count(self):
        self.move_count += 1

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