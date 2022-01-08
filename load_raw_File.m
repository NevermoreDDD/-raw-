function [laserArr,fnumL] = load_raw_File(filepath, info_figure)

%获得指定文件夹下所有文件夹和文件，dir('*.m')列出当前目录下符合正则表达式的文件夹和文件
tmpL = dir([filepath, '*', info_figure.fmt]);
fnumL = length(tmpL);
% 如果文件过多，则只读取固定帧数
if(fnumL > 450)
    fnumL = 300;
end
% fnumL = 3;
% 保证图像 列宽 大于 行高
if(info_figure.width < info_figure.height)
    wid = info_figure.height;
    hei = info_figure.width;
    rotate = 1;
else
    hei = info_figure.height;
    wid = info_figure.width;
    rotate = 0;
end
% 申请保存图像矩阵的内存空间
laserArr = zeros(hei, wid, fnumL, info_figure.bits);
if strcmp(info_figure.fmt, '.raw')
    for i=1:fnumL
        filenameL = [filepath, tmpL(i).name];
        fid = fopen(filenameL);
        imgL = fread( fid, [info_figure.width, info_figure.height],info_figure.bits )';
        fclose(fid);
        if rotate
            laserArr(:,:,i) = imgL';
        else
            laserArr(:,:,i) = imgL;
        end
    end
else
    error([fmt ' file type is not support']);
end
end
