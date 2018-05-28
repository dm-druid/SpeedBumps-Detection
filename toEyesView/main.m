% im = imread('im1.jpg');
% imshow(im);
% [xi,yi] = getpts();

dd = 20;
xi2 = [0,0,1,1,2,2,3,3,4,4,1,2,3,4]*dd;
yi2 = [0,1,0,1,0,1,0,1,0,1,2,2,2,2]*dd;

K = fitgeotrans([xi yi],[xi2;yi2]','projective');
B = imwarp(im,K);
imshow(B);