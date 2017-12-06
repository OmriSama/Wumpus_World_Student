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
        self.max_x = 7
        self.min_x = 0
        self.max_y = 7
        self.min_y = 0
        self.post_bump = False
        self.bump_counter = 0
        self.turning = False
        self.move_count = 0
        self.has_gold = False
        self.wumpus_alive = True
        self.can_shoot = True # always a boolean
        self.just_shot = False
        self.tile_info = {(0,0) : 1}
        self.tracker = {}
        self.depth = 0
        self.predecessor = {}
        self.destination = ()
        self.post_inc_depth = False
        self.wumpus_tile = ()
        self.wumpus_tracker = {}
        self.stench_update_counter = 0
        self.handling_wumpus = False

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

        is_dangerous = True if breeze or stench else False
        if(not self.wumpus_alive):
            stench = False
        self.check_depth()
        if(self.turning):
            return self.change_dir(self.goal_dir)

        

        if(self.has_gold): # only while we have the gold, will we backtrack
            if(len(self.orientation_history) == 0 or self.get_position() == (0,0)):
                return self.climb()
            #backtracking to starting position
            old_hist = (self.orientation_history.pop() if self.orientation_history.__len__() > 0 else None) # ((0,0), 'e')
            if(old_hist is None):
                pass
            elif(old_hist[2] == 'F' and old_hist[1] == self.get_dir()):
                #turn around and move
                self.update_goal_dir(self.oppdir(self.get_dir()))
                return self.change_dir(self.goal_dir)
            elif(old_hist[2] == 'F' and old_hist[1] == self.oppdir(self.get_dir())):
                return self.move_forward()
            elif(old_hist[2] == 'TR'):
                return self.turn_left()
            elif(old_hist[2] == 'TL'):
                return self.turn_right()

        if(scream):
            stench = False 
            self.wumpus_alive = False

        if(not self.wumpus_alive):
            is_dangerous = True if breeze else False

        if(self.post_bump):
            self.bump_counter += 1

        if(self.tile_info[0,0] > 2):
            return self.climb()
        if(self.get_position() == (0,0) and self.climb_check()):
            return self.climb()
        if(self.get_position() == (0,0) and self.dir == 's'):
            return self.climb()

        elif(glitter):
            self.has_gold = True
            return self.grab()
            #on the coordinate where Gold is
        if(bump):
            self.orientation_history.pop()
            self.post_bump = True
            self.recover_position()
            self.recover_depth()
            self.bump_info()     
            self.clean_pred()  
            self.clean_tracker()

        elif(is_dangerous):
            self.post_bump = False
            self.bump_counter = 0
            if(self.get_move_count() == 0):
                if(breeze):
                    return self.climb()
                elif(stench and self.can_shoot):
                    return self.shoot()
            elif(self.get_position() == (0,0) and (not self.can_shoot) and (self.tile_info[(0,0)] > 1)):
                return self.climb()
            elif(stench):
                if(self.stench_update_counter == 0):
                    if(not breeze):
                        self.update_tracker()
                    self.handle_stench_tracking()
                #if wumpus tile != () then kill wumpus
                if(self.wumpus_tile != ()):
                    return self.handle_wumpus()
                else:
                    return self.go_to_predecessor()
            elif(breeze):
                self.post_inc_depth = False
                self.breeze_update_tracker()     
                #'not stench' there because havent been keeping track of wumpus           
                if(self.tile_info[self.get_position()] <= 2):
                    self.tracker_based_move()
                    return self.go_to_adj(self.destination)
                else:
                    return self.go_to_predecessor()                       
            else:
                return self.go_to_predecessor()
   
        if(not bump and not breeze):
            self.update_tracker()  
        self.just_shot = False
        if(self.change_destination() == 0):
            return self.change_depth()
        return self.go_to_adj(self.destination)
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
        self.stench_update_counter = 0 
        self.update_predecessor()
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
            self.just_shot = True
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
        if(self.get_position() == (0,0) and self.dir == 'w'):
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
            self.post_bump = False
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
        if(self.get_position()[0] < self.get_position()[1]):
            return self.turn_right()
        if(self.get_dir() == 'e'):
            return self.move_forward()
        if(self.get_dir() == 'w'):
            return self.move_forward()
        if(self.get_dir() == 's'):
            return self.move_forward()   
        elif(self.get_position()[0] > self.get_position()[1]):
            return self.turn_left()

    def update_tracker(self):
        # look at all 5 possible tiles associated with a move and update tracker
        x = self.get_position()[0]
        y = self.get_position()[1]
      
        no_pit = (-1, 'NP')
        
        self.tracker[x,y] = no_pit
        
        if((x+1,y) not in self.tile_info):
            if(self.in_bounds(x+1,y)):
                self.tracker[x+1,y] = no_pit
        if((x-1,y) not in self.tile_info):
            if(self.in_bounds(x-1,y)):
                self.tracker[x-1,y] = no_pit
        if((x,y+1) not in self.tile_info):
            if(self.in_bounds(x,y+1)):
                self.tracker[x,y+1] = no_pit
        if((x,y-1) not in self.tile_info):
            if(self.in_bounds(x,y-1)):
                self.tracker[x,y-1] = no_pit


    def breeze_update_tracker(self):
        x = self.get_position()[0]
        y = self.get_position()[1]
        base = (1, 'PP')

        if((x+1,y) not in self.tracker):
            if(self.in_bounds(x+1,y)):
                self.tracker[x+1,y] = base
        elif((x+1,y) in self.tracker):
            if(self.tracker[x+1,y][1] != 'NP'):
                self.tracker[x+1,y] = (self.tracker[x+1,y][0]+1, self.tracker[x+1,y][1])
        if((x-1,y) not in self.tracker):
            if(self.in_bounds(x-1,y)):
                self.tracker[x-1,y] = base
        elif((x-1,y) in self.tracker):
            if(self.tracker[x-1,y][1] != 'NP'):
                self.tracker[x-1,y] = (self.tracker[x-1,y][0]+1, self.tracker[x-1,y][1])
        if((x,y+1) not in self.tracker):
            if(self.in_bounds(x,y+1)):
                self.tracker[x,y+1] = base
        elif((x,y+1) in self.tracker):
            if(self.tracker[x,y+1][1] != 'NP'):
                self.tracker[x,y+1] = (self.tracker[x,y+1][0]+1, self.tracker[x,y+1][1])
        if((x,y-1) not in self.tracker):
            if(self.in_bounds(x,y-1)):
                self.tracker[x,y-1] = base
        elif((x,y-1) in self.tracker):
            if(self.tracker[x,y-1][1] != 'NP'):
                self.tracker[x,y-1] = (self.tracker[x,y-1][0]+1, self.tracker[x,y-1][1])


    def tracker_based_move(self):
        #updates destination based on the info from breeze/tracker
        x = self.get_position()[0]
        y = self.get_position()[1]

        if(((x+1,y) not in self.tile_info) and ((x+1,y) in self.tracker) and (self.tracker[x+1,y][1] == 'NP')):
            self.destination = (x+1,y)
        elif(((x-1,y) not in self.tile_info) and ((x-1,y) in self.tracker) and (self.tracker[x-1,y][1] == 'NP')):
            self.destination = (x-1,y)
        elif(((x,y+1) not in self.tile_info) and ((x,y+1) in self.tracker) and (self.tracker[x,y+1] == 'NP')):
            self.destination = (x,y+1)
        elif(((x,y-1) not in self.tile_info) and ((x,y-1) in self.tracker) and (self.tracker[x,y-1][1] == 'NP')):
            self.destination = (x,y-1)
        else:
            self.destination = self.predecessor[x,y]


    def go_to_predecessor(self):
        self.destination = self.predecessor[self.get_position()]
        return self.go_to_adj(self.destination)

    def get_home_help(self):
        x = self.get_position()[0]
        y = self.get_position()[1]
        dest_tile = self.predecessor[x,y]
        return self.go_to_adj(dest_tile)


    def bump_info(self):
        x = self.get_position()[0]
        y = self.get_position()[1]
        if(x <= self.max_x and self.get_dir() == 'e'):
            self.max_x = x
        if(y <= self.max_y and self.get_dir() == 'n'):
            self.max_y = y

    def update_predecessor(self):
        if(self.destination not in self.tile_info):
            self.predecessor[self.destination] = self.get_position()


    def clean_pred(self):
        pred = dict(self.predecessor)
        for key in pred:
            if(key[0] > self.max_x):
                del self.predecessor[key]
            if(key[0] < self.min_x):
                del self.predecessor[key]
            if(key[1] > self.max_y):
                del self.predecessor[key]
            if(key[1] < self.min_y):
                del self.predecessor[key]

    def clean_tracker(self):
        track = dict(self.tracker)
        for key in track:
            if(key[0] > self.max_x):
                del self.tracker[key]
            if(key[0] < self.min_x):
                del self.tracker[key]
            if(key[1] > self.max_y):
                del self.tracker[key]
            if(key[1] < self.min_y):
                del self.tracker[key]


    def go_to_adj(self, tile):
        dir = self.get_dir()
        dest_x = tile[0]
        dest_y = tile[1]
        x = self.get_position()[0]
        y = self.get_position()[1]
        if(dest_x < x):
            self.update_goal_dir('w')
            return self.change_dir(self.goal_dir)
        elif(dest_x > x):
            self.update_goal_dir('e')
            return self.change_dir(self.goal_dir)
        elif(dest_y < y):
            self.update_goal_dir('s')
            return self.change_dir(self.goal_dir)
        elif(dest_y > y):
            self.update_goal_dir('n')
            return self.change_dir(self.goal_dir)

    def change_destination(self):
        #fix post increasing depth
        #need to dtermine upon post increasing depth whether or not to make destination left or right
        x = self.get_position()[0]
        y = self.get_position()[1]
        dir = self.get_dir()
        depth = self.depth
        ret = 0
        if(y == depth):
            if(self.in_bounds(x+1,y)):
                if((x+1,y) not in self.tile_info):
                    if(self.tracker[x+1,y][1] == 'NP'):
                        ret = 1
                        self.destination = (x+1,y)
                        return ret
            if(self.in_bounds(x-1,y)):
                if((x-1,y) not in self.tile_info):
                    if(self.tracker[x-1,y][1] == 'NP'):
                        ret = 1
                        self.destination = (x-1,y)
                        return ret
        return ret



    def change_depth(self):
        #finnicky
        x = self.get_position()[0]
        y = self.get_position()[1]
        dir = self.get_dir()
        if((x,y+1) not in self.tile_info):
            if(self.in_bounds(x,y+1)):
                if(self.tracker[x,y+1][1] == 'NP'):
                    return self.increase_depth()
                elif(self.in_bounds(x,y-1)):
                    if(self.tracker[x,y-1][1] == 'NP'):
                        return self.decrease_depth()
                else:
                    return self.go_to_predecessor()
            elif((x,y-1) not in self.tile_info):
                if(self.tracker[x,y-1][1] == 'NP'):
                    return self.decrease_depth()
            else:
                return self.go_to_predecessor()
        elif((x,y-1) not in self.tile_info):
            if(self.in_bounds(x,y-1)):
                if(self.tracker[x,y-1][1] == 'NP'):
                    return self.decrease_depth()
            else:
                return self.go_to_predecessor()
        else:
            return self.go_to_predecessor()


    def increase_depth(self):
        x = self.get_position()[0]
        y = self.get_position()[1]
        self.depth += 1
        self.post_inc_depth = True
        self.destination = (x,y+1)
        return self.go_to_adj(self.destination)
        #self.update_goal_dir('n')
        #return self.change_dir(self.goal_dir)

    def decrease_depth(self):

        x = self.get_position()[0]
        y = self.get_position()[1]
        self.depth -= 1
        self.destination = (x,y-1)
        return self.go_to_adj(self.destination)
        #self.update_goal_dir('s')
        #return self.change_dir(self.goal_dir)



    def in_bounds(self, a, b):
        x = a
        y = b
        ret = True
        if((x > self.max_x) or (x < self.min_x)):
            ret = False
        if((y > self.max_y) or (y < self.min_y)):
            ret = False
        return ret

    def track_wumpus(self):
        x = self.get_position()[0]
        y = self.get_position()[1]

        if((x+1,y) not in self.tile_info):
            if(self.in_bounds(x+1,y)):
                if((x+1,y) not in self.wumpus_tracker):
                    self.wumpus_tracker[x+1,y] = 1
                else:
                    self.wumpus_tracker[x+1,y] += 1
        if((x-1,y) not in self.tile_info):
            if(self.in_bounds(x-1,y)):
                if((x-1,y) not in self.wumpus_tracker):
                    self.wumpus_tracker[x-1,y] = 1
                else:
                    self.wumpus_tracker[x-1,y] += 1
        if((x,y+1) not in self.tile_info):
            if(self.in_bounds(x,y+1)):
                if((x,y+1) not in self.wumpus_tracker):
                    self.wumpus_tracker[x,y+1] = 1
                else:
                    self.wumpus_tracker[x,y+1] += 1
        if((x,y-1) not in self.tile_info):
            if(self.in_bounds(x,y-1)):
                if((x,y-1) not in self.wumpus_tracker):
                    self.wumpus_tracker[x,y-1] = 1
                else:
                    self.wumpus_tracker[x,y-1] += 1


    def check_for_wumpus_tile(self):
        wump = dict(self.wumpus_tracker)
        for key in wump:
            if(wump[key] == 2):
                self.wumpus_tile = (key)

    def handle_stench_tracking(self):
        #update wumpus tracker/tile
        self.stench_update_counter = 1
        if(self.wumpus_tile == ()):
            self.track_wumpus()
            self.check_for_wumpus_tile()
    
    def handle_wumpus(self):
        self.handling_wumpus = True
        wump_x = self.wumpus_tile[0]
        wump_y = self.wumpus_tile[1]

        if(self.above(wump_x,wump_y)):
            self.update_goal_dir('n')
        elif(self.to_right_of(wump_x,wump_y)):
            self.update_goal_dir('e')
        elif(self.to_left_of(wump_x,wump_y)):
            self.update_goal_dir('w')
        elif(self.below(wump_x,wump_y)):
            self.update_goal_dir('s')
        return self.kill_wumpus()

    def kill_wumpus(self):
        goal_dir = self.goal_dir
        curr_dir = self.get_dir()
        if(goal_dir == curr_dir):
            self.wumpus_tile = ()
            if(self.can_shoot):
                return self.shoot()
        else:
            return self.face_wumpus()

    def face_wumpus(self):
        goal_dir = self.goal_dir
        curr_dir = self.get_dir()

        if(curr_dir == 'e'):
            if(goal_dir == 'n'):
                return self.turn_left()
            elif(goal_dir == 's'):
                return self.turn_right()
        elif(curr_dir == 'w'):
            if(goal_dir == 'n'):
                return self.turn_right()
            elif(goal_dir == 's'):
                return self.turn_left()
        elif(curr_dir == 'n'):
            if(goal_dir == 'e'):
                return self.turn_right()
            elif(goal_dir == 'w'):
                return self.turn_left()
        elif(curr_dir == 's'):
            if(goal_dir == 'e'):
                return self.turn_left()
            elif(goal_dir == 'w'):
                return self.turn_right()

    def recover_depth(self):
        self.depth = self.get_position()[1]
    
    def check_depth(self):
        y = self.get_position()[1]
        if(self.depth != y):
            self.depth = y

    def climb_check(self):
        x = self.get_position()[0]
        y = self.get_position()[1]
        if((x+1,y) in self.tile_info and (x,y+1) in self.tile_info):    
            return True
        else:
            return False

    def above(self, a, b):
        x = self.get_position()[0]
        y = self.get_position()[1]
        ret = False
        if(y+1 == b):
            ret = True
        return ret

    def to_right_of(self, a, b):
        x = self.get_position()[0]
        y = self.get_position()[1]
        ret = False
        if(x+1 == a):
            ret = True
        return ret

    def to_left_of(self, a, b):
        x = self.get_position()[0]
        y = self.get_position()[1]
        ret = False
        if(x-1 == a):
            ret = True
        return ret

    def below(self, a, b):
        x = self.get_position()[0]
        y = self.get_position()[1]
        ret = False
        if(y-1 == b):
            ret = True
        return ret


        


    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================