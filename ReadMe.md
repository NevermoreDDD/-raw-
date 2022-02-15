# AutoProcessing
## 环境
```
python 3.6
opencv 4+
```
## 使用方法
+ 直接运行process_main.py
+ 按照提示输入储存目录 - RAW文件目录（网络位置要用网络地址 \\192.168.x.xxx\）
+ 等待结果就可以了

## Features
+ 目前可以自动识别已经读取过的文件目录
+ 可以在一次读取中赋予数据集连续的ID（无论有多少文件夹）
+ 可以自动识别多个分辨率

## Working
+ 多进程同时读取文件，能提高CPU利用率 （暂时还没做平）