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
from pprint import pprint

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
        self.post_bump = False
        self.bump_counter = 0
        self.turning = False
        self.move_count = 0
        self.has_gold = False
        self.wumpus_alive = True
        self.can_shoot = True # always a boolean
        self.tile_info = {(0,0) : 1}
        self.visited_nodes = {(0,0): True}
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def getAction( self, stench, breeze, glitter, bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        #print(self.position, self.dir)
        stateDict = {
            'stench':stench, 'breeze':breeze, 'glitter': glitter, 'bump':bump, 'scream': scream, 'can_shoot' : self.can_shoot, 
            'turning': self.turning, 'goal_dir': self.goal_dir, 'has_gold': self.has_gold
        }

        pprint(stateDict)
        pprint(self.visited_nodes)

        is_dangerous = True if breeze or stench else False
        #pprint(self.orientation_history)

        #print("position of last turn:", self.get_position())
        if(self.turning):
            return self.change_dir(self.goal_dir)

        

        if(self.has_gold): # only while we have the gold, will we backtrack
            #print("in has gold")
            if(len(self.orientation_history) == 0 or self.get_position() == (0,0)):
                return self.climb()
            #print("not in (0,0)")
            #backtracking to starting position
            old_hist = (self.orientation_history.pop() if self.orientation_history.__len__() > 0 else None) # ((0,0), 'e')
            #print(old_hist)
            if(old_hist is None):
                pass
            elif(old_hist[2] == 'F' and old_hist[1] == self.get_dir()):
                #turn around and move
                self.update_goal_dir(self.oppdir(self.get_dir()))
                return self.change_dir(self.goal_dir)
            elif(old_hist[2] == 'F' and old_hist[1] == self.oppdir(self.get_dir())):
                #print("backtrack move: F")
                return self.move_forward()
            elif(old_hist[2] == 'TR'):
                #print("backtrack move: TL")
                return self.turn_left()
            elif(old_hist[2] == 'TL'):
                #print("backtrack move: TR")
                return self.turn_right()

        if(not self.wumpus_alive):
            is_dangerous = True if breeze else False

        if(self.post_bump):
            self.bump_counter += 1

        if(self.tile_info[0,0] > 2):
            return self.climb()
           
        
        elif(glitter):
            self.has_gold = True
            return self.grab()
            #on the coordinate where Gold is
        if(scream): 
            self.wumpus_alive = False

        elif(bump):
            #print("inside bump")
        #might be popping at wrong time
            self.orientation_history.pop()
            self.post_bump = True
            self.recover_position()
            return self.bump_help()   

        elif(is_dangerous):
            if(self.get_move_count() == 0):
                if(breeze):
                    return self.climb()
                elif(stench and self.can_shoot):
                    return self.shoot()
            elif(self.get_position() == (0,0) and not self.can_shoot and self.tile_info[(0,0)] > 1):
                return self.climb()
            elif(breeze):
                self.post_bump = False
                self.update_goal_dir(self.oppdir(self.get_dir()))
                return self.change_dir(self.goal_dir)
            elif(stench):
                #greedy right now, implement heuristics at higher level
                if(self.wumpus_alive and self.can_shoot):
                    return self.shoot()
                elif(self.wumpus_alive and not self.can_shoot):
                    self.update_goal_dir(self.oppdir(self.get_dir()))
                    return self.change_dir(self.goal_dir)
                elif(not self.wumpus_alive and not self.can_shoot):
                    return self.move_forward()
                else:
                    self.update_goal_dir(self.oppdir(self.get_dir()))
                    return self.change_dir(self.goal_dir)
            else:
                self.update_goal_dir(self.oppdir(self.get_dir()))
                return self.change_dir(self.goal_dir)
                
        elif(self.post_bump and self.bump_counter >= 3):
            #handle this stuff in function
            #print("inside post_bump")
            return self.post_bump_move()

        '''elif(bump):
            #print("inside bump")
            self.post_bump = True
            self.recover_position()
            return self.bump_help()     '''       
            

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
        if(not self.has_gold):
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
        if(not self.has_gold):
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
        if(not self.has_gold):
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
            return self.move_forward()
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
                return self.turn_left()
            elif(self.dir == 's' and goal_dir == 'w'):
                return self.turn_right()
            else:
                return self.turn_left()
        if(not self.turning):
            return self.move_forward()
    

    def bump_help(self):
        self.bump_counter += 1
        if(self.position == (0,0) and self.dir == 'w'):
            return self.turn_right()
        elif(self.position[0] < self.position[1] and self.dir == 'w' and self.post_bump):
           return self.turn_right()
        elif(self.position[0] > self.position[1] and self.dir == 'e'):
            return self.turn_left()
        elif(self.position[0] > self.position[1] and self.dir == 's'):
            return self.turn_right()
        elif(self.position[0] < self.position[1] and self.dir == 'n'):
            return self.turn_right()
        elif(self.position[0] < self.position[1] and self.dir == 'w'):
            return self.turn_left() 
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

    def post_bump_move(self):
        self.bump_counter = 0
        self.post_bump = False
        if(self.get_position()[0] == self.get_position()[1]):
            return self.turn_left()
        if(self.get_dir() == 'w'):
            return self.move_forward()
        if(self.get_dir() == 's'):
            return self.move_forward()   
        if(self.get_position()[0] < self.get_position()[1]):
            return self.turn_right()
        elif(self.get_position()[0] > self.get_position()[1]):
            return self.turn_left()

  
    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================