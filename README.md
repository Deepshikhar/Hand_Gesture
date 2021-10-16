

# Hand_Gesture_Recognition
* ## **Introduction**

  In this project we implement a Hand_Gesture_Recognition algorithm using OpenCV and Python3.
  We separate the hand from background using hsv giving it the skin color range to differentiate it from background.
  Now the detected hand is then processed by thresholidng ,using contours and convex hull to count fingers. Finally different hand gestures detected by diffetentiating them by     their extent ratio.


* ## **Tools and hardware used**
1. VsCode
2. Python3
3. Libraries-OpenCV,Numpy
4. WebCam

* ## **Roadmap**
  ![](https://i.imgur.com/aR1ST5C.png)
  <br>Gestures we are detecting</br>
1.  #### Capturing a Video frame ,separating the skin color object :- 
    We take the frame and using hsv (`lower_color_range:[0,58,30] and upper_color_range:[33,255,255]`)we detect the skin color object(hand) in it and using mask extract that object from the frame.<br>
    ![](https://i.imgur.com/w6lqSId.png)<br>
    **Detecting the hand by separating with hsv**

2. #### Reducing the Noise:-
 *   The technique of Dilation is used to dilate the image using `5*5` kernel to remove black spots or noise in the image. Then we blur the image using `bilateralFiler` or we can use GaussianBlur      for smoothing the image. We are interested in shape of the image not the details in it.<br>
 ![](https://i.imgur.com/GxqR7OV.png) <br>**Image before dilation**<br>
 ![](https://i.imgur.com/B6WSaAH.png)<br>
**Blurred Image after dilation removing black spots and noise**


3. #### Thresholding:-
  * First we convert our BGR image to  greyscale image.
  * We use thresholding for image segmentation i.e. to create binary image from greyscale image.
  * Basically thresholding is like a filter which we use to separate out the image corresponding to objects which we want to process.This is done by allowing the particular         color to appear as white while showing other colors as black.
  * After separating the specific pixels, we can assign them determined values i.e. we can assigh 255(white) and 0(black).
  * There are different types of thresholding:-
    Gaussian Thresholding, Gaussian Adaptive Thresholding, Threshold Binary, threshold Binary Inverted ,Threshold Truncate etc.
  * In our project we are using Threshold Truncate whose value is `98` to separate hand shape from the frame ![](https://i.imgur.com/Ee25Gve.png)<br>
**Threshold image after using Threshold Truncate technique**


4. #### Finding the contours ,convex hull and convexity defects:-
    We find the contours in the threshold image and then select the contour of maximum area. Then we make the convex hull around the hand .Now we find the convex points and         defects in the contour. The convex points are end points or points at the tip of the finger and the points which are far away from the contour are convexity defects. With       the help of these points we find the number of fingers extended.<br>
    ![](https://i.imgur.com/OKxxKcO.png)<br>
    **Drawing contours around hand**<br>
    ![](https://i.imgur.com/zbuJE09.png)<br>
    **Drawing hull around the hand**<br>
    ![](https://i.imgur.com/pMrx1vf.png)<br>
    **Representing the defects points in the valley between two fingers**




5. #### Finding the area of contour and hull:-
    Next we find the area of hull and area of contour which we will be used as other criteria to differentiate the other fingers number after using number of convexity defects.


- ## Final Result:-
<br>![](Fingers_detection.gif)</br>
