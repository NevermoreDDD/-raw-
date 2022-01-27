import cv2
import os
import glob
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


class RawFile:
    def __init__(self, img_path, dtype, height, width, logger):
        self.dtype = np.uint8 if dtype == 'uint8' else np.uint16
        self.img_data = np.fromfile(img_path, self.dtype)
        self.img_path = img_path
        self.width = width
        self.height = height
        self.logger = logger

    def handle_img(self):
        if self.img_data is None:
            return None
        try:
            self.img_data = self.img_data.reshape(self.height, self.width, 1)
        except ValueError as e:
            self.logger.error(f"{self.img_path} has something wrong")
            return None
        else:
            if self.dtype == np.uint16:
                img = (self.img_data / 256).astype('uint8')
            else:
                img = self.img_data
            img_guassian = cv2.GaussianBlur(img, (5, 5), 1)
            # plt.imshow(img_guassian, cmap="gray")
            # plt.show()
            # print(img_guassian)
            img_gamma = np.power(img / float(np.max(img_guassian)), 0.45)
            img_gamma = (img_gamma*255).astype('uint8')
            img_guassian = cv2.GaussianBlur(img_gamma, (5, 5), 1)
            img_raw = cv2.resize(img_guassian, dsize=(self.height, self.width), interpolation=cv2.INTER_CUBIC)
            # img_512 = cv2.cvtColor(img_512, cv2.COLOR_BGR2GRAY)
            # cv2.imshow("image", img_512)
            # cv2.waitKey(0)
            # plt.imshow(img_512,cmap="gray")
            # plt.show()
            # print((img_512.dtype))
            return img_raw


if __name__ == '__main__':
    logger = 1
    data = RawFile(r"D:\autoprocess\auto_test\2\13323496096.raw",'uint16',1080,1440,logger)
    data.handle_img()
    # cv2.imwrite("img.jpg",data)
    # cv2.imshow("img",data)
    # data = np.fromfile(r"D:\matlab-test\auto_test\1440_1056_1.raw", np.uint8)
    # print(data)

