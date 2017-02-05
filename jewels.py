__author__ = 'Andrew'
import copy
import sys
sys.setrecursionlimit(10000)
_states = ['D', 'R', 'E']
_tree = []
_found_states= []
_map={0:{'y':0, 'x':0},1:{'y':0, 'x':1}, 2:{'y':0, 'x':2}, 3:{'y':1, 'x':0}, 4:{'y':1, 'x':1}, 5:{'y':1, 'x':2},
      6: {'y': 2, 'x': 0}, 7:{'y':2, 'x':1}, 2:{'y':2, 'x':2}}
class Node(object):
    def __init__(self,data, pos_value=0, state='open'):
        # self.parent = parent
        self.data = data
        self.state =state
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
    for y in range(0, len(grid)):
        for x in range(0, len(grid[y])):
            _ = copy.deepcopy(node.data)
            update_grid(_, {'y': y, 'x': x}, find_bounds({'y': y, 'x': x}))
            if grid_to_key(_) in _found_states:
                continue
            else:
                child_node = Node( _, {'y': y, 'x': x}, 'open')
                node.children.append(child_node)
                _found_states.append(grid_to_key(_))


def build_tree(node, base_case):
    #base case
    # new_node  = copy.copy(node)
    if node.data == base_case:
        node.state='closed'
        print "found base"
        print "node data %s" %(node.data)
        print "base case %s" %(base_case)

        return

    for child_node in node.children:
        build_tree(child_node, base_case)
        #build the children for this level

    generate_children(node)
    if len(node.children)==0:
        node.state == 'closed'

    for child_node in node.children:
        build_tree(child_node, base_case)

def dfs_search(node, goal_state, next_moves):
    #base
    if len(node.children) == 0 and node.data != goal_state:
        return False
    elif len(node.children) == 0  and node.data== goal_state:
        # next_moves.append(node.pos_value)
        return True

    for child_node in node.children:
        found = dfs_search(child_node, goal_state, next_moves)
        if found:
            next_moves.append(child_node.pos_value)
            return True

    #basically if there is no match in the tree
    return False





#ok create our grid
grid = create_grid()
# def __init__(self, data, pos_value=0, state='open'):
n = Node(grid, 0, 'open' )
goal_state_0 =[]
for i in range(0, 3):
    goal_state_0.append([])
    for j in range(0, 3):
        goal_state_0[i].append('E')


build_tree(n,goal_state_0)
next_moves = []
found = dfs_search(n, goal_state_0, next_moves)
print "found: %s" %(found)
print next_moves

print "Test"
