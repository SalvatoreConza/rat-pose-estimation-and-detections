Tools and AI software for the Behavioural Neuroscience Laboratory.

The keypoint of body parts were done predicted using HRNet. First, we predict the bounding boxes using YOLOv11, and then we predict the body part coordinates using HRNet. This is the custom pipeline. I was focused on the bottom images. 

Here, some predictions for pose estimation, the confidence in the pipeline is set to 1. Custom Pipeline. bottom view. 900 images:

<img width="640" height="360" alt="R1_mike_20250311_170_1_V01_168" src="https://github.com/user-attachments/assets/f05d1271-1129-4898-85b1-9a4ba8c265ff" />

<img width="620" height="360" alt="R1_mike_20250311_170_1_V01_914" src="https://github.com/user-attachments/assets/6e5f9807-f2b3-43d0-b000-bbdde12c7408" />

<img width="620" height="360" alt="R1_mike_20250311_180_1_V01_709" src="https://github.com/user-attachments/assets/175ee38a-a782-4945-8365-5d2e487a2ddf" />
<br />
<br />
<br />

Here, some results on the test set for pose estimation. prediction vs results. Custom Pipeline. bottom view. 900 images:
<img width="850" height="850" alt="32" src="https://github.com/user-attachments/assets/95514366-4e36-4d42-8661-d782bee2e4e4" />

<img width="850" height="850" alt="15" src="https://github.com/user-attachments/assets/ce3a11b9-6d85-4170-b6f1-12677b1db9c2" />

<img width="850" height="850" alt="12" src="https://github.com/user-attachments/assets/a87ac94b-6ca1-4e40-9a1a-7b43985d9ecf" />
<br />
<br />
<br />

Here, some train, test and val batches for detection. Custom Pipeline. bottom view. 900 images:

<img width="400" height="300" alt="image" src="https://github.com/user-attachments/assets/19a068f6-8c16-459f-a25e-4d8a569591c5" />






