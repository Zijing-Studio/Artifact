# 本地测试

解压Miracle，在new/Miracle下运行Judger

```
PS E:new\Miracle> python ./Judger/judger.py test_mode
You can input help to know the instrution set
>
```

### 人人对战

先开两个服务器端口：

```
PS E:new\Miracle> python ./Judger/judger.py test_mode
You can input help to know the instrution set
> 1 0 127.0.0.1 12345 1
> 1 1 127.0.0.1 12346 1
>
```

然后开两个播放器，分别在播放器的在线模式下输入token，点击send，分别连接对应的服务器端口：

```
127.0.0.1:12345/1/player/0
```

```
127.0.0.1:12346/1/player/1
```

两个播放器连上Judger后会有提示：

```
PS E:new\Miracle> python ./Judger/judger.py test_mode
You can input help to know the instrution set
> 1 0 127.0.0.1 12345 1
> 1 1 127.0.0.1 12346 1
>    %{"type": 1, "index": 0, "success": 1}   %{"type": 1, "index": 1, "success": 1}
```

**播放器会弹出一个错误` cannot decode the token!...`，点击OK无视掉就好！（用网站的token连就应该不会弹出这个错误）**

最后输入` 4 python+main.py my_config record`开启逻辑：

```
PS E:new\Miracle> python ./Judger/judger.py test_mode
You can input help to know the instrution set
> 1 0 127.0.0.1 12345 1
> 1 1 127.0.0.1 12346 1
>    %{"type": 1, "index": 0, "success": 1}   %{"type": 1, "index": 1, "success": 1}
Your instrution is wrong, please check your input
> 4 python+main.py my_config record
start game! <command>: python logic.py, <config>: my_config, <replay>: record
   &{"type": 4, "success": 1, "index": -1}
```

### 人机对战

先用`0 1 python+..\\example\\example_py\\main.py`的命令启动AI：

```
PS E:new\Miracle> python ./Judger/judger.py test_mode
You can input help to know the instrution set
> 0 1 python+..\\example\\example_py\\main.py
start successfully! <index>: 0, <command>: python Ai\\ai_py\\ai-sample.py
>
```

再开启一个服务器端口：

```
PS E:new\Miracle> python ./Judger/judger_win.py test_mode
You can input help to know the instrution set
> 0 1 python+..\\example\\example_py\\main.py
start successfully! <index>: 0, <command>: python ..\\example\\example_py\\main.py
> 1 0 127.0.0.1 12345 1
>
```

开一个播放器，在线模式下输入token，点击send，连接对应的服务器端口：

```
127.0.0.1:12345/1/player/1
```

连上之后会有提示：

```
PS E:new\Miracle> python ./Judger/judger.py test_mode
You can input help to know the instrution set
> 0 1 python+..\\example\\example_py\\main.py
start successfully! <index>: 0, <command>: python ..\\example\\example_py\\main.py
> 1 0 127.0.0.1 12345 1
>    %{"type": 1, "index": 1, "success": 1}
```

**播放器会弹出一个错误` cannot decode the token!127.0.0.1:12346/1/player/1`，点击OK无视掉就好！**

最后开启逻辑：

```
PS E:\Tsinghua\AC\Miracle> python ./Judger/judger.py test_mode
You can input help to know the instrution set
> 0 1 python+..\\example\\example_py\\main.py
start successfully! <index>: 0, <command>: python ..\\example\\example_py\\main.py
> 1 0 127.0.0.1 12345 1
>    %{"type": 1, "index": 1, "success": 1}
Your instrution is wrong, please check your input
> 4 python+main.py my_config record
start game! <command>: python main.py, <config>: my_config, <replay>: record
   &{"type": 4, "success": 1, "index": -1}
```

享受被AI爆锤的乐趣吧 x)



