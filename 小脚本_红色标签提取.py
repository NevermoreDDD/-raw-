import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
path = r'D:\zhou\数据集\wholedataset_backup\labels'
save_path = r'D:\zhou\数据集\wholedataset\labels'
labels_names = os.listdir(path)
for label_name in labels_names:
    print(os.path.join(path,label_name))
    label = plt.imread(os.path.join(path,label_name))
    label = cv2.cvtColor(np.asarray(label), cv2.COLOR_RGB2BGR)
    # cv2.imshow('label',label)
    # print(label)
    b,g,r = cv2.split(label)
    r[g!=0]=0

    # cv2.imshow('r',r)
    r[r!=0]=255
    plt.imsave(os.path.join(save_path,label_name),r,cmap = plt.gray())
    # break
    # cv2.waitKey(0)