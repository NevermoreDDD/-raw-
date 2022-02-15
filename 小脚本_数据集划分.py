import os
import shutil

import numpy as np
import random
import glob
import re

path = r'D:\zhou\数据集\New\dataset_删减版_加类别_扩充'
folds = os.listdir(path)
random.seed(0)
train_txt = []
val_txt = []
test_txt = []
for fold in folds:
    fold_path = os.path.join(path,fold)
    images_names = os.listdir(fold_path)
    for idx in range(len(images_names)-1,0,-1):
        if images_names[idx].endswith('.png') == False:
            images_names.remove(images_names[idx])
    random.shuffle(images_names)
    train = images_names[:38]
    val = images_names[38:45]
    test = images_names[45:]
    train_txt.append(train)
    val_txt.append(val)
    # print(train)
    # print(val)
    # print(test)
    # print(len(train),len(val),len(test))
    test_txt.append(test)

        # print(len(train),len(val),len(test))
        # break

train_txt = np.array(train_txt).reshape(-1)
val_txt = np.array(val_txt).reshape(-1)
test_txt = np.array(test_txt).reshape(-1)
# print(train_txt)
# print(test_txt)
# print(len(train_txt),len(val_txt),len(test_txt))

# for item in train_txt:
#     print(item)
save_path = r'D:\zhou\数据集\New\dataset_删减版_加类别_扩充_标注_训练用\ImageSets'
# np.savetxt(os.path.join(save_path,'train.txt'),train_txt)
# np.savetxt(os.path.join(save_path,'val.txt'),val_txt)
# np.savetxt(os.path.join(save_path,'test.txt'),test_txt)


with open(os.path.join(save_path,'train.txt'),'w') as f:
    for item in train_txt:
        f.write(item)
        f.write('\n')

with open(os.path.join(save_path,'val.txt'),'w') as f:
    for item in val_txt:
        f.write(item)
        f.write('\n')

with open(os.path.join(save_path,'test.txt'),'w') as f:
    for item in test_txt:
        f.write(item)
        f.write('\n')


raw_images_path = r'D:\zhou\数据集\New\dataset_删减版_加类别_扩充_标注_训练用\images'
raw_labels_path = raw_images_path.replace('images','labels')
dataset_images_path = r'D:\zhou\数据集\New\dataset_删减版_加类别_扩充_标注_训练用拆分\images'
dataset_labels_path = dataset_images_path.replace('images','labels')

for item in train_txt:
    shutil.copy(os.path.join(raw_images_path, item),os.path.join(dataset_images_path,'train',item))
    shutil.copy(os.path.join(raw_labels_path,item), os.path.join(dataset_labels_path, 'train' ,item))

for item in val_txt:
    shutil.copy(os.path.join(raw_images_path,item),os.path.join(dataset_images_path,'val', item))
    shutil.copy(os.path.join(raw_labels_path, item), os.path.join(dataset_labels_path,'val', item))

for item in test_txt:
    shutil.copy(os.path.join(raw_images_path,item),os.path.join(dataset_images_path,'test', item))
    shutil.copy(os.path.join(raw_labels_path, item), os.path.join(dataset_labels_path,'test', item))