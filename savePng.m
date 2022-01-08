warning off all
close all
clc
% R0000*.png Ϊԭͼ�ֱ���
% S0000*.png Ϊ512*512�ֱ���

fid = fopen('loadFile.txt','r','n','UTF-8');
FILE = textscan(fid,'%s');
fclose(fid);
info_figure  =  struct('width', 1920, 'height', 1080, 'fmt', '.raw', 'bits', 'uint16'); % ����ͼ����Ϣ
filepath = FILE{1,1}{1,1};
savepath = FILE{1,1}{2,1};
pathF = FILE{1,1}{3,1};
info_figure.width = str2double(FILE{1,1}{4,1});
info_figure.height = str2double(FILE{1,1}{5,1});
info_figure.bits = FILE{1,1}{6,1};
[laserArr,frames] = load_raw_File([filepath '\'], info_figure);
%{
clear
filepath  =  '\\192.168.2.58\weld_data_line\temppp\N-01\N-07'; % rawͼ�ļ���ַ
pathF = '28ѣ��'; %�����ַ��ÿ�ζ��ø�
savepath = 'C:\����\000\gamma�任 + ����ͼƬ\gamma�任 + ����ͼƬ'; % ͼƬ�����ַ

info_figure  =  struct('width', 1056, 'height', 1440, 'fmt', '.raw', 'bits', 'uint8'); % ����ͼ����Ϣ

% [laserArr,frames]  =  loadOriFile_1([filepath '\'], info_figure);
[laserArr,frames] = load_raw_File([filepath '\'], info_figure);
%}

mkdir([savepath '\' pathF 'ScaleRaw']);
mkdir([savepath '\' pathF 'Scale512']);
fkernel = fspecial('gaussian', [5, 5], 1);
for frame = 1 : frames
   % �˲�
   img = laserArr(:, :, frame);
%    imshow(img);
   img_filter = imfilter(img, fkernel);
%    laserArr1 = double(img)/65535;
%    img_filter = uint16(bfilter2(laserArr1,6,[1,1])*65535);
   % BLC
   img_blc = img_filter - min(img_filter(:)) + 200;
   % ٤��
   imageGamma = imadjust(img_filter, [], [], 0.45);
   image8 = im2uint8(imageGamma);
   % �˲�
   img_filter = imfilter(image8, fkernel);
   imageScale_512 = imresize(img_filter, [512 512], 'bicubic');
   imageScaleHalf = imresize(img_filter, 0.5);
%    subplot(131);imshow(img_filter);title('original');
%    subplot(133);imshow(imageScale_512);title('512 �� 512');
%    subplot(132);imshow(imageScaleHalf);title('half');
   imwrite(imageScale_512, [savepath '\' pathF 'Scale512\' num2str(frame, '%05d') '.png']);
   imwrite(img_filter, [savepath '\' pathF 'ScaleRaw\' num2str(frame,'%05d') '.png']);
end
%




