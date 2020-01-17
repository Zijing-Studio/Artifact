# ai_py

## api.py

包含以下函数。您可以调用以下函数来快速执行相关操作。

其中\_round参数均指代当前的回合数。如果\_round不等于实际当前回合数，则操作无效。



```python
 summon(_round, _type, star, position)
```
​		在地图position处召唤一个本方类型为\_type，星级为star的单位



```python
move(_round, mover, position)
```
​		将地图上id为mover的单位移动到地图position处




```python
attack(_round, attacker, target)
```
​		令地图上id为attacker的单位攻击地图上id为target的单位




```python
end(_round)
```
​		结束当前回合。



## ai.py

包含类AI。该类包含的类方法如下

```python
__inti__(self)
```

​		初始化游戏局面信息相关的变量。

```python
update_game_info()
```

​		更新游戏局面信息，并存入类属性中。


```python
play(self)
```

​		您需要在此处结合游戏当前局面信息，做出自己的处理，并调用api.py中的接口，实现自己的操作。

同时该文件中也包含main()函数，用于启动AI。



## 说明

一般来说，您只需要编写play函数中的内容，而不必关注其余函数的实现。