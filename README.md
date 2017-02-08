# jewels

A short report that describes who in your group implemented which portions (if you
worked in a group), what you learned from the assignment, how easy or challenging the
assignment was

An explanation of your heuristic and whether you felt it improved the search and whether
a better heuristic might help

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