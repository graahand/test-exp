# ISSAC ROS NVIDIA

## Monocular Camera Calibration for Issac ROS

Calibration means estimating the intrinsic and extrinsic parameters of the camera to accurately map the 2D image points to 3D  world point for tasks such as depth estimation, object localization and 3D reconstruction. 

1. Intrinsic Parameters (Camera-specific properties):

**Focal length (fx, fy)**: Determines how the scene is projected onto the image plane, how much lens magnifies the image. 
**Principal point (cx, cy)**: The optical center of the camera.
**Lens distortion coefficients**: Accounts for radial and tangential distortions caused by the lens.

1. Extrinsic Parameters (Camera's position and orientation in the world):

**Rotation matrix (R**): Defines the camera's orientation.
**Translation vector (t)**: Defines the camera's position relative to the world.

# NOTES

### V4L

Video for Linux is a Linux kernel API for video capture devices like web cameras and TV tuners.

### UVC (USB Video Camera)

is a USB standard that allow  the communication between video capture devices with operating system, it also eliminates the need of device-specific drivers and works with standard driver like UVC and DirectShow.

**Distortion Coefficients Calculation** 

The distortion coefficients are determined by the camera calibration algorithms like CheckerBoard method and April Tags and ArUco Markers.

The algorithm calculates following information:

| The solver estimates:
Distortion coefficients (k1, k2, k3, p1, p2)
Camera matrix (fx, fy, cx, cy)
Extrinsic (camera position & orientation) |
| --- |

![image.png](attachment:b5065ac8-e48b-40d3-bad4-be9d7d086c5a:image.png)

**Examples showcasing Radial and Tangential Distortion**