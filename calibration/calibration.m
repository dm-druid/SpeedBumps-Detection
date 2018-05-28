% Auto-generated by cameraCalibrator app on 26-May-2018
%-------------------------------------------------------


% Define images to process
imageFileNames = {'/Users/lyq/PycharmProjects/CV/SpeedBumps-Detection/images/calibration/0.jpg',...
    '/Users/lyq/PycharmProjects/CV/SpeedBumps-Detection/images/calibration/1.jpg',...
    '/Users/lyq/PycharmProjects/CV/SpeedBumps-Detection/images/calibration/2.jpg',...
    '/Users/lyq/PycharmProjects/CV/SpeedBumps-Detection/images/calibration/3.jpg',...
    '/Users/lyq/PycharmProjects/CV/SpeedBumps-Detection/images/calibration/4.jpg',...
    '/Users/lyq/PycharmProjects/CV/SpeedBumps-Detection/images/calibration/5.jpg',...
    '/Users/lyq/PycharmProjects/CV/SpeedBumps-Detection/images/calibration/6.jpg',...
    '/Users/lyq/PycharmProjects/CV/SpeedBumps-Detection/images/calibration/7.jpg',...
    '/Users/lyq/PycharmProjects/CV/SpeedBumps-Detection/images/calibration/8.jpg',...
    '/Users/lyq/PycharmProjects/CV/SpeedBumps-Detection/images/calibration/9.jpg',...
    '/Users/lyq/PycharmProjects/CV/SpeedBumps-Detection/images/calibration/10.jpg',...
    '/Users/lyq/PycharmProjects/CV/SpeedBumps-Detection/images/calibration/11.jpg',...
    '/Users/lyq/PycharmProjects/CV/SpeedBumps-Detection/images/calibration/12.jpg',...
    '/Users/lyq/PycharmProjects/CV/SpeedBumps-Detection/images/calibration/13.jpg',...
    '/Users/lyq/PycharmProjects/CV/SpeedBumps-Detection/images/calibration/14.jpg',...
    '/Users/lyq/PycharmProjects/CV/SpeedBumps-Detection/images/calibration/15.jpg',...
    '/Users/lyq/PycharmProjects/CV/SpeedBumps-Detection/images/calibration/16.jpg',...
    '/Users/lyq/PycharmProjects/CV/SpeedBumps-Detection/images/calibration/17.jpg',...
    };

% Detect checkerboards in images
[imagePoints, boardSize, imagesUsed] = detectCheckerboardPoints(imageFileNames);
imageFileNames = imageFileNames(imagesUsed);

% Generate world coordinates of the corners of the squares
squareSize = 65;  % in units of 'mm'
worldPoints = generateCheckerboardPoints(boardSize, squareSize);

% Calibrate the camera
[cameraParams, imagesUsed, estimationErrors] = estimateCameraParameters(imagePoints, worldPoints, ...
    'EstimateSkew', false, 'EstimateTangentialDistortion', false, ...
    'NumRadialDistortionCoefficients', 3, 'WorldUnits', 'mm', ...
    'InitialIntrinsicMatrix', [], 'InitialRadialDistortion', []);

% View reprojection errors
h1=figure; showReprojectionErrors(cameraParams);

% Visualize pattern locations
h2=figure; showExtrinsics(cameraParams, 'CameraCentric');

% Display parameter estimation errors
displayErrors(estimationErrors, cameraParams);

% For example, you can use the calibration data to remove effects of lens distortion.
originalImage = imread(imageFileNames{1});
undistortedImage = undistortImage(originalImage, cameraParams);

% See additional examples of how to use the calibration data.  At the prompt type:
% showdemo('MeasuringPlanarObjectsExample')
% showdemo('StructureFromMotionExample')