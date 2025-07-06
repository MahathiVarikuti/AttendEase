import numpy as np
import cv2
import face_recognition
import mysql.connector
import pickle
import zlib
from datetime import datetime, date
import os
from dotenv import load_dotenv
import mysql.connector


load_dotenv()

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = db.cursor()

#from known faces in db
cursor.execute("SELECT first_name, roll_number, face_encoding FROM student")
data = cursor.fetchall()

known_encodings, known_names, known_rolls = [], [], []
for name, roll, enc_blob in data:
    try:
        encoding = pickle.loads(zlib.decompress(enc_blob))
        known_encodings.append(encoding)
        known_names.append(name)
        known_rolls.append(roll)
    except Exception as e:
        print(f"Error decoding face for {name}: {e}")

print("Loaded encodings from student table.")


def mark_attendance(name, roll):
    today = date.today()
    now = datetime.now().strftime('%H:%M:%S')
    cursor.execute("SELECT * FROM attendance WHERE student_name=%s AND date=%s", (name, today))
    if cursor.fetchone() is None:
        cursor.execute(
            "INSERT INTO attendance (student_name, roll_number, date, time) VALUES (%s, %s, %s, %s)",
            (name, roll, today, now)
        )
        db.commit()
        print(f"Marked attendance for {name} at {now}")


cap = cv2.VideoCapture(0)

while True:
    db.ping(reconnect=True)
    success, img = cap.read()
    if not success:
        break

    img_small = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
    rgb_small = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)

    faces = face_recognition.face_locations(rgb_small)
    encodings = face_recognition.face_encodings(rgb_small, faces)

    for encodeFace, faceLoc in zip(encodings, faces):
        matches = face_recognition.compare_faces(known_encodings, encodeFace)
        face_distances = face_recognition.face_distance(known_encodings, encodeFace)

        if len(face_distances) > 0:
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = known_names[best_match_index]
                roll = known_rolls[best_match_index]


                y1, x2, y2, x1 = [v * 4 for v in faceLoc]

                # b box
                cv2.rectangle(img, (x1, y1), (x2, y2), (147, 20, 255), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (147, 20, 255), cv2.FILLED)
                cv2.putText(img, name.upper(), (x1 + 6, y2 - 6),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)


                mark_attendance(name, roll)

    cv2.imshow("Attendance System", img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

