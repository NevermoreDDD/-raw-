import os
from matplotlib import pyplot as plt
import cv2
import numpy as np
# path = r'D:\User\Desktop\222'
# path = r'D:\zhou\数据集\New\dataset_删减版_加类别_扩充_标注\M型'
# path = r'D:\zhou\数据集\New\dataset_删减版_加类别_扩充_标注\N型'
# path = r'D:\zhou\数据集\New\dataset_删减版_加类别_扩充_标注\搭接'
# path = r'D:\zhou\数据集\New\dataset_删减版_加类别_扩充_标注\对接'
# path = r'D:\zhou\数据集\New\dataset_删减版_加类别_扩充_标注\钢筋'
# path = r'D:\zhou\数据集\New\dataset_删减版_加类别_扩充_标注\内角焊'
# path = r'D:\zhou\数据集\New\dataset_删减版_加类别_扩充_标注\外角焊'
path = r'D:\zhou\数据集\New\dataset_删减版_加类别_扩充_标注\直线圆弧'

json_files = os.listdir(path)
save_path = os.path.join(path,'labels')
if os.path.exists(save_path)==False:
    os.makedirs(save_path)

for json_file in json_files:
    if json_file.endswith('.json'):
        cmdline = 'labelme_json_to_dataset ' + os.path.join(path,json_file)
        os.system(cmdline)
        json_path = os.path.join(path,json_file.split('.')[0]+'_json')
        label = plt.imread(os.path.join(json_path,'label.png'))
        label = cv2.cvtColor(np.asarray(label), cv2.COLOR_RGB2BGR)
        # cv2.imshow('label',label)
        # print(label)
        b, g, r = cv2.split(label)
        r[g != 0] = 0
        r[r != 0] = 255
        # break
        plt.imsave(os.path.join(save_path,json_file.replace('.json','.png')), r, cmap=plt.gray())
        # break
        # plt.imshow(label)
        # plt.show()

