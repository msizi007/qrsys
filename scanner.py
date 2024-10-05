import cv2
from pyzbar.pyzbar import decode
import numpy as np
import qrcode
import datetime
import time

# list of all allowed users
users = []
# get a list of all allowed users
with open('allowed.txt', 'r') as fl:
    users = [l[:-1] for l in fl.readlines() if len(l) > 2]

# initiate video capture
cap = cv2.VideoCapture(1)

# dictionary containing all recent logins
most_recent_access = dict()
# time frame between logins (logs)
time_between_logs = 60

while True:
    ret, frame = cap.read()

    qr_info = decode(frame)

    # if a QR code is detected (more than 0), process it
    if len(qr_info) > 0:
        qr = qr_info[0]

        data = qr.data
        rect = qr.rect
        polygon = qr.polygon

        # if the detected code is in allowed codes, allow access (save the log) else deny
        if data.decode() in users: 
            cv2.putText(
            frame, 
            'ACCESS GRANTED',
            (rect.left, rect.top - 15),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2)



            # if the data is not in most recent keys or time between logs is > 60s then save log
            if data.decode() not in most_recent_access.keys() \
            or time.time() - most_recent_access[data.decode()] > time_between_logs:
                most_recent_access[data.decode()] = time.time()
                with open('log.txt', 'a') as fl:
                    fl.write(f'{data.decode()} logged at {datetime.datetime.now()} \n')
        else:
            cv2.putText(
            frame, 
            'ACCESS DENIED',
            (rect.left, rect.top - 15),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2)
            with open('spam.txt', 'a') as fl:
                fl.write(f'[FRAUD!]: {data.decode()} @{datetime.datetime.now()} \n')

        # display rectangle and polygon
        frame = cv2.rectangle(frame, 
            (rect.left, rect.top),
            (rect.left + rect.width, rect.top + rect.height),
            (0, 255, 0), 2)
        
        frame = cv2.polylines(frame, 
            [np.array(polygon)],
            True, (255, 0, 0), 5)

    # display camera (frame)
    cv2.imshow('video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
