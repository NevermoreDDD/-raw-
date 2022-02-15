import os
import shutil

path = r'D:\zhou\数据集\wholedataset\images'
images_names = os.listdir(path)
file_0 = []
file_1 = []
file_2 = []
file_3 = []
file_4 = []
file_5 = []
file_6 = []
file_7 = []
file_8 = []
file_9 = []
file_10 = []
file_11 = []
file_12 = []
file_13 = []

for image_name in images_names:
    if image_name.find('(') == -1:
        file_0.append([image_name])
    # print(image_name,image_name.find('('))
for filename in file_0:

print(len(file_0))