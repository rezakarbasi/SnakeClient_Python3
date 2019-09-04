from src.World import *
import random


def get_action(world: World):
    head_pos = world.get_self().get_head()
    next_head = []
    next_head.append(head_pos + Vector2D(1, 0))
    next_head.append(head_pos + Vector2D(0, 1))
    next_head.append(head_pos + Vector2D(-1, 0))
    next_head.append(head_pos + Vector2D(0, -1))
    next_head_prince = [0, 0, 0, 0]
    actions = ['d', 'r', 'u', 'l']

    h_number = -1
    for h in next_head:
        h_number += 1
        accident = False
        for s in world.snakes:
            if h in world.snakes[s].get_body():
                accident = True
                next_head_prince[h_number] = 100
                break
        if accident:
            print(h, 'snake')
        elif h in world.get_walls():
            accident = True
            print(h, 'wall')
            next_head_prince[h_number] = 100

    mini = min(next_head_prince)
    for h_number in range(4):
        if next_head_prince[h_number] == mini:
            return actions[h_number]
