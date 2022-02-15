import os
import shutil

path = r'D:\zhou\数据集\New\matlab_images'

save_path = r'D:\zhou\数据集\New\dataset'
fold_names = os.listdir(path)
print(fold_names)
cnt = 0
for folename in fold_names:
    img_path = os.path.join(path,folename)
    imgs_names = os.listdir(img_path)
    print(imgs_names)
    imgs_nums = len(imgs_names)
    # print(len(imgs_names))
    if imgs_nums == 0:
        continue
    if imgs_nums <= 10:
        for img_name in imgs_names:
            # shutil.copy(os.path.join(img_path, img_name), os.path.join(save_path, str(cnt) + '.png'))
            print(cnt,os.path.join(img_path, img_name), os.path.join(save_path, str(cnt) + '.png'))
            cnt += 1
    else:
        interval = imgs_nums//10
        for i in range(10):
            # shutil.copy(os.path.join(img_path, imgs_names[interval*i]), os.path.join(save_path, str(cnt) + '.png'))
            print(cnt,os.path.join(img_path, imgs_names[interval*i]), os.path.join(save_path, str(cnt) + '.png'))
            cnt += 1
            # shutil.copy(os.path.join(img_path,img_name),os.path.join(save_path,str(cnt)+'.png'))
    # break
print(cnt)