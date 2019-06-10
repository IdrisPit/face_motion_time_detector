import cv2,time, pandas
from datetime import datetime


key = []
first_frame = None
status_list=[None,None]
video = cv2.VideoCapture(0)
times = []
df=pandas.DataFrame(columns=["Start", "End"])

while True:
    check, frame = video.read()
    status=0
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)  # blurs the image, removes noise

    # first frame variable
    if first_frame is None:
        first_frame = gray
        continue

    # delta frame variable (apply difference between first frame and current frame)
    delta_frame = cv2.absdiff(first_frame, gray)
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)  # removes white holes / smoothes image

    # contours method
    (_,cnts,_) = cv2.findContours(int((thresh_frame.copy(), cv2.RETR_EXTERNAL(), cv2.CHAIN_APPROX_SIMPLE())) # METHODS OPENCV APPLIES TO RETRIEVING COUNTOURS




    for contours in cnts:
        if cv2.contourArea(contours) < 10000:
            continue
    status=1


        (x, y, w, h) = cv2.boundingRect(contours)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        status_list=append(status)
            if status_list[-1]==1 and status_list[-2]==0:
                times.append(datetime.now())
            if status_list[-1]==0 and status_list[-2]==1:
                times.append(datetime.now())

    cv2.imshow("Gray Frame", gray)
    cv2.imshow("Delta Frame", delta_frame)
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Color Frame", color_frame)

    key = cv2.waitKey(1)
    print(gray)
    print(delta_frame)

    if key == ord('q'):
        if status_list==1:
            times.append(datetime.now())
        break


print(status_list)



for i in range(0,len(times),2):
    df=df.append({"Start":times[i],"End",[i+1]},ignore_index=True)


df.to_csv("Times.csv")
video.release()
print(times)
cv2.destroyAllWindows

