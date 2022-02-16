import cv2
import os
import re
import glob
import logging
import logging.handlers
import hashlib
import random
import warnings
import multiprocessing
from multiprocessing import Pool
from tqdm import tqdm
import numpy as np


def handle_img(dtype, img_path, width, height):
    img_data = np.fromfile(img_path, dtype)
    dtype = np.uint8 if dtype == 'uint8' else np.uint16
    if img_data is None:
        return None
    try:
        img_data = img_data.reshape(height, width, 1)
    except ValueError as e:
        warnings.warn(f"{img_path} has something wrong")
        return None
    else:
        if dtype == np.uint16:
            img = (img_data / 256).astype('uint8')
        else:
            img = img_data
        img_guassian = cv2.GaussianBlur(img, (5, 5), 1)
        # plt.imshow(img_guassian, cmap="gray")
        # plt.show()
        # print(img_guassian)
        if dtype == np.uint8:
            img_gamma = img_guassian
        else:
            img_gamma = np.power(img / 4 / float(np.max(img_guassian)), 0.45)
            img_gamma = (img_gamma * 255).astype('uint8')
        img_guassian = cv2.GaussianBlur(img_gamma, (5, 5), 1)
        img_raw = cv2.resize(img_guassian, dsize=(width, height), interpolation=cv2.INTER_CUBIC)
        if dtype == np.uint8:
            img_raw = cv2.transpose(img_raw)
        # img_512 = cv2.cvtColor(img_512, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("image", img_raw)
        # cv2.waitKey(0)
        # plt.imshow(img_512,cmap="gray")
        # plt.show()
        # print((img_512.dtype))
        return img_raw


class Logger:
    def __init__(self, flevel=logging.INFO, clevel=logging.INFO):
        self.logger = logging.getLogger('auto-process.log')
        self.logger.setLevel(logging.INFO)
        fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(process)d %(message)s ', '%Y-%m-%d %H:%M:%S')
        ch = logging.StreamHandler()
        ch.setFormatter(fmt)
        ch.setLevel(clevel)
        fh = logging.handlers.TimedRotatingFileHandler('auto_process.log', when='H', interval=1)
        # fh.namer = lambda x: x.split('.')[1]
        fh.suffix = "%Y-%m-%d_%H.log"
        fh.setFormatter(fmt)
        fh.setLevel(flevel)
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def war(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def cri(self, message):
        self.logger.critical(message)


def select_resolution(files):
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
            width = 1440
            height = 1080
            bit = 'uint16'
            return width, height, bit
        elif round(os.stat(file).st_size / 1024) in [1484, 1485, 1486]:
            width = 1056
            height = 1440
            bit = 'uint8'
            return width, height, bit
        elif round(os.stat(file).st_size / 1024) in [4049, 4050, 4051]:
            width = 1920
            height = 1080
            bit = 'uint16'
            return width, height, bit
        elif round(os.stat(file).st_size / 1024) in [1979, 1980, 1981]:
            width = 1056
            height = 1920
            bit = 'uint8'
            return width, height, bit
        elif round(os.stat(file).st_size / 1024) in [2969, 2970, 2971]:
            width = 1440
            height = 1056
            bit = 'uint16'
            return width, height, bit
        elif round(os.stat(file).st_size / 1024) in [3959, 3960, 3961]:
            width = 1920
            height = 1056
            bit = 'uint16'
            return width, height, bit
        elif round(os.stat(file).st_size / 1024) in [2679, 2680, 2681]:
            width = 1280
            height = 1072
            bit = 'uint16'
            return width, height, bit
        elif round(os.stat(file).st_size / 1024) in [1518, 1519, 1520]:
            width = 720
            height = 1080
            bit = 'uint16'
            return width, height, bit
        elif round(os.stat(file).st_size / 1024) in [1319, 1320, 1321]:
            width = 1056
            height = 1280
            bit = 'uint8'
            return width, height, bit
        else:
            # 如果文件不满足预设的条件，抛出异常
            # logger.error(f"{file} size of {round(os.stat(file).st_size / 1024)} KB. Please Check Manually")
            print(f"{file} size of {round(os.stat(file).st_size / 1024)} KB. Please Check Manually")
            continue
    # logger.error(f"{files} has totally new resolution")
    return 0, 0, 0


def set_parameter(filepath, savepath: str, handle_duplicate=None):
    """
    设定需要传入matlab的参数并且调用matlab脚本
    :param handle_duplicate:
    :param filepath:
    :type savepath: str
    """
    process_id = os.getpid()

    # 获取源目录下的所有文件
    file_list = os.listdir(filepath)
    # print(file_list)
    # 获取存储路径下的所有文件的名字
    save_dir = os.listdir(savepath)
    exist_save = []
    for save in save_dir:
        save_path = savepath + '/' + save
        if os.path.isdir(save_path):
            exist_save.append(save)
            # print(exist_save)
    exist_save = [x for x in re.findall(r"[^ ]*(?=ScaleRaw|Scale512)", " ".join(exist_save)) if x != '']
    # 这里要读日志，然后获取已经处理过的文件夹，如果存在在日志中，就跳过
    log_files = glob.glob(os.getcwd() + "/*" + '.log')
    try:
        log_files.sort(key=lambda x: re.findall(r'(?<=auto_process).*(?=.log)', x)[0])
    except IndexError:
        pass
    finally:
        done_list = []
        for log in log_files:
            with open(log, 'r') as l:
                try:
                    logs = l.readlines()
                    data = ' '.join(logs)
                    # print(re.findall(r'(?<=Work done: ).*(?= finished)', data))
                    done_list += re.findall(r'(?<=Work done: ).*(?= finished)', data)
                except IndexError:
                    done_list = []
        root_file = []
        for item in file_list:
            path = filepath + '/' + item
            if os.path.isdir(path):
                if path in done_list:
                    continue
                set_parameter(path, savepath, handle_duplicate)
            elif len(re.findall(r"\.raw$", item)) != 0:
                root_file.append(item)
        # print(root_file)
        if len(root_file) != 0:
            i = os.path.join(*re.split(r'/', filepath)[4:])
            print("目标文件夹路径：", i)
            while i in exist_save:
                i += str(handle_duplicate)
                handle_duplicate += 1
            save_path = os.path.join(savepath, i + 'ScaleRaw')
            # 会自动在结尾加上一个数字，这个数字不一定是连续的
            if os.path.exists(save_path):
                return
            os.makedirs(save_path)
            width, height, bit = select_resolution(filepath)
            if width == height == bit == 0:
                return
            process_raw(filepath, save_path, bit, width, height)
        return


def process_raw(directory, save_path, bit, width, height):
    image_list = glob.glob(directory + '/*' + '.raw')
    number_image = len(image_list)
    print('即将读取的目录： {},这里有{}张图片，目前设定最多只会读取2000张图片'.format(directory, number_image))
    iter_time = 2000 if number_image > 2000 else number_image
    for index in tqdm(range(iter_time)):
        image = handle_img(dtype=bit, img_path=image_list[index], width=width, height=height)
        if not isinstance(image, type(None)):
            cv2.imencode('.png', image)[1].tofile(os.path.join(save_path, 'temp' + '.png'))
        with open(os.path.join(save_path, 'temp' + '.png'), 'rb') as f:
            md = hashlib.md5()
            data = f.read()
            md.update(data)
            file_name = md.hexdigest()
        os.remove(os.path.join(save_path, 'temp' + '.png'))
        with open(os.path.join(save_path, file_name + '.png'), 'wb') as f:
            f.write(data)
    # self.engine.savePng(nargout=0)
    with open('auto_process.log', 'a+') as f:
        f.write(f"Work done: {directory} finished \n")
    # logger.info(f"Work done: {directory} finished")
    print("执行完毕")
    return
    # else:
    #     return


if __name__ == '__main__':
    # 全局变量，用来应对重名文件过多的问题
    handle_duplicate = 0
    pool = multiprocessing.Pool(10)
    # while True:
    savepath = input("请输入储存数据的目录（绝对路径）：").replace("\\", '/')
    workdir = input('输入源文件的绝对路径(直接按回车可以停止脚本): ').replace("\\", '/')
    if workdir == '':
        exit(0)
    for _ in range(10):
        re = pool.apply_async(set_parameter, (workdir, savepath, handle_duplicate))
    pool.close()
    pool.join()
    # set_parameter(workdir, logger_, savepath, handle_duplicate)
