function [laserArr,fnumL] = load_raw_File(filepath, info_figure)

%���ָ���ļ����������ļ��к��ļ���dir('*.m')�г���ǰĿ¼�·���������ʽ���ļ��к��ļ�
tmpL = dir([filepath, '*', info_figure.fmt]);
fnumL = length(tmpL);
% ����ļ����࣬��ֻ��ȡ�̶�֡��
if(fnumL > 450)
    fnumL = 300;
end
% fnumL = 3;
% ��֤ͼ�� �п� ���� �и�
if(info_figure.width < info_figure.height)
    wid = info_figure.height;
    hei = info_figure.width;
    rotate = 1;
else
    hei = info_figure.height;
    wid = info_figure.width;
    rotate = 0;
end
% ���뱣��ͼ�������ڴ�ռ�
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
