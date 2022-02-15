import numpy as np
import cv2
import os
from matplotlib import pyplot as plt
def cv_show(img):
    cv2.imshow("image",img)
    cv2.waitKey(0)


# path_dataset_images = r'D:\zhou\数据集\wholedataset\images'
# path1_dataset_labels = r'D:\zhou\数据集\wholedataset\labels'
path_dataset_images =  r'D:\zhou\数据集\New\dataset_删减版_加类别_扩充_标注_训练用\images'
# path1_dataset_labels = r'D:\zhou\数据集\New\dataset_删减版_加类别_扩充_标注_训练用\labels'
path1_dataset_labels = r'D:\zhou\数据集\Results'
filenames = os.listdir(path1_dataset_labels)
for idx,filename in enumerate(filenames):
    # if filename != '2249.png':
    #     continue

    label_path = os.path.join(path1_dataset_labels,filename)
    data_label = np.array(plt.imread(label_path)).astype(dtype=np.uint8)
    # data_label = cv2.cvtColor(data_label, cv2.COLOR_RGB2GRAY)
    data_label = cv2.resize(data_label, (512, 512))
    data_label[data_label!=0] = 255

    img_path = os.path.join(path_dataset_images,filename)
    data_image = plt.imread(img_path)
    data_image = cv2.cvtColor(np.asarray(data_image), cv2.COLOR_RGB2BGR)
    data_image = cv2.resize(data_image,(512,512))
    # cv2.imshow("image_", data_image)

    # print(data_label)

    contours, hierarchy = cv2.findContours(data_label, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(data_image, contours, -1, (0, 255, 0), 1)
    # data_label[data_label !=0] = 255
    # cv2.imshow("raw_label", data_label)

    # b, g, r = cv2.split(data_image)
    # b[data_label == 255] = 255
    # r[data_label == 255] = 255
    # new_image = cv2.merge((b, g, r))

    cv2.imshow("raw_label_image", data_image)
    cv2.waitKey(0)
