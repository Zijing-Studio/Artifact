example文件夹下是ai相关代码和文档。打包成游戏包时，需要分别将example_cpp、example_py下的文件压缩成zip文件（去掉外层文件夹）。

game文件夹下是游戏相关的代码，以及一个供玩家使用的judger。

ForPlayer文件夹下是给玩家看的引导，打包成游戏包时只需将tutorial.pdf放到根目录下，不必管这个文件夹。

doc文件夹下是包括各种不用放到游戏包中的文档。

Data.json也要打包入codes压缩包。

打包时，注意去掉冗余文件（pycache，record，log等）。