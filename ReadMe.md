# AutoProcessing
## 环境
```
切换到labelme环境下：conda activate labelme
python 3.6
opencv 4+
```
## 使用方法
+ 直接运行process_main.py
+ 按照提示输入储存目录 - RAW文件目录（网络位置要用网络地址 \\\192.168.x.xxx\）
+ 等待结果就可以了
## v0.2.0版本
### Change
+ **\++  重新更改了process_main.py中的命名方式，现在的命名格式如下：**
```
../directory/{id}_{md5}.png
```
### Note
+ process_main.py 为单进程脚本，可以生成和读取连续的ID
+ ***process_multiprocessing.py***是多进程脚本，只能记录哪些文件夹是已经处理过的 **没有ID相关的功能**
+ 如果对log文件中的格式有疑问，可以打开log文件获取内容
## v0.1.0版本
### Features
+ 目前可以自动识别已经读取过的文件目录
+ 现在可以创建与源目录相同的文件夹结构
+ 现在图片会用其md5值来命名
+ 可以自动识别多个分辨率
+ 多进程同时读取文件

### Working
+ 利用多进程的时候CPU的利用率还是很低，不知道哪里出了问题
+ Windows下的多进程不是很方便，不能序列化自定义出来的类。可以在linux下面做，不过linux需要先把数据服务器挂载进来，不能直接使用网络位置，我没有继续往下做。

## alpha版本
### Features
+ 目前可以自动识别已经读取过的文件目录
+ 可以在一次读取中赋予数据集连续的ID（无论有多少文件夹）
+ 可以自动识别多个分辨率

### Working
+ 利用多进程读取文件，加快速度
