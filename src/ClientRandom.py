from src.World import *
import random

# this code always show my recent code

def get_action(world: World):
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
    for s in world.snakes:
        snake_temp = world.snakes[s]
        snake_temp_head = world.snakes[s].get_head()

        obstacle_1 += snake_temp.get_body()

        if snake_temp_head is not head_pos:
            obstacle_2.append(snake_temp_head + Vector2D(1, 0))
            obstacle_2.append(snake_temp_head + Vector2D(0, 1))
            obstacle_2.append(snake_temp_head + Vector2D(-1, 0))
            obstacle_2.append(snake_temp_head + Vector2D(0, -1))
    
    h_number = -1
    for h in next_head:
        h_number += 1
        
        if h in obstacle_1:
            next_head_price[h_number] += 60
        if h in obstacle_2:
            next_head_price[h_number] += 20*obstacle_2.count(h)      

        next_head_price[h_number]+=world.goal_position.dist(h)
    
    print(next_head_price)
    print(actions)
    mini = min(next_head_price)
    for h_number in range(4):
        if next_head_price[h_number] == mini:
            return actions[h_number]
