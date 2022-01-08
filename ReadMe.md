# Labelme 使用说明

+ Labelme是用python编写的程序，只能安装在python3.6环境下
+ 为了安装python3.6，需要Anaconda

## 下载Anaconda

> https://www.anaconda.com/products/individual

1. 点击Download即可

![image-20220106100224354](./image/image-20220106100224354.png)

2. 下载完成后点击安装，可以修改安装路径

![image-20220106100406328](./image/image-20220106100406328.png)



3. 之后一直点击next就可以，不需要更改设置
4. 安装完成

## 使用Anaconda安装labelme

1. 在开始菜单中找到Anaconda prompt

![image-20220106100554050](./image/image-20220106100554050.png)

2. 进入命令行界面

![image-20220106100642718](./image/image-20220106100642718.png)

3. 输入conda create -n labelme python=3.6 

  <font color = 'red'>（如果电脑上有代理，需要提前关闭代理）</font>
  ![image-20220106100819056](./image/image-20220106100819056.png)

4. 安装完成后如图

![image-20220106101106429](./image/image-20220106101106429.png)

5. 输入activate labelme

![image-20220106101137625](./image/image-20220106101137625.png)

6. 输入pip install labelme -i https://pypi.douban.com/simple

   等待安装
   
   <img src="./image/image-20220106101334619.png" />
7. 安装完成

## 数据目录及标签类型介绍
#### 图片文件夹:.   <font color='red'>（请先检查目录，如果缺少文件夹请自己建立）</font>
  ├─M形

  ├─内角焊

  ├─右N形

  ├─外角焊

  ├─对接

  ├─左N形

  └─弧形

#### 需要在图片中标出的标签类型
> | 激光线 | 强飞溅 | 弱飞溅 | 强眩光 |
> | :-------: | ---------- | ----------|---------- |
> | 中眩光 | 弱眩光 | 弧光  ||


## 使用Labelme

1. 安装结束后在当前界面输入labelme

![image-20220106101533022](./image/image-20220106101533022.png)

2. 回车后应该出现交互界面
3. OpenDir打开文件夹

![image-20220106101615667](./image/image-20220106101615667.png)

4. 在图片上右键或者直接在侧边栏中找到Create Polygons，点击之后在激光线上画出边缘，多边形闭合之后会自动弹出label的窗口，标注类型即可
   如果没画好需要调整多边形，可以点击Edit Polygons，删除的话可以直接在多边形上右键delete掉

   ![image-20220106101916370](./image/image-20220106101916370.png)

5. 图例中一条激光线和一处眩光，都标注出来，标注完成后是这样的

   ![image-20220106102108535](./image/image-20220106102108535.png)
   
6. 标注之后点击save，会弹出窗口保存json文件，选择该激光线对应的类型文件夹。保存到里面即可。图例中的激光线是M形，因此保存到M形文件夹中
   <font color='red'>这个json文件是我们需要的目标文件</font>
   保存好之后可以在右下角的File List中看到这个图片已经被打勾了，表示已经保存好

![image-20220106104050454](./image/image-20220106104050454.png)

7. 提交的时候把整个文件夹打包好提交。
