# Data augmentation using brightness and darkness to enhance the performance of yolo7 object detection algorithm 
[Abdulghani M. Abdulghani]
## From Abstract

Data augmentation is used for diversifying and expanding the dataset for object detection. YOLOv7 was trained Open Images dataset containing 4 different classes. The dataset was augmented using two different augmentation technique (data brightness and data darkness). Data augmentation contributed to the performance gain for all classes in the dataset by increasing the mAP@.5 value by 13% and F1-score by 11%. 

## From Introduction
Data augmentation techniques increase the size of images and generate new data instead of adding more images to your dataset and labelling them. **The study aims to choose the best data augmentation techniques to help expand dataset and performance metrics including Mean Average Precision (mAP), Precision and Recall for object detection.**

## Summary 

Abdulghani M. Abdulghani explored the use of data augmentation to enhance object detection performance. YOLOv7 was trained on a subset of the Open Images dataset comprising four object classes. The dataset was augmented using two distinct techniques: brightness enhancement and brightness reduction. Rather than collecting and labeling additional images, these augmentation strategies expanded the dataset by generating synthetic variations of existing samples. The study was aimed to identify the most effective augmentation methods for improving performance metrics such as mean average precision (mAP), precision, and recall. Results showed that data augmentation improved performance across all object classes, increasing mAP@0.5 by 13% and F1 score by 11%, highlighting the value of targeted photometric strategies in object detection. 


######################################################################################

In summary, techniques ranging from basic image transformations to advanced deep learning methods are used to apply data augmentation to computer vision datasets. Augmentation timing can affect the authenticity of generated samples and their contribution to model learning. Information theory also suggests that retaining original data characteristics during augmentation is crucial for preserving useful features, reducing redundancy, and maximizing a model’s ability to generalize to unseen scenarios. Our study provides evidence that augmentation timing is a key factor in enhancing model performance and generalizability.