import os
from matplotlib import pyplot as plt
import cv2
import numpy as np
path = r'D:\User\Desktop\111'

labels_names = os.listdir(path)
label = plt.imread(os.path.join(path,'label.png'))
for label_name in labels_names:
        label_path = os.path.join(path,label_name)
        plt.imsave(os.path.join(label_path), label, cmap=plt.gray())
        # plt.imshow(label)
        # plt.show()

