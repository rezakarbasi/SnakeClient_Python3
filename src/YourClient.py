from src.World import *
import random

class Example:
    staticVariable = 5 # Access through class

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


def aStar_end(openset, start, heur):
    out = []
    for i in range(2):
        if len(openset) == 0:
            return out
        temp = min(openset, key=lambda o: o.G + heur*o.H)
        openset.remove(temp)

        if temp.parent is None:
            return out

        while(temp.parent.point is not start.point):
            temp = temp.parent
        out.append(temp.point)
    return out


def manhattan(point, point2):
    return point.point.dist(point2)


def aStar(start: Node,  goal: Vector2D,  obs: list, heurWeight, maxOpenList):
    # The open and closed sets
    openset = set()
    closedset = set()

    # Current point is the starting point
    current = start

    # Add the starting point to the open set
    openset.add(current)

    counter = 0

    charkhesh = 0

    # While the open set is not empty
    while openset:
        counter += 1
        if counter > 50:  # resideG
            return aStar_end(openset, start, (heurWeight+1)/2)

        while len(openset) > maxOpenList:
            openset.remove(max(openset, key=lambda o: o.G + heurWeight*o.H))

        # Find the item in the open set with the lowest G + H score
        charkhesh += 1
        if charkhesh == 6:
            charkhesh = 0
            # resideG
            current = min(openset, key=lambda o: heurWeight * o.G + o.H)
        elif charkhesh > 3:
            current = min(openset, key=lambda o: o.G + o.H)
        else:
            current = min(openset, key=lambda o: o.G +
                          heurWeight*o.H)                 # resideG

        # If it is the item we want, retrace the path and return it
        if current.point == goal:
            path = []
            if current.parent is None:
                return aStar_end(openset, start, (heurWeight+1)/2)

            while current.parent.point is not start.point:
                # path.append(current.point)
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
    return aStar_end(openset, start, (heurWeight+1)/2)


def my_fast_selection(next_head: list, goal: Vector2D, obstacle_1: list, obstacle_2: list):

    next_head_price = [0, 0, 0, 0]
    actions = ['d', 'r', 'u', 'l']
    h_number = -1
    for h in next_head:
        h_number += 1
        next_head_price[h_number] += 3*goal.dist(h)

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
            out[i] += 1000                   # resideG

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
            if num_surrounded > 12:
                out[i] += 100
            if num_surrounded > 11:
                out[i] += 19
            elif num_surrounded > 9:
                out[i] += 15
            elif num_surrounded > 6:
                out[i] += 10

    return out


def get_action(world: World):
    aaa=Example()
    aaa.staticVariable+=1
    print('---------------------- static ------------------------\n',aaa.staticVariable)

    goal = world.goal_position
    head_pos = world.get_self().get_head()

    next_head = []
    next_head.append(head_pos + Vector2D(1, 0))
    next_head.append(head_pos + Vector2D(0, 1))
    next_head.append(head_pos + Vector2D(-1, 0))
    next_head.append(head_pos + Vector2D(0, -1))
    next_head_price = [0, 0, 0, 0]
    actions = ['d', 'r', 'u', 'l']

    obstacle_1 = []
    obstacle_2 = []

    obstacle_1 += world.get_walls()

    min_dist = 1000
    my_dist = goal.dist(head_pos)
    c = 0
    for s in world.snakes:
        c += 1
        t = world.snakes[s].get_head().dist(goal)
        if min_dist > t:
            min_dist = t

        snake_temp = world.snakes[s]
        snake_temp_head = world.snakes[s].get_head()

        print('Snake num ', c, '  :  ', snake_temp.get_body())
        obstacle_1 += snake_temp.get_body()

        if snake_temp_head is not head_pos:
            obstacle_2.append(snake_temp_head + Vector2D(1, 0))
            obstacle_2.append(snake_temp_head + Vector2D(0, 1))
            obstacle_2.append(snake_temp_head + Vector2D(-1, 0))
            obstacle_2.append(snake_temp_head + Vector2D(0, -1))

    a_star = []

    if ((2.5*min_dist) < my_dist) or (min_dist < 10 and (my_dist-min_dist) > 3):
        heu = 1
        newGoal = Vector2D(14, 15)
        if head_pos.i > 15 and head_pos.j > 15:
            newGoal = Vector2D(10, 10)
        elif head_pos.i < 15 and head_pos.j > 15:
            newGoal = Vector2D(20, 10)
        elif head_pos.i > 15 and head_pos.j < 15:
            newGoal = Vector2D(10, 20)
        else:
            newGoal = Vector2D(20, 20)

        toCenter = head_pos.dist(newGoal)
        # print('goal ', newGoal)

        if toCenter > 30:
            heu = 4
        elif toCenter > 20:
            heu = 3
        elif toCenter > 10:
            heu = 2
        a_star = aStar(Node(head_pos), Vector2D(14, 15), obstacle_1, heu, 30)

        if len(a_star) == 0:
            next_head_price = my_fast_selection(
                next_head, goal, obstacle_1, obstacle_2)
    else:
        # print('goal ', goal)
        heu = 1
        if my_dist > 30:
            heu = 4
        elif my_dist > 20:
            heu = 3
        elif my_dist > 10:
            heu = 2
        a_star = aStar(Node(head_pos), goal, obstacle_1, heu, 30)

        if len(a_star) == 0:
            next_head_price = my_fast_selection(
                next_head, goal, obstacle_1, obstacle_2)

    next_price = check_next(head_pos, obstacle_1, obstacle_2)
    h_number = -1
    for h in next_head:
        h_number += 1

        next_head_price[h_number] += next_price[h_number]

        if h in a_star:
            next_head_price[h_number] -= 20             # resideG
    # print('Rezaaaaaaaaaaaaaaaaaaaaaaa')
    # print('aStar output ', a_star)
    # print(actions)
    # print(next_price)
    # print(next_head_price)
    mini = min(next_head_price)
    for h_number in range(4):
        if next_head_price[h_number] == mini:
            return actions[h_number]
