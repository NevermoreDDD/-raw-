import multiprocessing
from multiprocessing import Pool
from process_multiprocessing import set_parameter
from process_multiprocessing import Logger


def main(workdir, save_path):
    pool = Pool(6)
    handle_duplicate = 0
    logger_ = Logger()
    for item in range(6):
        pool.apply_async(target=set_parameter, (workdir, logger_, save_path, handle_duplicate))
    pool.close()
    pool.join()

if __name__ == "__main__":
    savepath = input("请输入储存数据的目录（绝对路径）：").replace("\\", '/')
    workdir = input('输入源文件的绝对路径(直接按回车可以停止脚本): ').replace("\\", '/')
    main(workdir, savepath)