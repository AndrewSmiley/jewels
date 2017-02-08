__author__ = 'Andrew Smiley'
import copy
import sys
#python is wonky about recursion, have to increase the recursion limit
sys.setrecursionlimit(100000)
#just a list of our state progression to allow us to move from one space state to the next
_states = ['D', 'R', 'E']
#the states we've found in our search
_found_states= []
#this is no longer needed, however, this is a mapping between a space on the grid[y][x] to an absolute position, i.e. 4,5,6 etc
_map={0:{'y':0, 'x':0},1:{'y':0, 'x':1}, 2:{'y':0, 'x':2}, 3:{'y':1, 'x':0}, 4:{'y':1, 'x':1}, 5:{'y':1, 'x':2},
      6: {'y': 2, 'x': 0}, 7:{'y':2, 'x':1}, 2:{'y':2, 'x':2}}

#this is our node object
class Node(object):
    def __init__(self,data, pos_value=0, parent=None):
        #the parent of the node
        self.parent = parent
        #the grid at the node
        self.data = data
        #the value of the move that got us to this state
        self.pos_value = pos_value
        #the children of the node
        self.children = []
    #add a child to the node
    def add_child(self, child):
        self.children.append(child)

#calculate the next value for the space
def get_next_state(state):
    return _states[0]  if _states.index(state) == (len(_states)-1) else _states[_states.index(state)+1]

#convert a grid (list of lists) to a dictionary key
def grid_to_key(grid):
    _ = []
    for i in range(0, len(grid)):
        for j in range(0,len(grid[i])):
            _.append(grid[i][j])
    return ''.join(_)

#get pos as a 0-8 val
def pos_to_value(pos):
    #just iterate through the map and return the key which is the position value
    for k, v in _map.iteritems():
        if pos['x'] == v['x'] and pos['y']==v['y']:
            return k

#build out a clean grid, i.e. [[d,d,d], [d,d,d], [d,d,d]]
def create_grid():
    #just an iteration to fill
    grid = []
    for i in range(0, 3):
        grid.append([])
        for j in range(0,3):
            grid[i].append('D')
    return grid


#this function goes through and finds the bounds of the move,
#i.e. move in pos 4 changes the values on itself, 1,3,5 and 7
def find_bounds(pos):
    #up down left right
    bounds = {}
    #we know it's centered
    if pos['y']==1:
        bounds['up'] =0
        bounds['down']=2
    if pos['x']==1:
        bounds['left']=0
        bounds ['right']=2
    if pos['y']==0:
        bounds['down']=1
    if pos['x']==0:
        bounds['right']=1
    if pos['y']==2:
        bounds['up']=1
    if pos['x']==2:
        bounds['left']=1

    return bounds

#this updates the grid to the next state based upon the bounds passed in
def update_grid(grid, pos, bounds):
    #update the selected space
    grid[pos['y']][pos['x']] = get_next_state(grid[pos['y']][pos['x']])
    #just determine if N,S,E,W should be updated to the next space and get that updated value
    if 'up' in bounds:
        grid[bounds['up']][pos['x']] =  get_next_state(grid[bounds['up']][pos['x']])
    if 'down' in bounds:
        grid[bounds['down']][pos['x']] = get_next_state(grid[bounds['down']][pos['x']])
    if 'left' in bounds:
        grid[pos['y']][bounds['left']] = get_next_state(grid[pos['y']][bounds['left']])
    if 'right' in bounds:
        grid[pos['y']][bounds['right']] = get_next_state(grid[pos['y']][bounds['right']])

#this function generatees the children of the node
def generate_children(node):
    #make sure it does not already have children
    if len(node.children)==0:
        #if it does, go space by space and generate the values
        for y in range(0, len(node.data)):
            for x in range(0, len(node.data[y])):
                #this is python so we have to copy the parent node explicitly
                _ = copy.deepcopy(node.data)
                #update the grid at position we are iterated on
                update_grid(_, {'y': y, 'x': x}, find_bounds({'y': y, 'x': x}))
                #create the child node
                child_node = Node( _, {'y': y, 'x': x},  node)
                #append to the node
                node.children.append(child_node)

#this is our depth first search function
#node: the starting node
#goal_state: the desired goal state
#stack: our "runtime stack" of nodes we've dove into
def dfs(node, goal_state, stack):
    global viewed_states
    viewed_states = viewed_states +1
    #make moves a global so we can work with the recursion
    global moves
    #if we've already found a goal state, moves will be >0 ergo exit
    if len(moves) >0:
        return
    #if the current node is the goal node we can calculate the moves to get there and then exit
    if node.data == goal_state:
        n = node
        while n.parent is not None:
            #append the move and update the node
            moves.append(pos_to_value(n.pos_value))
            n = n.parent
        #ouput the result
        print "Found %s in Depth First Search:\nTook %s moves of %s states visited\n\n"%(goal_state,len(moves), viewed_states)
        return
    #generate children for the current node
    generate_children(node)

    #if we've already looked at this node, then go back to the previous node and go to the next child
    if grid_to_key(node.data) in _found_states:
        stack.pop()
        return

    else:
        #append the current node to the list of found nodes
        _found_states.append(grid_to_key(node.data))
        #iterate over the children in the current node
        for child in stack[-1].children:
            #if we've already found this child to be a dead end, move to the next but increment the number of visited states
            if grid_to_key(child.data) in _found_states:
                viewed_states = viewed_states +1
                continue
            else:
                #otherwise, add the child to the stack and recurse
                stack.append(child)
                dfs(child, goal_state, stack)
    return
#this is our best first search function
#node: the starting node
#goal_state the goal state to find
def bfs(node, goal_state):
    global viewed_states
    viewed_states = viewed_states +1
    #make moves accessibly globally
    global moves

    #if we've already found a goal state, moves will be >0 ergo exit
    if len(moves) >0:
        return
    #if the current node is the goal node we can calculate the moves to get there and then exit
    if node.data == goal_state:
        n = node
        while n.parent is not None:
            moves.append(pos_to_value(n.pos_value))
            n = n.parent
        # print "size: %s" %(len(stack))
        print "Found %s in Best First Search:\nTook %s moves of %s states visited\n\n"%(goal_state, len(moves), viewed_states)
        return

    #if we've already looked at this node, then go back
    if grid_to_key(node.data) in _found_states:
        return
    else:
        #generate children of the node
        generate_children(node)
        #sort the children by largest hueristic value
        node.children = sorted(node.children, key=lambda x: hueristic(x, goal_state), reverse=True)
        #add the current node to the list of viewed states
        _found_states.append(grid_to_key(node.data))
        #iterate over the children, leftmost (i.e. first) is the one with highest hueristic value
        for child in node.children:
            #if the child has already been viewed but it's a dead end, increment number of viewed states but move to the next
            if grid_to_key(child.data) in _found_states:
                viewed_states = viewed_states +1
                continue
            else:
                #if not, recurse!
                bfs(child, goal_state)
    return


#just a little utility function to generate the number of steps to the goal state at that space
#space: the value at a particular spsace
#the goal value at a particular space
def get_space_distance(space, goal):
    return _states.index(goal) - _states.index(space) if space != _states[-1] else 1 + _states.index(goal)


#our hueristic function
#node: the node we are calculating score for
#goal_state: the desired goal state
def hueristic(node, goal_state):
    #total score for incrementing
    total_score = 0
    #well, if this node is our goal give it the highest score
    if node.data == goal_state:
        return pow(9, 5)
    #generate the children
    generate_children(node)
    #if the children of this node contain the solution, it's the next best solution
    if len (filter(lambda x: x.data == goal_state, node.children)) >0:
        return pow(9,4)
    #kill the children \M/
    del node.children[:]
    #iterate through and calculate a given score based upon the number of steps it will take a space to reach the goal space value
    for y in range(0, len(node.data)):
        for x in range(0, len(node.data[y])):
            distance_to_goal = get_space_distance(node.data[y][x], goal_state[y][x])
            #if the next move will get us there, we want to give the highest value
            if distance_to_goal == 1:
                total_score = total_score+4
            else:
                #otherwise, we score the distance, which will not be > 3 moves
                total_score = total_score+distance_to_goal
    return total_score




moves =[]
#ok create our grid
grid = create_grid()
# def __init__(self, data, pos_value=0, state='open'):
n = Node(grid, 0, None)
#create the first goal state, yes, i could optimize this.
#wrote this code at 3:42AM on saturday morning during the hackathon event, judge me
# goal_state_0 =[]
# for i in range(0, 3):
#     goal_state_0.append([])
#     for j in range(0, 3):
#         goal_state_0[i].append('E')
#fuck it, i changed it.
#anyway, here's our goal states to search for
goal_state_0=[['E', 'E', 'E', ], ['E', 'E', 'E'], ['E', 'E', 'E']]
goal_state_1=[['E', 'E', 'R', ], ['E', 'R', 'E'], ['R', 'E', 'R']]
goal_state_2=[['R', 'R', 'E', ], ['R', 'E', 'R'], ['E', 'R', 'R']]
goal_state_3=[['R', 'D', 'R', ], ['D', 'R', 'D'], ['R', 'D', 'R']]

#do all the searches
#create viewed states
viewed_states = 0
dfs(n, goal_state_0, [n])
#reset moves and found states
viewed_states = 0
moves= []
_found_states =[]
new_node = Node(grid, 0, None)
bfs(new_node, goal_state_0)
viewed_states = 0
moves= []
_found_states =[]
n = Node(grid, 0, None)
dfs(n, goal_state_1, [n])
#reset moves and found states
viewed_states = 0
moves= []
_found_states =[]
new_node = Node(grid, 0, None)
bfs(new_node, goal_state_1)
viewed_states = 0
moves= []
_found_states =[]
n = Node(grid, 0, None)
dfs(n, goal_state_2, [n])
#reset moves and found states
viewed_states = 0
moves= []
_found_states =[]
new_node = Node(grid, 0, None)
bfs(new_node, goal_state_2)
viewed_states = 0
moves= []
_found_states =[]
n = Node(grid, 0, None)
dfs(n, goal_state_3, [n])
#reset moves and found states
viewed_states = 0
moves= []
_found_states =[]
new_node = Node(grid, 0, None)
bfs(new_node, goal_state_3)
