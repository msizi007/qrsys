import cv2
from pyzbar.pyzbar import decode
import numpy as np
import qrcode
import datetime
import time
from models import Student, Scan
from setup import session, db, app

globs = {
    'ALL_STUDENTS': None,
    'ALL_STUDENT_NUMBERS': None,
    'MOST_RECENT_ACCESS': None,
    'SCAN_TIME_BETWEEN_LOGS': 0,
}

class Scanner:
    def __init__(self, id):
        self.id = id

        if self.id:
            self.all_students = Student.query.all()
            self.all_student_numbers = [str(stu.number) for stu in self.all_students]
        self.most_recent_access = dict()
        self.scan_time_between_logs = 60

        self.vid_capture = cv2.VideoCapture(1)

    def activate(self):

        while True:
            ret, frame = self.vid_capture.read()

            qr_info = decode(frame)

            # if a QR code is detected (more than 0), process it
            if len(qr_info) > 0:
                qr = qr_info[0]

                data = qr.data
                rect = qr.rect
                polygon = qr.polygon

                print('My Code', data.decode(), type(data.decode()), type(self.all_student_numbers[0]))
                # if the detected code is in allowed codes, allow access (save the log) else deny
                if data.decode() in self.all_student_numbers: 
                    cv2.putText(frame, 
                        'ACCESS GRANTED',
                        (rect.left, rect.top - 15),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        2)
                    
                    # if the data is not in most recent keys or time between logs is > 60s then save log
                    if data.decode() not in self.most_recent_access.keys() \
                    or time.time() - self.most_recent_access[data.decode()] > self.scan_time_between_logs:
                        self.most_recent_access[data.decode()] = time.time()
                        with open('log.txt', 'a') as fl:
                            fl.write(f'{data.decode()} logged at {datetime.datetime.now()} \n')

                    # save log data on db (scan)
                    self.save_log(data.decode(), self.id)
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

    def deactivate(self):
        cv2.waitKey(1)
        self.vid_capture.release()
        cv2.destroyAllWindows()

    def save_log(self, stud_num, scanner_id):
        scan_log = Scan(
            student_number = stud_num,
            scanner_id = scanner_id,
            timestamp = datetime.datetime.now()
        )
        with app.app_context():
            db.session.add(scan_log)
            db.session.commit()
