__author__ = 'Andrew'
import copy
import sys
sys.setrecursionlimit(100000)
_states = ['D', 'R', 'E']
_tree = []
_found_states= []
_map={0:{'y':0, 'x':0},1:{'y':0, 'x':1}, 2:{'y':0, 'x':2}, 3:{'y':1, 'x':0}, 4:{'y':1, 'x':1}, 5:{'y':1, 'x':2},
      6: {'y': 2, 'x': 0}, 7:{'y':2, 'x':1}, 2:{'y':2, 'x':2}}
_nodes = []
class Node(object):
    def __init__(self,data, pos_value=0, parent=None):
        self.parent = parent
        self.data = data
        self.pos_value = pos_value
        self.children = []

    def add_child(self, child):
        self.children.append(child)


def get_next_state(state):
    return _states[0]  if _states.index(state) == (len(_states)-1) else _states[_states.index(state)+1]

def grid_to_key(grid):
    _ = []
    for i in range(0, len(grid)):
        for j in range(0,len(grid[i])):
            _.append(grid[i][j])
    # _ = [''.join(x) for x in _]
    return ''.join(_)

#get pos as a 0-8 val
def pos_to_value(pos):
    for k, v in _map.iteritems():
        if pos['x'] == v['x'] and pos['y']==v['y']:
            return k

def create_grid():
    grid = []
    for i in range(0, 3):
        grid.append([])
        for j in range(0,3):
            grid[i].append('D')
    return grid


def hueristic(grid):
    pass

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

def update_grid(grid, pos, bounds):
    grid[pos['y']][pos['x']] = get_next_state(grid[pos['y']][pos['x']])
    if 'up' in bounds:
        grid[bounds['up']][pos['x']] =  get_next_state(grid[bounds['up']][pos['x']])
    if 'down' in bounds:
        grid[bounds['down']][pos['x']] = get_next_state(grid[bounds['down']][pos['x']])
    if 'left' in bounds:
        grid[pos['y']][bounds['left']] = get_next_state(grid[pos['y']][bounds['left']])
    if 'right' in bounds:
        grid[pos['y']][bounds['right']] = get_next_state(grid[pos['y']][bounds['right']])


def generate_children(node):

    # if node.data == goal_state:
    #     print 'found goal state'
    #     return
    if len(node.children)==0:
        for y in range(0, len(grid)):
            for x in range(0, len(grid[y])):
                _ = copy.deepcopy(node.data)
                update_grid(_, {'y': y, 'x': x}, find_bounds({'y': y, 'x': x}))
                # if grid_to_key(_) in _found_states:
                #     continue
                # else:
                child_node = Node( _, {'y': y, 'x': x},  node)
                node.children.append(child_node)
                # _found_states.append(grid_to_key(_))




def build_tree(node, base_case, depth=1):

    #base case
    # new_node  = copy.copy(node)
    # if depth == 20:
    #     return
    if node.data == base_case:
        node.state='closed'
        print "found base"
        print "node data %s" %(node.data)
        print "base case %s" %(base_case)

        return
    #
    # for child_node in node.children:
    #     build_tree(child_node, base_case)
    #     build the children for this level
    generate_children(node, base_case)

    # if len(node.children)==0:
        # node.state == 'closed'

    for child_node in node.children:
        # _found_states.append(grid_to_key(child_node))
        build_tree(child_node, base_case)



#ok create our grid
grid = create_grid()
# def __init__(self, data, pos_value=0, state='open'):
n = Node(grid, 0, None)
# _found_states.append(grid_to_key(n.data))
goal_state_0 =[]
for i in range(0, 3):
    goal_state_0.append([])
    for j in range(0, 3):
        goal_state_0[i].append('E')
goal_state_1=[['E', 'E', 'R', ], ['E', 'R', 'E'], ['R', 'E', 'R']]

class Node(object):
    def __init__(self,data, pos_value=0, parent=None):
        self.parent = parent
        self.data = data
        self.pos_value = pos_value
        self.children = []

    def add_child(self, child):
        self.children.append(child)

moves =[]
def dfs(node, goal_state, stack, depth):
    global moves
    if len(moves) >0:
        return

    if grid_to_key(node.data) in _found_states:
        return

    if node.data == goal_state:
        n = node
        while n.parent is not None:
            moves.append(pos_to_value(n.pos_value))
            n = n.parent
        print "size: %s" %(len(stack))
        print "found len %s %s "%(len(moves), moves)
        return
    generate_children(node)

    # stack.append(node)
    if grid_to_key(node.data) in _found_states:
        stack.pop()
        print len(stack)
        return

    else:
        _found_states.append(grid_to_key(node.data))
        for child in stack[-1].children:
            if grid_to_key(child.data) in _found_states:
                continue
            else:
                stack.append(child)
                dfs(child, goal_state, stack, depth+1)
    return

#just a little utility function to generate the number of steps to the goal state at that space
def get_space_distance(space, goal):
    return _states.index(goal) - _states.index(space) if space != _states[-1] else 1 + _states.index(goal)



def hueristic(node, goal_state):
    total_score = 0
    #well, if this node is our goal give it the highest score
    if node.data == goal_state:
        return pow(9, 5)
    generate_children(node)
    #if the children of this node contain the solution, it's the next best solution
    if len (filter(lambda x: x.data == goal_state, node.children)) >0:
        return pow(9,4)
    #kill the children \M/
    del node.children[:]
    for y in range(0, len(node.data)):
        for x in range(0, len(node.data[y])):
            distance_to_goal = get_space_distance(node.data[y][x], goal_state[y][x])
            if distance_to_goal == 1:
                total_score = total_score+4
            else:
                total_score = total_score+distance_to_goal



def bfs(node, goal_state, stack, depth):


print dfs(n, goal_state_0, [n], 0)
n = Node(grid, 0, None)



print "Test"
