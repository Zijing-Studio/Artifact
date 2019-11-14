# 游戏状态系统

## 接口

```python
emit(Event)
# 触发一个事件，交由状态系统处理
start_event_process()
# 使状态系统开始处理事件堆中堆积的事件，直至清空
get_map()
# 返回当前地图
get_units()
# 返回当前所有单位的列表/集合
get_unit_by_id(int id)
# 通过生物id获取生物
get_player_by_id(int player_id)
# 通过player的id获取其信息
get_barracks(player_id)
# 返回选手id为player_id的兵营列表
get_obstacles()
# 返回所有障碍物
get_relic_by_id(player_camp)
# 获得一个玩家的神迹
unit_conflict(string type, pos)
# 检查在pos位置如果产生种类为type的生物是否会发生重叠
player.check_unit_cost(string type, int star)
# 检查player召唤星级为star的生物生物槽是否够用
player.check_mana_cost(string type, int star)
# 检查player召唤星级为star的生物法力值是否够用
path(mover, position)
# 返回移动到position的路径，不行就返回False
```

