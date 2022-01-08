import matlab
import matlab.engine
import os
import re
import glob
import pandas as pd

# PATH = '//192.168.2.58/weld_data_line/temppp/A-04/A-10'
# files = glob.glob(PATH+'/*'+'.raw')
savepath= input("请输入储存数据的目录（绝对路径）：").replace("\\",'/')
workdir = input('输入源文件的绝对路径: ').replace("\\",'/')

# engine = matlab.engine.start_matlab()
# file_list = os.listdir(PATH)
# i = 0
# for directory in file_list:
#     parameters['filepath'] = PATH + '/' + directory
#     parameters['pathF'] = str(i) + '眩光'
#     files = glob.glob(PATH + '/*' + '.raw')
#     for file in files:
#         if round(os.stat(file).st_size/1024) in [3038,3037]:
#             parameters['width'] = 1440
#             parameters['height'] = 1080
#             parameters['bit'] = 'uint16'
#             break
#         elif round(os.stat(file).st_size/1024) in [1484,1485,1486]:
#             parameters['width'] = 1056
#             parameters['height'] = 1440
#             parameters['bit'] = 'uint8'
#             break
#         elif round(os.stat(file).st_size/1024) in [4049,4050,4051]:
#             parameters['width'] = 1920
#             parameters['height'] = 1080
#             parameters['bit'] = 'uint16'
#             break
#         elif round(os.stat(file).st_size/1024) in [1979,1980,1981]:
#             parameters['width'] = 1056
#             parameters['height'] = 1920
#             parameters['bit'] = 'uint8'
#             break
#     engine.api(**parameters,nargout=0)
#     break
class ResolutionException(Exception):
    pass

class SavePng():
    def __init__(self, pathF = None, savepath=savepath, width=None, height=None, bit=None):
        """
        传入matlab的参数
        """
        self.pathF = pathF
        self.savepath = savepath
        self.width = width
        self.height = height
        self.bit = bit
        self.engine = matlab.engine.start_matlab()
    def _select_resolution(self,files):
        """
        根据图片大小选择合适的分辨率和比特
        """
        print(f"正在读取{files}...")
        # 获得文件夹中所有后缀为.raw的文件
        files = glob.glob(files + '/*' + '.raw')
        if not files:
            return
        for file in files:
            if round(os.stat(file).st_size / 1024) in [3038, 3037]:
                self.width = 1440
                self.height = 1080
                self.bit = 'uint16'
                break
            elif round(os.stat(file).st_size / 1024) in [1484, 1485, 1486]:
                self.width = 1056
                self.height = 1440
                self.bit = 'uint8'
                break
            elif round(os.stat(file).st_size / 1024) in [4049, 4050, 4051]:
                self.width = 1920
                self.height = 1080
                self.bit = 'uint16'
                break
            elif round(os.stat(file).st_size / 1024) in [1979, 1980, 1981]:
                self.width = 1056
                self.height = 1920
                self.bit = 'uint8'
                break
            else:
                # 如果文件不满足预设的条件，抛出异常
                raise ResolutionException("没有定义这样的分辨率数据，请检查代码")
        return
    def set_parameter(self,filepath):
        """
        设定需要传入matlab的参数并且调用matlab脚本
        """
        # 获取源目录下的所有文件
        file_list = os.listdir(filepath)
        # print(file_list)
        # 获取存储路径下的所有文件
        save_dir = os.listdir(self.savepath)
        exist_save = []
        for save in save_dir:
            save_path = self.savepath + '/' + save
            if os.path.isdir(save_path):
                exist_save.append(save)
                # print(exist_save)
        exist_save = [x for x in re.findall(r"[^ ]*(?=ScaleRaw|Scale512)", " ".join(exist_save)) if x != '']
        root_file = []
        for item in file_list:
            path = filepath + '/' + item
            if os.path.isdir(path):
                self.set_parameter(path)
            else:
                root_file.append(item)
        # print(root_file)
        if len(root_file) != 0:
            i = re.split(r'/',filepath)[-1]
            print(i)
            while i in exist_save:
                i = input("该文件已存在于savepath中，请写一个新名字（只能用英文或者数字）:")
            self._select_resolution(filepath)
            self.pathF = i
            self.connect_matlab(filepath)
        return

    def connect_matlab(self,dir):
        print('即将读取的目录： {},这里有{}张图片，目前设定最多只会读取300张图片，如需要请更改load_raw_File.m'.format(dir,len(os.listdir(dir))))
        # check = input()
        # if check.lower() == 'y':
        with open("loadFile.txt",'w',encoding='utf-8') as f:
            f.write(dir.replace('/','\\') +'\n')
            f.write(self.savepath.replace('/','\\') +'\n')
            f.write(self.pathF+'\n')
            f.write(str(self.width)+'\n')
            f.write(str(self.height)+'\n')
            f.write(self.bit+'\n')
        self.engine.savePng(nargout=0)
        print("执行完毕")
        return
        # else:
        #     return
    def start(self):
        pass
if __name__ == '__main__':
    while True:
        a = SavePng()
        a.set_parameter(workdir)
        del a

