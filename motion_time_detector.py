import cv2, time, pandas
from datetime import datetime

first_frame=None
status_list=[None, None]
times=[]
df=pandas.DataFrame(columns=["Start", "End"])

video=cv2.VideoCapture(0)

while True: 
    check, frame = video.read()
    status=0 #denotes no motion in frame

    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(21,21),0) #blurs the image, removes noise

    #first frame variable
    if first_frame is None:
        first_frame=gray
        continue
    
    #delta frame variable (apply difference between first frame and current frame)
    delta_frame=cv2.absdiff(first_frame, gray)
    thresh_frame=cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame= cv2.dilate(thresh_frame, None, iterations=2) #removes white holes / smoothes image

    #contours method
    (_,cnts,_)=cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #METHODS OPENCV APPLIES TO RETRIEVING COUNTOURS

    for contours in cnts: 
        if cv2.contourArea(contours) < 10000: #100x100 pixels
            continue
        status = 1 #denotes object in motion of frame

        (x,y,w,h) = cv2.boundRect(contour)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0),3)

    status_list.append(status)

    if status_list[-1]==1 and status_list[-2]==0:
        times.append(datetime.now())
    if status_list[-1]==1 and status_list[-2]==1:
        times.append(datetime.now())
    

    cv2.imshow("Gray Frame", gray)
    cv2.imshow("Delta Frame", delta_frame)
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Color Frame", frame)

    key=cv2.waitKey(1)

    if key == ord('q'):
        if status == 1:
            times.append(datetime.now())
        break

print(status_list)
print(times)

for i in range(0,len(times),2):
    df = df.append({"Start": times[i], "End":times[i+1]}, ignore_index=True)

df.to_csv("motion_times.csv")
    
video.release()
cv2.destroyAllWindows

