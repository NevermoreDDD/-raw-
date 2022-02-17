"""
说明：
本脚本用来自动处理raw格式的文件，使用教程已经写在readme中
包含的类：
Logger: 日志类，定义了日志的输出格式和内容。
方法：
select_resolution: 根据图像的大小，自动分配人工预设置的分辨率
set_parameter: 脚本的主函数，包括递归查找存放raw文件的所有子目录，创建存储路径，一旦找到最底层的文件夹，就调用图片处理方法
process_raw: 图片处理方法，可以读取目录下的raw文件，通过调用process_raw模块下的方法，将raw文件转换成png文件，并且可以赋予它们连续的ID
"""

import cv2
import os
import re
import glob
import logging
import logging.handlers
from process_raw import RawFile
import hashlib
from tqdm import tqdm


class Logger:
    """
    日志类，实例化的时候不需要传入任何参数，当然也可以参考官方文档设置输出日志的等级，但是不建议修改。
    """
    def __init__(self, flevel=logging.INFO, clevel=logging.INFO):
        # 获取日志文件
        self.logger = logging.getLogger('auto-process.log')
        self.logger.setLevel(logging.INFO)
        # 设置日志输出的格式
        fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s ', '%Y-%m-%d %H:%M:%S')
        ch = logging.StreamHandler()
        ch.setFormatter(fmt)
        ch.setLevel(clevel)
        # 每小时分割一次日志。
        fh = logging.handlers.TimedRotatingFileHandler('auto_process.log', when='H', interval=1)
        # fh.namer = lambda x: x.split('.')[1]
        # 分割后的日志后缀
        fh.suffix = "%Y-%m-%d_%H.log"
        fh.setFormatter(fmt)
        fh.setLevel(flevel)
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
    # 以下函数是日志对应的方法，不需要修改
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


def select_resolution(files, logger):
    """
    根据图片大小选择合适的分辨率和比特。
    注意：方法默认一个目录下的所有图片的参数都一致。如果实际出现不一致的情况，在后续处理（其他函数中）将会记录在日志里。
    files: 目录（这个目录下不存在子目录）
    logger: Logger类的实例化对象
    """
    print(f"正在读取{files}...")
    # 获得文件夹中所有后缀为.raw的文件
    raw_files = glob.glob(files + '/*' + '.raw')
    # 如果该目录下不存在raw文件，就返回
    if not raw_files:
        return
    # 遍历文件， 如果找到对应的分辨率目标，就直接返回结果
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
            # 如果文件不满足预设的条件，就把这个文件记录在日志中，继续检查下一个文件
            logger.error(f"{file} size of {round(os.stat(file).st_size / 1024)} KB. Please Check Manually")
            continue
    # 如果遍历结束仍未返回，为了避免程序中断，会将这个文件夹记录在日志中。并且返回(0, 0, 0)
    logger.error(f"{files} has totally new resolution")
    return 0, 0, 0


def set_parameter(filepath, logger, savepath: str, handle_duplicate=None):
    """
    主函数
    1. 从日志中读取内容，记录已经处理过的目录。
    2. 查看存储路径下是否有同名文件，如果有的话会在文件结尾加一个数字。
    3. 递归搜索文件的所有子目录
    4. 查找到最底层目录后，调用select_resolution函数，获取该目录下raw文件的WIDTH HEIGHT BIT.
    5. 获取需要的信息之后调用process_raw函数，转存raw图为png图片
    :param filepath: str，目前正在读取的目录
    :param logger: Logger对象
    :param savepath: str，存储路径
    ## 目前会生成多个exist_save和多个done_list，可以把145-172行单独拆出来一个函数，并作为参数传递进来。减少运算量和内存占用
    """
    # 获取源目录下的所有文件
    file_list = os.listdir(filepath)
    # print(file_list)
    # 获取存储路径下的所有文件的名字
    save_dir = os.listdir(savepath)
    exist_save = []
    # 遍历文件名字
    for save in save_dir:
        save_path = savepath + '/' + save
        # 判断获取到的文件是否是一个目录，如果是的话就加到exist_save里面
        if os.path.isdir(save_path):
            exist_save.append(save)
            # print(exist_save)
    # 对exist_save做二次筛选，以ScaleRaw或Scale512作为后缀来获取文件夹的实际名字。
    exist_save = [x for x in re.findall(r"[^ ]*(?=ScaleRaw|Scale512)", " ".join(exist_save)) if x != '']
    # 这里要读日志，然后获取已经处理过的文件夹，如果存在在日志中，就跳过
    log_files = glob.glob(os.getcwd() + "/*" + '.log')
    try:
        # 对文件夹按照日期排序，之前遇到bug了，所以用try来规避掉indexerror。
        log_files.sort(key=lambda x: re.findall(r'(?<=auto_process).*(?=.log)', x)[0])
    except IndexError:
        pass
    # 如果因为IndexError导致没办法排序，就不排了，继续执行下面的语句。
    finally:
        done_list = []
        for log in log_files:
            with open(log, 'r') as l:
                try:
                    logs = l.readlines()
                    data = ' '.join(logs)
                    # print(re.findall(r'(?<=Work done: ).*(?= finished)', data))
                    # 这里的格式是自定义的，会获取Work done: finished中间的字符串
                    done_list += re.findall(r'(?<=Work done: ).*(?= finished)', data)
                except IndexError:
                    done_list = []
        # 定义一个root_file，用来判断是不是已经到了最底层。
        root_file = []
        for item in file_list:
            path = filepath + '/' + item
            if os.path.isdir(path):
                # 如果已经存在在done_list里面，说明这个文件夹处理过了，跳过
                if path in done_list:
                    continue
                # 如果不在，就再调用一次set_parameter
                set_parameter(path, logger, savepath, handle_duplicate)
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
            width, height, bit = select_resolution(filepath, logger)
            if width == height == bit == 0:
                return
            process_raw(filepath, logger, save_path, bit, width, height)
        return


def process_raw(directory, logger, save_path, bit, width, height):
    image_list = glob.glob(directory + '/*' + '.raw')
    number_image = len(image_list)
    print('即将读取的目录： {},这里有{}张图片，目前设定最多只会读取2000张图片'.format(directory, number_image))
    # 这里从日志里面获取编号、给PNG标上
    log_files = glob.glob(os.getcwd() + "/*" + '.log')
    try:
        log_files.sort(key=lambda x: re.findall(r'(?<=auto_process).*(?=.log)', x)[0])
    except IndexError:
        pass
    finally:
        if len(log_files) != 0:
            with open(log_files[0], 'r') as l:
                logs = l.readlines()
                for index in range(-1, -len(logs) - 1, -1):
                    try:
                        img_id = re.findall(r"(?<=FINAL ID: ).*(?= )", logs[index])[-1]
                    except IndexError:
                        img_id = 0
                        continue
                    else:
                        break
        else:
            img_id = 0
        true_id = int(img_id)
        iter_time = 2000 if number_image > 2000 else number_image
        for index in tqdm(range(iter_time)):
            raw_handler = RawFile(img_path=image_list[index], dtype=bit, width=width, height=height, logger=logger)
            image = raw_handler.handle_img()
            if not isinstance(image, type(None)):
                cv2.imencode('.png', image)[1].tofile(os.path.join(save_path, 'temp' + '.png'))
            with open(os.path.join(save_path, 'temp' + '.png'), 'rb') as f:
                md = hashlib.md5()
                data = f.read()
                md.update(data)
                file_name = md.hexdigest()
            os.remove(os.path.join(save_path, 'temp' + '.png'))
            with open(os.path.join(save_path, "{:0>7d}_".format(true_id) + file_name + '.png'), 'wb') as f:
                f.write(data)
            true_id += 1
    # self.engine.savePng(nargout=0)
    logger.info(f"Work done: {directory} finished, FINAL ID: {true_id} ")
    print("执行完毕")
    return
    # else:
    #     return


if __name__ == '__main__':
    # 全局变量，用来应对重名文件过多的问题
    handle_duplicate = 0
    logger_ = Logger()
    while True:
        savepath = input("请输入储存数据的目录（绝对路径）：").replace("\\", '/')
        workdir = input('输入源文件的绝对路径(直接按回车可以停止脚本): ').replace("\\", '/')
        if workdir == '':
            break
        set_parameter(workdir, logger_, savepath, handle_duplicate)
