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
        self.action = ''
        self.orientation_history = [
            (self.position, self.dir, self.action)
        ]
        self.turning = False
        self.move_count = 0
        self.has_gold = False
        self.wumpus_alive = True
        self.can_shoot = True # always a boolean
        self.tile_info = {(0,0) : 1}
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def getAction( self, stench, breeze, glitter, bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        print(self.position, self.dir)
        stateDict = {
            'stench':stench, 'breeze':breeze, 'glitter': glitter, 'bump':bump, 'scream': scream, 'can_shoot' : self.can_shoot, 
            'turning': self.turning, 'goal_dir': self.goal_dir
        }
        print(stateDict)

        is_dangerous = True if breeze or stench else False

        if(not self.wumpus_alive):
            is_dangerous = True if breeze else False

        if(self.tile_info[0,0] > 2):
            return self.climb()

        if(self.has_gold):
            #backtracking to starting position
            old_tile = orientation_history.pop() # ((0,0), 'e')
            print(old_tile)
            next_pos = self.get_next_position()
            if(self.position == (0,0)):
                return self.climb()
        if(self.turning):
            return self.change_dir(self.goal_dir)

        elif(glitter):
            self.has_gold = True
            return self.grab()
            #on the coordinate where Gold is
        elif(scream): 
            self.wumpus_alive = False

        elif(is_dangerous):
            if(self.get_move_count() == 0):
                if(breeze or stench):
                    return self.climb()
            elif(breeze):
                self.update_goal_dir(self.oppdir(self.get_dir()))
                return self.change_dir(self.goal_dir)
            elif(stench):
                #greedy right now, implement heuristics at higher level
                if(self.wumpus_alive and self.can_shoot):
                    return self.shoot()
                else:
                    return self.move_forward()
            else:
                self.update_goal_dir(self.oppdir(self.get_dir()))
                return self.change_dir(self.goal_dir)

        elif(bump):
            self.recover_position()
            return self.bump_help()
       
        return self.move_forward()
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================
    def oppdir(self, dir_s):
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
    
    def update_goal_dir(self, g_dir):
        self.goal_dir = g_dir

    # Return the first and last moves that happened in the move history
    def get_latest(self):
        return self.orientation_history[-1]

    def get_first(self):
        return self.orientation_history[0]

    def move_forward(self):
        #updates the position and orientation history
        #need to make it so when agent bumps the position doesnt change preemptively 
        if(self.dir == 'e'):
            self.position = (self.position[0] + 1, self.position[1])
        if(self.dir == 'w'):
            self.position = (self.position[0] - 1, self.position[1])
        if(self.dir == 'n'):
            self.position = (self.position[0], self.position[1] + 1)
        if(self.dir == 's'):
            self.position = (self.position[0], self.position[1] - 1)
        self.orientation_history.append((self.position, self.dir, 'F'))
        if(self.position in self.tile_info):
            self.tile_info[self.position] += 1
        else:
            self.tile_info[self.get_position()] = 1
        self.inc_move_count()
        return Agent.Action.FORWARD

    def turn_left(self):
        if(self.dir == 'e'):
            self.dir = 'n'
        elif(self.dir == 'w'):
            self.dir = 's'
        elif(self.dir == 'n'):
            self.dir = 'w'
        elif(self.dir == 's'):
            self.dir = 'e'
        self.orientation_history.append((self.position, self.dir, 'TL'))
        self.inc_move_count()
        return Agent.Action.TURN_LEFT


    def turn_right(self):
        if(self.dir == 'e'):
            self.dir = 's'
        elif(self.dir == 'w'):
            self.dir = 'n'
        elif(self.dir == 'n'):
            self.dir = 'e'
        elif(self.dir == 's'):
            self.dir = 'w'   
        self.orientation_history.append((self.position, self.dir, 'TR'))
        self.inc_move_count()
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
            if(self.dir == 'e' and goal_dir == 'n'):
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
            else:
                return self.turn_left()
        if(not self.turning):
            return self.move_forward()
    

    def bump_help(self):
        if(self.position == (0,0) and self.dir == 'w'):
            return self.turn_right()
        elif(self.position[0] > self.position[1]):
            return self.turn_left()
        elif(self.position[0] < self.position[1]):
            return self.turn_right()
        elif(self.position[0] == self.position[1] and self.dir == 'e'):
            return self.turn_right()
        elif(self.position[0] == self.position[1] and self.dir == 'n'):
            return self.turn_left()
        elif(self.position[0] == self.position[1] and self.dir == 's'):
            return self.turn_left()

    def recover_position(self):
        #update the position post bump
        if(self.dir == 'e'):
            self.position = (self.position[0] - 1, self.position[1]) 
        elif(self.dir == 'w'):
            self.position = (self.position[0] + 1, self.position[1])
        elif(self.dir == 'n'):
            self.position = (self.position[0], self.position[1] - 1)
        elif(self.dir == 's'):
            self.position = (self.position[0], self.position[1] + 1)
        

    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================