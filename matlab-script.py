import matlab
import matlab.engine
import os
import re
import glob
from collections import defaultdict

# PATH = '//192/home/fullv/workspace/projects/NeuralNetWork/MMSegmentation_Tutorial.ipynb.168.2.58/weld_data_line/temppp/A-04/A-10'
# files = glob.glob(PATH+'/*'+'.raw')


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
    def __init__(self, pathF=None, savepath=None, width=None, height=None, bit=None):
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
        raw_files = glob.glob(files + '/*' + '.raw')

        if not raw_files:
            return
        for file in raw_files:
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
                skip_files[f'{files}'].append(os.stat(file).st_size / 1024)
        return
    def set_parameter(self, filepath, handle_duplicate=None):
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
                self.set_parameter(path,handle_duplicate)
            elif len(re.findall(r"\.raw$", item)) != 0:
                root_file.append(item)
        # print(root_file)
        if len(root_file) != 0:
            i = re.split(r'/',filepath)[-1]
            print("目标文件夹前缀：", i)
            # 会自动在结尾加上一个数字，这个数字不一定是连续的
            while i in exist_save:
                i += str(handle_duplicate)
                handle_duplicate += 1
            self._select_resolution(filepath)
            self.pathF = i
            self.connect_matlab(filepath)
        return

    def connect_matlab(self,dir):
        print('即将读取的目录： {},这里有{}张图片，目前设定最多只会读取300张图片，如需要请更改load_raw_File.m'.format(dir,len(glob.glob(dir + '/*' + '.raw'))))
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
    savepath = input("请输入储存数据的目录（绝对路径）：").replace("\\", '/')
    # 全局变量，用来应对重名文件过多的问题
    handle_duplicate = 0
    skip_files = defaultdict(list)
    while True:
        workdir = input('输入源文件的绝对路径(直接按回车可以停止脚本): ').replace("\\", '/')
        if workdir == '':
            break
        a = SavePng(savepath=savepath)
        a.set_parameter(workdir,handle_duplicate)
        del a


