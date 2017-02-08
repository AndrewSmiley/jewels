# jewels


##A short report that describes who in your group implemented which portions (if you worked in a group), what you learned from the assignment, how easy or challenging the assignment was

##An explanation of your heuristic and whether you felt it improved the search and whether a better heuristic might help

```
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
```
**What It Does**  
Essentially, what my hueristic does is done in 3 parts. The first, is to determine if the node we are currently looking at is the goal state. This will return the highest score. The next, is to generate the children of the node we are looking at, if the a child of the current node contains the goal state, we return the second highest score for this node. The two aforementioned scorings ensure that we always select the node that is the goal state or the node in which the goal state will be in the next recursion. Finally, since we've generated children for the node (and python being a pass by reference language), we kill the children of the node so we do not generate duplicate children for the node. Finally, if neither of the above options are hit, we look space by space to determine how close a given space on the grid (space= grid[y][x]) to the goal state at that same position. I.e. if `node.data[y][x] == 'D'` and `goal_state[y][x]=='E'` then the score for that space is 1, or how many moves until the goal state is reached

**Did It Improve Search?**  
In short, yes. I believe the hueristic improved the search. However, don't take my word for it, the resulting data speaks for itself. In some cases, boasting a 2223% improvement over DFS. 

**Would A Better Hueristic Help?**  
A better hueristic would have helped, absolutely. Time permitting, I would have liked to tweak the 3rd check in the hueristic to not look at individual spaces, but rather look at moves as a whole by their bounds. There is a function in `jewels.py` called `find_bounds(pos)` that determines, given a position, what spaces around it will be impacted. I would like to improve the hueristic to not look at individual spaces, but rather entire moves to determine what percentatge of the next move would be a part of the goal state. However, this is not entirely accurate given that the bounds of a move can overlap with other moves, howevr, it would be a first step. 

