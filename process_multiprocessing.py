import cv2
import os
import re
import glob
import logging
import logging.handlers
from process_raw import RawFile, multiple_working
import multiprocessing
from multiprocessing.pool import Pool
from tqdm import tqdm
import warnings
import time
from datetime import datetime

"""
def _get_last_line(filename):
    get last line of a file
    :param filename: file name
    :return: last line or None for empty file
    try:
        filesize = os.path.getsize(filename)
        if filesize == 0:
            return None
        else:
            with open(filename, 'rb') as fp:  # to use seek from end, must use mode 'rb'
                offset = -8  # initialize offset
                while -offset < filesize:  # offset cannot exceed file size
                    fp.seek(offset, 2)  # read # offset chars from eof(represent by number '2')
                    lines = fp.readlines()  # read from fp to eof
                    if len(lines) >= 2:  # if contains at least 2 lines
                        return lines[-1]  # then last line is totally included
                    else:
                        offset *= 2  # enlarge offset
                fp.seek(0)
                lines = fp.readlines()
                return lines[-1]
    except FileNotFoundError:
        print(filename + ' not found!')
        return None
"""


class Logger:
    def __init__(self, flevel=logging.INFO, clevel=logging.INFO):
        self.logger = logging.getLogger('auto_process.log')
        self.logger.setLevel(logging.INFO)
        fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(process)d %(message)s ', '%Y-%m-%d %H:%M:%S')
        ch = logging.StreamHandler()
        ch.setFormatter(fmt)
        ch.setLevel(clevel)
        fh = logging.handlers.TimedRotatingFileHandler('auto_process.log', when='H', interval=1, backupCount=3)
        fh.namer = lambda x: x.split('.')[0]
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


class NoDaemonProcess(multiprocessing.Process):
    def _get_daemon(self):
        return False

    def _set_daemon(self, value):
        pass

    daemon = property(_get_daemon, _set_daemon)


class MyPool(Pool):
    Process = NoDaemonProcess


def main():
    savepath = input("请输入储存数据的目录（绝对路径）：").replace("\\", '/')
    # 全局变量，用来应对重名文件过多的问题
    handle_duplicate = 0
    logger_ = Logger()
    global logs
    logs_ = logger_
    num_cores = multiprocessing.cpu_count()
    pool = MyPool(num_cores)
    workdir = input('输入源文件的绝对路径(直接按回车可以停止脚本): ').replace("\\", '/')
    if workdir == '':
        return
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
        warnings.warn("Something happens in sorting log files. ")
    finally:
        done_list = []
        for log in log_files:
            with open(log, 'r') as l:
                try:
                    logs = l.readlines()
                    data = ' '.join(logs)
                    done_list += re.findall(r'(?<=Work done: ).*(?= finished)', data)
                except IndexError:
                    done_list = []
        set_parameter(workdir, logs_, savepath, done_list, exist_save, pool, handle_duplicate)


def select_resolution(files, logger):
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
            logger.error(f"{file} size of {round(os.stat(file).st_size / 1024)} KB. Please Check Manually")
            continue
    logger.error(f"{files} has totally new resolution")
    return 0, 0, 0


def set_parameter(filepath, logger, savepath, done_list, exist_save, pool, handle_duplicate=0):
    # 获取源目录下的所有文件
    file_list = os.listdir(filepath)
    # print(file_list)
    # 获取存储路径下的所有文件的名字
    root_file = []
    for item in file_list:
        path = filepath + '/' + item
        if os.path.isdir(path):
            if path in done_list:
                continue
            set_parameter(path, logger, savepath, done_list, exist_save, pool,handle_duplicate)
        elif len(re.findall(r"\.raw$", item)) != 0:
            root_file.append(item)
    # print(root_file)
    if len(root_file) != 0:
        i = re.split(r'/', filepath)[-1]
        print("目标文件夹前缀：", i)
        while i in exist_save:
            i += str(handle_duplicate)
            handle_duplicate += 1
        save_path = os.path.join(savepath, i + 'ScaleRaw')
        # 会自动在结尾加上一个数字，这个数字不一定是连续的
        os.mkdir(save_path)
        width, height, bit = select_resolution(filepath, logger)
        if width == height == bit == 0:
            return
        connect_matlab(filepath, logger, save_path, bit, width, height, pool)
    return


def recursive_func(args):
    set_parameter(*args)


def connect_matlab(directory, logger, save_path, bit, width, height, pool):
    image_list = glob.glob(directory + '/*' + '.raw')
    number_image = len(image_list)
    print('即将读取的目录： {},这里有{}张图片，目前设定最多只会读取1000张图片'.format(directory, number_image))
    # 这里从日志里面获取编号、给PNG标上
    log_files = glob.glob(os.getcwd() + "/*" + '.log')
    try:
        log_files.sort(key=lambda x: re.findall(r'(?<=auto_process).*(?=.log)', x)[0])
    except IndexError:
        pass
    finally:
        if len(log_files) != 0:
            with open(log_files[-1], 'r') as l:
                try:
                    logs = l.readlines()
                    if len(logs) == 0:
                        img_id = 0
                    for index in range(-1, -len(logs)-1, -1):
                        img_id = re.findall(r"(?<=FINAL ID: ).*(?= )", logs[index])[-1]
                        if img_id == "":
                            continue
                        else:
                            break
                except IndexError:
                    img_id = 0
        else:
            img_id = 0
        true_id = int(img_id)
        iter_time = 1000 if number_image > 1000 else number_image
        for index in tqdm(range(iter_time)):
            raw_handler = RawFile(img_path=image_list[index], dtype=bit, width=width, height=height, logger=logger)
            images = []
            image = pool.apply_async(multiple_working(raw_handler))
            print(image)
            if not isinstance(image, type(None)):
                try:
                    cv2.imencode('.png', image)[1].tofile(os.path.join(save_path, ("{:0>7d}".format(true_id))) + '.png')
                except cv2.error:
                    logger.error(f"{directory}中出现错误，请检查")
            true_id += 1
        pool.close()
        pool.join()
        # self.engine.savePng(nargout=0)
        logger.info(f"Work done: {directory} finished, FINAL ID: {true_id} ")
        print("执行完毕")
        return
    # else:
    #     return


if __name__ == '__main__':
    main()
