from src.World import *
import random


class Node:
    def __init__(self, point: Vector2D):
        # self.value = value
        self.point = point
        self.parent = None
        self.H = 0
        self.G = 0
    # def move_cost(self,other):
    #     return 0 if self.value == '.' else 1


def children(point: Vector2D, obs: list):
    out = set()
    if (point.point+Vector2D(0, 1)) not in obs:
        n = Node(point.point+Vector2D(0, 1))
        out.add(n)
    if (point.point+Vector2D(1, 0)) not in obs:
        n = Node(point.point+Vector2D(1, 0))
        out.add(n)
    if (point.point+Vector2D(0, -1)) not in obs:
        n = Node(point.point+Vector2D(0, -1))
        out.add(n)
    if (point.point+Vector2D(-1, 0)) not in obs:
        n = Node(point.point+Vector2D(-1, 0))
        out.add(n)

    return out


def manhattan(point, point2):
    return point.point.dist(point2)


def aStar(start: Node,  goal: Vector2D,  obs: list):
    # The open and closed sets
    openset = set()
    closedset = set()

    # Current point is the starting point
    current = start

    # Add the starting point to the open set
    openset.add(current)

    counter = 0

    # While the open set is not empty
    while openset:
        counter += 1
        if counter > 80:  # resideG
            return []

        # Find the item in the open set with the lowest G + H score
        current = min(openset, key=lambda o: o.G +
                      o.H)                 # resideG

        # If it is the item we want, retrace the path and return it
        if current.point == goal:
            path = []
            while current.parent.point is not start.point:
                path.append(current.point)
                current = current.parent
            path.append(current.point)
            return path

        # Remove the item from the open set
        openset.remove(current)

        # Add it to the closed set
        closedset.add(current)

        # Loop through the node's children/siblings
        for node in children(current, obs):
            # If it is already in the closed set, skip it
            if node in closedset:
                continue

            # Otherwise if it is already in the open set
            if node in openset:
                # Check if we beat the G score
                new_g = current.G + 1  # current.move_cost(node)
                if node.G > new_g:
                    # If so, update the node to have a new parent
                    node.G = new_g
                    node.parent = current
            else:
                # If it isn't in the open set, calculate the G and H score for the node
                node.G = current.G + 1  # current.move_cost(node)
                node.H = manhattan(node, goal)

                # Set the parent to our current item
                node.parent = current

                # Add it to the set
                openset.add(node)

    # Throw an exception if there is no path
    # raise ValueError('No Path Found')
    return []


def my_fast_selection(next_head: list, goal: Vector2D, obstacle_1: list, obstacle_2: list):

    next_head_price = [0, 0, 0, 0]
    actions = ['d', 'r', 'u', 'l']
    h_number = -1
    for h in next_head:
        h_number += 1

        if h in obstacle_1:
            next_head_price[h_number] += 60                         # resideG
        if h in obstacle_2:
            next_head_price[h_number] += 15*obstacle_2.count(h)     # resideG
        next_head_price[h_number] += 2*goal.dist(h)

    return next_head_price

# returns a list of numbers that shows how bad is the next cituation with concidering the obstacles


def check_next(pos: Vector2D, obs1, obs2):
    out = [0, 0, 0, 0]

    next_head = []
    next_head.append(pos + Vector2D(1, 0))
    next_head.append(pos + Vector2D(0, 1))
    next_head.append(pos + Vector2D(-1, 0))
    next_head.append(pos + Vector2D(0, -1))
    next_head_price = [0, 0, 0, 0]

    obs1.append(pos)
    for i in range(4):
        if next_head[i] in obs1:
            out[i] += 100                   # resideG

        else:
            if next_head[i] in obs2:
                out[i] += 15                # resideG

            temp_next = [next_head[i]+Vector2D(1, 0)]
            temp_next.append(next_head[i]+Vector2D(0, 1))
            temp_next.append(next_head[i]+Vector2D(-1, 0))
            temp_next.append(next_head[i]+Vector2D(0, -1))

            num_surrounded = 0
            for j in range(4):
                if temp_next[j] in obs1:
                    num_surrounded += 4         # resideG

            for j in range(4):
                if temp_next[j] in obs2:
                    num_surrounded += 1         # resideG

            # resideG
            if num_surrounded > 14:
                out[i] += 40
            elif num_surrounded > 10:
                out[i] += 18
            elif num_surrounded > 6:
                out[i] += 9

    return out


def get_action(world: World):
    goal = world.goal_position
    head_pos = world.get_self().get_head()

    next_head = []
    next_head.append(head_pos + Vector2D(1, 0))
    next_head.append(head_pos + Vector2D(0, 1))
    next_head.append(head_pos + Vector2D(-1, 0))
    next_head.append(head_pos + Vector2D(0, -1))
    next_head_price = [0, 0, 0, 0]
    actions = ['d', 'r', 'u', 'l']

    if goal in next_head:
        for i in range(4):
            if next_head[i] is goal:
                return actions[i]

    obstacle_1 = []
    obstacle_2 = []

    obstacle_1 += world.get_walls()

    min_dist = 1000
    my_dist = goal.dist(head_pos)
    for s in world.snakes:
        t = world.snakes[s].get_head().dist(goal)
        if min_dist > t:
            min_dist = t

        snake_temp = world.snakes[s]
        snake_temp_head = world.snakes[s].get_head()

        obstacle_1 += snake_temp.get_body()

        if snake_temp_head is not head_pos:
            obstacle_2.append(snake_temp_head + Vector2D(1, 0))
            obstacle_2.append(snake_temp_head + Vector2D(0, 1))
            obstacle_2.append(snake_temp_head + Vector2D(-1, 0))
            obstacle_2.append(snake_temp_head + Vector2D(0, -1))

    a_star = []

    if 3*min_dist < my_dist:
        # fast selection to center
        next_head_price = my_fast_selection(
            next_head, Vector2D(14, 14), obstacle_1, obstacle_2)
    elif my_dist > 25:
        # fast selection to goal
        next_head_price = my_fast_selection(
            next_head, goal, obstacle_1, obstacle_2)
    else:
        a_star = aStar(Node(head_pos), goal, obstacle_1)

        if a_star is []:
            next_head_price = my_fast_selection(
                next_head, goal, obstacle_1, obstacle_2)

    next_price = check_next(head_pos, obstacle_1, obstacle_2)
    h_number = -1
    for h in next_head:
        h_number += 1

        next_head_price[h_number] += next_price[h_number]

        # if h in obstacle_1:
        #     next_head_price[h_number] += 60
        # if h in obstacle_2:
        #     next_head_price[h_number] += 15*obstacle_2.count(h)
        if h in a_star:
            next_head_price[h_number] -= 20             # resideG

    print(next_head_price)
    print(actions)
    mini = min(next_head_price)
    for h_number in range(4):
        if next_head_price[h_number] == mini:
            return actions[h_number]
