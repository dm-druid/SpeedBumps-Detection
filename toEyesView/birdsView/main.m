im = imread('im5.jpg');
% imshow(im);
% [xi,yi] = getpts();

% dd = 200;
% IM3.JPG
% xi2 = [2,3,0,1,2,3,0,1,2,3,1,2,3,4,2,3]*dd;
% yi2 = [0,0,2,2,2,2,3,3,3,3,4,4,4,4,5,5]*dd;
% 
% K = fitgeotrans([xi yi],[xi2;yi2]','projective');
B = imwarp(im,K);
imshow(B(2000:3000, 2500:3700,:));
[xi,yi] = getpts();