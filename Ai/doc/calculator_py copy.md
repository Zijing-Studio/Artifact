# 计算几何库

```cpp
// 通过起点、终点、阻挡列表、拦截列表寻找路径，obstacles代表不能停留也不能经过的点，obstructs代表可以停留但不能经过的点
std::vector<Point> search_path(Point start, Point to,
    std::vector<Point> obstacles={}, std::vector<Point> obstructs={})

// A*算法，给出从单位unit到dest点的路径（包含起点），不行就返回空数组, _map为地图系统
std::vector<Point> path(gameunit::Unit unit, Point dest, gameunit::Map _map)

// 给出两个位置之间的距离
int cube_distance(Point a, Point b)

// 给出单位unit在其最大步数内可达的位置，结果为列表，列表中的元素为经过等于下标的步数可达的位置的列表（例如result[1]为经过1步能到达的位置的列表）
std::vector<std::vector<Point>> reachable(gameunit::Unit unit, gameunit::Map _map)

// 给出某点pos在给定范围内存在的单位,dist为给定的范围（步数），camp默认为-1，将会返回所有阵营的单位，0为先手阵营，1为后手阵营；flyingIncluded表示将飞行单位包含其中，onlandIncluded为将地面单位包含其中，默认两者都包含
std::vector<gameunit::Unit> units_in_range(Point pos, int dist, gameunit::Map _map, int camp=-1,
                                bool flyingIncluded=true, bool onlandIncluded=true)

// 判断某个点pos是否在地图范围之内，返回布尔值
bool in_map(Point pos)

// 给出地图内的所有点
std::vector<Point> all_pos_in_map()
```

