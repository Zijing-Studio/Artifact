#!/usr/bin/python
# -*- coding:utf-8 -*-
'''
calculator for hex-grids
'''

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

def search_path(start, to, obstacles=[]):
    '''
    return shortest path
    '''
    _start = ()
    _to = ()
    for i in range(3):
        _start += (start[i],)
        _to += (to[i],)
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

def path(unit, dest, _map):
    '''
    public sdk for search_path
    '''
    obstacles = []
    #obstacles += _map.get
    result = search_path(unit.pos, dest, obstacles)
    return result

if __name__ == "__main__":
    cube_reachable(1,1)
