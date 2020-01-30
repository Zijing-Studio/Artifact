# 计算几何库

```python
# 以下函数参数中的坐标均为立方坐标表示法下的坐标

# A*算法，给出从单位unit到dest点的路径（包含起点），不行就返回False, _map为地图系统
path(unit, dest, _map)

# 给出两个位置之间的距离
cube_distance(pos1, pos2)

# 给出单位unit在其最大步数内可达的位置，结果为列表，列表中的元素为经过等于下标的步数可达的位置的列表（例如result[1]为经过1步能到达的位置的列表）
reachable(unit, _map)
```