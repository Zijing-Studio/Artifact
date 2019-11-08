# 游戏状态系统

## 接口

```python
emit(Event)
# 触发一个事件，交由状态系统处理
startEventProcess()
# 使状态系统开始处理事件堆中堆积的事件，直至清空
getMap()
# 返回当前地图
getUnits()
# 返回当前所有单位的列表/集合
```

