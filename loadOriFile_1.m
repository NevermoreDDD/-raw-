function [laserArr,fnumL] = loadOriFile_1(filepath, info_figure)

%获得指定文件夹下所有文件夹和文件，dir('*.m')列出当前目录下符合正则表达式的文件夹和文件
tmpL = dir([filepath, '*', info_figure.fmt]);  
fnumL = length(tmpL);
% if(fnumL > 120)
%     fnumL = 120;
% end
laserArr = zeros(info_figure.height, info_figure.width, fnumL, info_figure.bits);
if strcmp(info_figure.fmt, '.bmp')
    for i=1:fnumL
        filenameL = [filepath,tmpL(i).name];
        imgL = imread(filenameL);
        laserArr(:,:,i) = imgL;
    end
elseif strcmp(info_figure.fmt, '.raw')
    for i=1:fnumL
        filenameL = [filepath, tmpL(i).name];
        fid = fopen(filenameL);
        imgL = fread( fid, [info_figure.width, info_figure.height],info_figure.bits )';
        fclose(fid);
        laserArr(:,:,i) = imgL;
    end
else
    error([fmt ' file type is not support']);
end
%     disp('运行到此');
% for i = 1 :  fnumL
%     name =  tmpL(i).name;
%     name
%     idx1 = strfind(name, '_');
% %     idx2 = strfind(name, fmt);
%     dis = name(idx1(2)+1: idx1(3)-1);
%     infoArr(i) = str2double(dis);%infoArr是某一帧拍摄时候z轴上的刻度距离
% end
end