function [laserArr,fnumL] = loadOriFile_1(filepath, info_figure)

%���ָ���ļ����������ļ��к��ļ���dir('*.m')�г���ǰĿ¼�·���������ʽ���ļ��к��ļ�
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
%     disp('���е���');
% for i = 1 :  fnumL
%     name =  tmpL(i).name;
%     name
%     idx1 = strfind(name, '_');
% %     idx2 = strfind(name, fmt);
%     dis = name(idx1(2)+1: idx1(3)-1);
%     infoArr(i) = str2double(dis);%infoArr��ĳһ֡����ʱ��z���ϵĿ̶Ⱦ���
% end
end