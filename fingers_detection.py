import cv2
import numpy as np
import math


#capturing the video 
cap = cv2.VideoCapture(0)

while(cap.isOpened()):
    try:                    #if there is an error comes or does not detect anything this will try error statement
        ret, frame = cap.read()
        frame=cv2.flip(frame,1)
        if ret==True:
            pass
        
        #making the frame of specific dimension
        frame =frame[100:700,100:700]
                
        
        
        #now using hsv we detect the color of skin
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #defining the range of skin color in hsv
        lower_skin = np.array([0, 58, 30], dtype = "uint8")
        upper_skin = np.array([33, 255, 255], dtype = "uint8")
        
        #applying mask to extract skin color object from the frame        
        mask = cv2.inRange(hsv, lower_skin, upper_skin)
        cv2.imshow("before",mask)
        #now we dilate our skin color object to remove black spots or noise from it
        kernel = np.ones((5,5),np.uint8)
        mask = cv2.dilate(mask,kernel,iterations = 3)

        #now we blur the image to smoothen edges in it 
        blur = cv2.bilateralFilter(mask,9,200,200)
        #blur = cv2.GaussianBlur(blur,(5,5),100) 
        

        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(frame,frame, mask= blur)

        #now converting the image into BGR -> GRAY 
        frame_gray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)

        #thresholding the image
        ret, thresh = cv2.threshold(frame_gray, 98, 255,cv2.THRESH_TRUNC)
        
        #finding contours in the threshold image
        contours,_ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        #selecting the contour of max area 
        cnt = max(contours, key = lambda x: cv2.contourArea(x))
        

        #making the convex hull around the hand 
        hull = cv2.convexHull(cnt)
        #finding the area of hull
        hullarea = cv2.contourArea(hull)
        #finding the area of max contour
        cntarea = cv2.contourArea(cnt)
        #making a rectangle around the hand
        x,y,w,h = cv2.boundingRect(hull)
        frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

        #finding the difference between the hull area and contour area
        reduction = (hullarea-cntarea)

        #taking the ratio of sum of hull area + contour area to the reduction
        ratio=(hullarea+cntarea)/reduction
        print("ratio:",ratio)
        img = cv2.drawContours(frame, hull, -2, (0,0,255), 10)
        
        #first check if contours are detected or not and find convexity defects in it
        if len(contours) > 0:
            hull = cv2.convexHull(cnt, returnPoints=False)
            defects = cv2.convexityDefects(cnt, hull)
            #let us assume n denotes the number of defects in the image
            n = 0
                
            #now we run the loop to find the angles of defects which for a triangle and 
            #avoid those with angles less than 90 degree
            for i in range(defects.shape[0]):
                    s,e,f,d = defects[i,0]
                    first = tuple(cnt[s][0])
                    second = tuple(cnt[e][0])
                    far = tuple(cnt[f][0])
                    cv2.line(img,first,second,[255,0,0],2)
                    cv2.circle(img,far,5,[0,0,255],-1)
                    #now finding the sides of triangle formed by first,second and far point
                    a = math.sqrt((second[0] - first[0])**2 + (second[1] - first[1])**2)
                    b = math.sqrt((far[0] - first[0])**2 + (far[1] - first[1])**2)
                    c = math.sqrt((second[0] - far[0])**2 + (second[1] - far[1])**2)
                    
                    #now we find the angles between the sides of triangle
                    angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57.295
                    if angle <= 90 :
                        n += 1
        
        # Now we are using no. of defects in the image and the ratio to classify the different
        # hand gestures and display the result 
        font = cv2.FONT_HERSHEY_SIMPLEX
        if n == 0 :
            if ratio<19:
                cv2.putText(frame,'1',(0,50), font, 2, (0,0,255), 4, cv2.LINE_AA)
            
            elif ratio>15 and ratio<21:
                cv2.putText(frame,'6',(0,50), font, 2, (0,0,255), 4, cv2.LINE_AA)
            elif ratio>25:
                if ratio<33:
                    cv2.putText(frame,'0',(0,50), font, 2, (0,0,255), 4, cv2.LINE_AA)
                else:
                    cv2.putText(frame,'9',(0,50), font, 2, (0,0,255), 4, cv2.LINE_AA)
          
                

        elif n == 1 :
            if ratio<13:
                cv2.putText(frame,'2',(0,50), font,2, (0,0,255), 4, cv2.LINE_AA)
            elif ratio >11 :
                cv2.putText(frame,'7',(0,50), font, 2, (0,0,255), 4, cv2.LINE_AA)

        elif n == 2:
            if ratio<10:
                cv2.putText(frame,'8',(0,50), font, 2, (0,0,255), 4, cv2.LINE_AA)
            elif ratio>13:
                cv2.putText(frame,'3',(0,50), font, 2, (0,0,255), 4, cv2.LINE_AA)
       
        elif n == 3:
            cv2.putText(frame,'4',(0,50), font, 2, (0,0,255), 4, cv2.LINE_AA)
        elif n == 4:
            cv2.putText(frame,'5',(0,50), font, 2, (0,0,255), 4, cv2.LINE_AA)

        #now displaying the result window
        #cv2.imshow('thresh',thresh)
        cv2.imshow('frame',frame)
        #cv2.imshow('mask',mask)
        #cv2.imshow('contours',img)

    except:
        pass
    #adding delay 
    k = cv2.waitKey(250) & 0xFF 
    if k == 27: #if we press esc then loop will break and our program ends
        break

#releasing the cap and destroying all the windows
cap.release()
cv2.destroyAllWindows()


