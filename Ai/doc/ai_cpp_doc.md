# ai_cpp

## json.hpp

开源的json库。

需要调用该json库的地方已经给出相关代码，您不必关注相关细节。

## gameunit.hpp

包含若干结构体，用于表述游戏中各单位的信息。

## ai_sdk.hpp

包含以下函数。您可以调用以下函数来快速执行相关操作。

其中round参数均指代当前的回合数。如果round不等于实际当前回合数，则操作无效。
```cpp
void summon(int round, int type, int star, int x, int y, int z)
```

​		在地图(x, y, z)处召唤一个本方类型为type，星级为star的单位

```cpp
void move(int round, int mover, int x, int y, int z)
```

​		将地图上id为**mover**的单位移动到地图(x, y, z)处

```cpp
void attack(int round, int attacker, int target)
```

​		令地图上id为attacker的单位攻击地图上id为target的单位

```cpp
void end(int round)
```

​		结束当前回合。

## ai.cpp

包含类AI。该类包含的类方法如下

```cpp
update_game_info()
```

​		更新游戏局面信息，并存入类属性中。

```cpp
play()
```

​		您需要在此处结合游戏当前局面信息，做出自己的处理，并调用api.hpp中的接口，实现自己的操作。

同时该文件中也包含main()函数，用于启动AI。



## 说明

一般来说，您只需要编写play函数中的内容，而不必关注其余函数的实现。
