import hashlib
import os
import re
import glob


def convert2hash(filepath):
    """
    设定需要传入matlab的参数并且调用matlab脚本
    """
    # 获取源目录下的所有文件
    file_list = os.listdir(filepath)
    # print(file_list)
    # 获取存储路径

    root_file = []
    for item in file_list:
        path = os.path.join(filepath, item)
        if os.path.isdir(path):
            convert2hash(path)
        elif len(re.findall(r"\.png$|\.jpg$", item)) != 0:
            root_file.append(path)
    # print(root_file)
    if len(root_file) != 0:
        # 这个部分会将png文件以md5作为文件名重命名并且放到指定的目录中
        print(f"正在处理路径{filepath}...")
        for image in root_file:
            with open(image, 'rb') as f:
                md = hashlib.md5()
                data = f.read()
                md.update(data)
                file_name = md.hexdigest()
            os.remove(image)
            with open(os.path.join(filepath, file_name + '.png'), 'wb') as f:
                f.write(data)
    return


if __name__ == "__main__":
    print("请输入PNG文件路径（只能处理PNG文件）：")
    filepath = input().replace("\\", "/")
    # print("请输入存储路径： ")
    # save_path = input().replace("\\", "/")
    convert2hash(filepath)
