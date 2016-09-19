#!/usr/bin/env python

import numpy as np
from itertools import combinations_with_replacement, combinations, permutations, product
import pygame
import random
import copy
import math

background_color = [0, 0, 0]
pacman_color = [255, 255, 0]
wall_color = [255, 255, 255]
ghost_color = [0, 0, 255]
alert_color = [255, 0, 0]
blocksize = 46
agentsize = 18
ghostsize = 34

# ' ' - nothing
# 'P' - player
# '#' - wall
# 'G' - ghost

mfield = np.array(
        [['#', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', ' ', ' ', ' ', ' ', ' ', '#'],
         ['#', ' ', '#', '#', '#', ' ', ' ', ' ', '#', '#', ' ', '#', ' ', '#', '#'],
         [' ', 'G', '#', ' ', ' ', ' ', '#', ' ', ' ', '#', ' ', '#', ' ', ' ', ' '],
         ['#', ' ', '#', ' ', '#', ' ', '#', '#', ' ', '#', ' ', '#', ' ', '#', ' '],
         ['#', ' ', '#', ' ', '#', ' ', '#', ' ', ' ', '#', ' ', '#', ' ', '#', 'G'],
         ['#', ' ', '#', ' ', '#', ' ', '#', '#', ' ', ' ', ' ', '#', ' ', '#', ' '],
         ['#', ' ', ' ', ' ', '#', ' ', '#', 'P', ' ', '#', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', '#', ' ', ' ', ' ', '#', ' ', '#', '#', '#', '#', '#', ' ', '#'],
         ['#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', ' ', ' ', '#', ' ', ' '],
         ['#', ' ', '#', ' ', '#', 'G', ' ', ' ', ' ', ' ', ' ', '#', '#', '#', ' '],
         ['#', ' ', ' ', ' ', '#', '#', ' ', '#', ' ', '#', ' ', ' ', ' ', '#', ' '],
         ['#', ' ', '#', '#', '#', ' ', ' ', '#', ' ', '#', ' ', '#', ' ', '#', '#'],
         [' ', ' ', '#', ' ', ' ', ' ', '#', '#', '#', '#', ' ', '#', ' ', '#', ' '],
         ['#', ' ', '#', '#', ' ', '#', '#', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' '],
         ['#', '#', '#', ' ', ' ', ' ', '#', ' ', '#', '#', ' ', '#', ' ', '#', '#']])

height = len(mfield)
width = len(mfield[0])

def randomize(field):
    nfield = copy.deepcopy(field)
    nowall_x = []
    nowall_y = []
    nowall_y, nowall_x = np.where(field != '#')
    nowall = list(zip(nowall_y, nowall_x))
    for pos in nowall:
        nfield[pos[0]][pos[1]] = ' '
    toplace = ['P', 'G', 'G', 'G']
    for item in toplace:
        while True:
            y = random.randrange(0, width - 1)
            x = random.randrange(0, width - 1)
            if(nfield[y][x] != ' '):
                continue
            else:
                nfield[y][x] = item
                break
    return nfield

# Returns the resulting position of a moving object, given its current position and its action
def update_position(position, action):
    newpos = [position[0] + action[0], position[1] + action[1]]
    newpos[0] %= height
    newpos[1] %= width
    return newpos

def player_position(field):
    return np.array(np.where(field == 'P')).flatten()

# Returns a list of possible actions (lists with relative y and x positions), given the current field and angent position
def possible_actions(field, position):
    actions = []
    for action in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
        newpos = update_position(position, action)
        target = field[newpos[0]][newpos[1]]
        if target == '#':
            continue
        elif target == 'G':
            continue
        actions.append(action)
    return actions

# Updates a field matrix and moves an agent from the old position to a new position
def move_agent(field, old_position, new_position):
    nfield = copy.deepcopy(field)
    agent = nfield[old_position[0]][old_position[1]]
    target = nfield[new_position[0]][new_position[1]]
    if not (agent == 'P' and target == 'G'):
        nfield[new_position[0]][new_position[1]] = agent
    nfield[old_position[0]][old_position[1]] = ' '
    return nfield

def dijkstra(field, position):
    distances = np.full((height, width), 60)
    distances[position[0]][position[1]] = 0
    unvisited_distances = np.full((height, width), 60)

    while True:
        for action in possible_actions(field, position):
            newpos = update_position(position, action)
            if(unvisited_distances[newpos[0]][newpos[1]] != 61):
                if distances[position[0]][position[1]] + 1 < distances[newpos[0]][newpos[1]]:
                    distances[newpos[0]][newpos[1]] = distances[position[0]][position[1]] + 1
                    unvisited_distances[newpos[0]][newpos[1]] = distances[position[0]][position[1]] + 1
        unvisited_distances[position[0]][position[1]] = 61
        position = list(np.unravel_index(unvisited_distances.argmin(), unvisited_distances.shape))

        if unvisited_distances[position[0]][position[1]] >= 60:
            return distances

def ghostaction(field, position, playerpos):
    mindist = 60
    minaction = []
    dist = dijkstra(field, playerpos)
    for action in possible_actions(field, position):
        newpos = update_position(position, action)
        if field[newpos[0]][newpos[1]] != 'G':
            if dist[newpos[0]][newpos[1]] < mindist:
                mindist = dist[newpos[0]][newpos[1]]
                minaction = action
    return minaction

def update(field, player_action):
    def euclidean(p_x, p_y, g_x, g_y):
        return math.sqrt((g_x - p_x)**2 + (g_y - p_y)**2)

    ## calculation of ghost actions
    # ghost positions
    ghost_x = []
    ghost_y = []
    ghost_x, ghost_y = np.where(field == 'G')

    player_pos = player_position(field)

    for ghost_pos in zip(ghost_x, ghost_y):
        actions_ghost = possible_actions(field, ghost_pos)
        distance = 10000 # high value
        best_action = ghostaction(field, ghost_pos, player_pos)
        if len(best_action) == 2:
            best_pos = update_position(ghost_pos, best_action)
            field = move_agent(field, ghost_pos, best_pos)

    new_player_pos = update_position(player_pos, player_action)
    field = move_agent(field, player_pos, new_player_pos)
    player_pos = new_player_pos
    return field

# Returns the empowerment resulting from traking a specific action in a field
def empowerment(field, action, steps):
    if steps == 0:
        return 1
    newfield = update(field, action)
    playerpos = player_position(newfield)
    if len(playerpos) != 2:
        return 1
    E = 1
    for nextaction in possible_actions(newfield, playerpos):
        E += empowerment(newfield, nextaction, steps - 1)
    return E

pygame.init()
clock = pygame.time.Clock()

size = [width * blocksize, height * blocksize]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pacman")

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(background_color)
    for x in range(0, width):
        for y in range(0, height):
            if(mfield[y][x] == '#'):
                pygame.draw.rect(screen, wall_color, [x * blocksize, y * blocksize, blocksize - 1, blocksize - 1])
            elif(mfield[y][x] == 'P'):
                pygame.draw.circle(screen, pacman_color, [int(x * blocksize + blocksize / 2), int(y * blocksize + blocksize / 2)], agentsize)
            elif(mfield[y][x] == 'G'):
                pygame.draw.rect(screen, ghost_color, [int(x * blocksize + (blocksize - ghostsize) / 2),
                                                       int(y * blocksize + (blocksize - ghostsize) / 2),
                                                       ghostsize - 1, ghostsize - 1])


    if len(player_position(mfield)) == 2:
        agent_actions = possible_actions(mfield, player_position(mfield))
        best_empowerment = 0
        best_action = random.choice(agent_actions)
        for action in agent_actions:
            E = empowerment(mfield, action, 4)
            #print(E)
            if(E > best_empowerment):
                best_empowerment = E
                best_action = action
        mfield = update(mfield, best_action)
    else:
        clock.tick(1)
        pygame.draw.rect(screen, alert_color, [0, 0, blocksize * width, blocksize * height])
        mfield = randomize(mfield)

    pygame.display.flip()

    clock.tick(2)

pygame.quit()

