import tkinter as tk
from tkinter import messagebox, scrolledtext
import mysql.connector
import face_recognition
import pickle
import numpy as np
import zlib
import cv2
import datetime
import os
from dotenv import load_dotenv


BG_COLOR = "#fffdf5"
BUTTON_COLOR = "#e7f1a8"
TEXT_COLOR = "#364c84"
FONT = ("Trebuchet MS", 14)
HEADER_FONT = ("Trebuchet MS", 30, "bold")

load_dotenv()

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = db.cursor()

# load encodings from student table
cursor.execute("SELECT first_name, last_name, roll_number, face_encoding FROM student")
data = cursor.fetchall()
known_encodings = []
known_names = []
roll_numbers = []

for first, last, roll, enc_blob in data:
    try:
        encoding = pickle.loads(zlib.decompress(enc_blob))
        known_encodings.append(encoding)
        full_name = f"{first} {last}"
        known_names.append(full_name)
        roll_numbers.append(roll)
    except Exception as e:
        print(f"Error decoding for {first} {last}: {e}")

# hui
login_window = tk.Tk()
login_window.title("Student Login")
login_window.geometry("1000x1000")
login_window.configure(bg=BG_COLOR)

container = tk.Frame(login_window, bg=BG_COLOR)
container.place(relx=0.5, rely=0.5, anchor='center')

tk.Label(container, text="AttendEase", font=HEADER_FONT, fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=20)

def recognize_and_show_attendance():
    cap = cv2.VideoCapture(0)
    messagebox.showinfo("Login", "Press 's' to scan your face.")

    student_name = None
    roll_number = None

    while True:
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Error", "Failed to read from webcam.")
            break

        cv2.imshow("Login Face Scan", frame)
        key = cv2.waitKey(1)

        if key == ord('s'):
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            encodings = face_recognition.face_encodings(rgb)

            if len(encodings) == 0:
                messagebox.showerror("Error", "No face detected.")
                continue

            encoding = encodings[0]
            matches = face_recognition.compare_faces(known_encodings, encoding)
            face_distances = face_recognition.face_distance(known_encodings, encoding)

            if True in matches:
                best_match_index = np.argmin(face_distances)
                student_name = known_names[best_match_index]
                roll_number = roll_numbers[best_match_index]
                break
            else:
                messagebox.showerror("Error", "Face not recognized.")
                break

        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if student_name and roll_number:
        # Mark attendance
        now = datetime.datetime.now()
        today = now.date()
        time_now = now.time()

        try:
            cursor.execute("""
                SELECT * FROM attendance
                WHERE student_name = %s AND roll_number = %s AND date = %s
            """, (student_name, roll_number, today))
            already_marked = cursor.fetchone()

            if not already_marked:
                cursor.execute("""
                    INSERT INTO attendance (student_name, roll_number, date, time)
                    VALUES (%s, %s, %s, %s)
                """, (student_name, roll_number, today, time_now))
                db.commit()

            show_attendance(student_name, roll_number)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to mark attendance: {e}")

def show_attendance(name, roll):
    cursor.execute("SELECT date, time FROM attendance WHERE student_name = %s AND roll_number = %s", (name, roll))
    records = cursor.fetchall()

    attendance_window = tk.Toplevel(login_window)
    attendance_window.title(f"{name}'s Attendance")
    attendance_window.geometry("700x700")
    attendance_window.configure(bg=BG_COLOR)

    tk.Label(attendance_window, text=f"Attendance for {name}", font=FONT, fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=10)

    text_area = scrolledtext.ScrolledText(attendance_window, width=50, height=12)
    text_area.pack(padx=10, pady=10)

    for date, time in records:
        text_area.insert(tk.END, f"{date} - {time}\n")
    text_area.config(state='disabled')

    total_days_label = tk.Label(attendance_window, text="", font=FONT, fg=TEXT_COLOR, bg=BG_COLOR)
    total_days_label.pack(pady=5)

    percentage_label = tk.Label(attendance_window, text="", font=FONT, fg=TEXT_COLOR, bg=BG_COLOR)
    percentage_label.pack(pady=5)

    def show_total_days():
        total = len(records)
        total_days_label.config(text=f"Total Days Present: {total}")

    def show_attendance_percentage():
        cursor.execute("SELECT COUNT(DISTINCT date) FROM attendance")
        result = cursor.fetchone()
        total_days = result[0] if result else 1
        present_days = len(records)
        percentage = (present_days / total_days) * 100
        percentage_label.config(
            text=f"Attendance Percentage: {percentage:.2f}%"
        )

    def make_label_button(text, command):
        label = tk.Label(
            attendance_window,
            text=text,
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR,
            font=FONT,
            padx=10,
            pady=5,
            cursor="hand2"
        )
        label.pack(pady=5)
        label.bind("<Button-1>", lambda e: command())

    make_label_button("View Total Days Present", show_total_days)
    make_label_button("View Attendance Percentage", show_attendance_percentage)


login_label = tk.Label(
    container,
    text="Login with Face",
    bg=BUTTON_COLOR,
    fg=TEXT_COLOR,
    font=("Trebuchet MS", 18, "bold"),
    padx=25,
    pady=10,
    cursor="hand2"
)
login_label.pack(pady=40)
login_label.bind("<Button-1>", lambda e: recognize_and_show_attendance())

login_window.mainloop()
