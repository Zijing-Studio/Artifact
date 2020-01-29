#!/usr/bin/python
# -*- coding:utf-8 -*-
'''
calculator for hex-grids
'''

# left-up, right-up, left-down, right-down, left-right, up, down
MAPBORDER = [(-15+i, 9, 6-i) for i in range(0, 14)] + \
            [(15-i, -6+i, -9) for i in range(0, 14)] + \
            [(-15+i, 6-i, 9) for i in range(0, 14)] + \
            [(15-i, -9, -6+i) for i in range(0, 14)] + \
            [(-15, 8, 7), (-15, 7, 8), (15, -7, -8), (15, -8, -7)] + \
            [(-1, 8, -7), (0, 8, -8), (1, 7, -8)] + \
            [(-1, -7, 8), (0, -8, 8), (1, -8,  7)]

def cube_distance(a, b):
    '''
    return distance between two unit
    '''
    try:
        distance = (abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2]))/2
    except KeyError:
        raise ValueError("Point format wrong: a: %s, b:%s"%(str(a), str(b)))
    return int(distance + 1e-8)

def cube_neighbor(pos, dir):
    _dir = dir%6
    if _dir == 0:
        neighbor = (pos[0]+1, pos[1], pos[2]-1)
    elif _dir == 1:
        neighbor = (pos[0]+1, pos[1]-1, pos[2])
    elif _dir == 2:
        neighbor = (pos[0], pos[1]-1, pos[2]+1)
    elif _dir == 3:
        neighbor = (pos[0]-1, pos[1], pos[2]+1)
    elif _dir == 4:
        neighbor = (pos[0]-1, pos[1]+1, pos[2])
    else:
        neighbor = (pos[0], pos[1]+1, pos[2]-1)
    return neighbor

class Node:
    def __init__(self, pos, G, H, parent=None):
        self.pos = pos
        self.G = G
        self.H = H
        self.parent = parent

    def __str__(self):
        return '''
                pos: {},
                G: {},
                F: {},
               '''.format(self.pos, self.G, self.H)

def search_path(start, to, obstacles=[]):
    '''
    return shortest path
    '''
    _start = ()
    _to = ()
    for i in range(3):
        _start += (start[i],)
        _to += (to[i],)
    if to in obstacles:
        return False
    opened = {}
    closed = {}
    opened[_start] =  Node(start, 0, cube_distance(start, to))
    while opened:
        cur_node = opened[min(opened, key=lambda x: opened[x].G + opened[x].H)]
        for i in range(6):
            neighbor = cube_neighbor(cur_node.pos, i)
            if neighbor not in closed and neighbor not in obstacles:
                if neighbor in opened:
                    if cur_node.G+1 < opened[neighbor].G:
                        opened[neighbor].G = cur_node.G + 1
                        opened[neighbor].parent = cur_node
                else:
                    opened[neighbor] = Node(neighbor, cur_node.G+1, cube_distance(neighbor, _to), cur_node) 
                    if neighbor == _to:
                        final_path = []
                        node = opened[neighbor]
                        while node is not None:
                            final_path.insert(0, node.pos)
                            node = node.parent
                        return final_path
        closed[cur_node.pos] = cur_node
        del opened[cur_node.pos]
    return False

def cube_reachable(start, movement, obstacles=[]):
    '''
    return reachable position from start point in steps limited by movement
    '''
    visited = []
    visited.append(start)
    fringes = []
    fringes.append([start])

    for i in range(0, movement):
        fringes.append([])
        for pos in fringes[i]:
            for j in range(0, 6):
                neighbor = cube_neighbor(pos, j)
                if neighbor not in visited and neighbor not in obstacles:
                    visited.append(neighbor)
                    fringes[i+1].append(neighbor)
    return fringes

def path(unit, dest, _map):
    '''
    public sdk for search_path
    '''
    obstacles = []
    obstacle_object = _map.get_units()
    for obstacle in obstacle_object:
        obstacles.append(obstacle.pos)
    result = search_path(unit.pos, dest, obstacles)
    return result

if __name__ == "__main__":
    print(cube_reachable((0, 0, 0), 1, MAPBORDER))
    print(MAPBORDER)
