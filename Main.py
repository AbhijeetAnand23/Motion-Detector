import cv2
import pandas
from datetime import datetime


video = cv2.VideoCapture(0)
first_frame = None
status_list = [None, None]
timestamp = []
df = pandas.DataFrame(columns=["Start", "End"])

while True:
    check, color_frame = video.read()
    status = 0

    if first_frame is None:
        first_frame = color_frame
        grey_first_frame = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
        continue

    grey_frame = cv2.cvtColor(color_frame, cv2.COLOR_BGR2GRAY)
    blur_grey_frame = cv2.GaussianBlur(grey_frame, (21, 21), 0)
    delta_frame = cv2.absdiff(grey_first_frame, grey_frame)
    thresh_frame = cv2.threshold(delta_frame, 100, 255, cv2.THRESH_BINARY)[1]
    thresh_frame_dilated = cv2.dilate(thresh_frame, None, iterations=2)

    (cnts, _) = cv2.findContours(thresh_frame_dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        else:
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(color_frame, (x, y), ((x + w), (y + h)), (0, 255, 0), 3)
            status = 1

    status_list.append(status)
    if status_list[-1] == 1 and status_list[-2] == 0:
        timestamp.append(datetime.now())
    if status_list[-1] == 0 and status_list[-2] == 1:
        timestamp.append(datetime.now())

    cv2.imshow("Color Frame", color_frame)
    cv2.imshow("Grey Frame", grey_frame)
    cv2.imshow("Delta Frame", delta_frame)
    cv2.imshow("Thresh Frame", thresh_frame)
    key = cv2.waitKey(1)

    if key == ord("q"):
        if status == 1:
            timestamp.append(datetime.now())
        break

for i in range(0, len(timestamp), 2):
    df = df.append({"Start": timestamp[i], "End": timestamp[i + 1]}, ignore_index=True)
df.to_csv("timestamp.csv")

video.release()
cv2.destroyAllWindows()
