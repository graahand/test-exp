# Feasibilty Study and Prototyping with 3d reconstruction from 2d images. 

self driving car lacks a advance real world navigation and localization mechanism which is often required for advancing with the development of autonomous vehicles which have the applications areas such as industry robots at coca-cola factory, rod haru weilding garne thauma, aru applications areas, an



with no other resources other than the existing ones, we will perform fast prototyping with 3d reconstruction with 2d images for real world navigation, our resources are enough for such ability for to produce such results according to the study done on this topic. currently our self driving perform segmentation at fixed path with the help of YOLOv11-segmentation model finetuned to deal with the problem of direct sunglight and model le nadekheko naya or odd kura jun real world ma huna sakxa with a real-world dynamic steering control mechanism (we only train for segmentation,we don't actually train the model with steering angle provided as labels) strength {strength maybe}.



## 3d reconstruction

it involves combination of  two things. 

openMVG and openMVS.

mvs means multiple view geometry, which means creating 3d maps with [triangulation](https://en.wikipedia.org/wiki/Triangulation)(producing 3d points based on a special point (base point) from the image (every image contains that))  

mvs means multi view stereo,which further means you get the 3d points from mvs now create a scene for those points connecting the dots (dense point cloud) and this can be rendered in 3d.  


process

Image collection
Feature extraction
Feature matching
Structure from Motion
Dense point-cloud reconstruction
Mesh Reconstruction
Mesh Refinement
Mesh Texturing

you collect twohigh quality images that overlap (matching garna ko lagi) with exif metadata (3d points calculate garna ko lagi (like focal length)). feature extraction is done with the help me algorithms like SIFT, AKAZE, SURF. 






### depth estimation and ed reconstruction
[meta vggt-1b model for 3d reconstruction comes with depth estimation model as well,these can also be experimented and used]




