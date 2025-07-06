import tkinter as tk
from tkinter import messagebox
import mysql.connector
import cv2
import face_recognition
import pickle
import zlib
import os
from dotenv import load_dotenv


BG_COLOR = "#fffdf5"
TEXT_COLOR = "#364c84"
ENTRY_BG = "#e7f1a8"
BUTTON_BG = "#95b1ee"

load_dotenv()

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)


cursor = db.cursor()

window = tk.Tk()
window.title("Student Registration")
window.geometry("1000x700")
window.configure(bg=BG_COLOR)

tk.Label(
    window,
    text="Welcome to AttendEase",
    font=("Trebuchet MS", 34, "bold"),
    fg=TEXT_COLOR,
    bg=BG_COLOR
).pack(pady=30)

container = tk.Frame(window, bg=BG_COLOR)
container.place(relx=0.5, rely=0.5, anchor='center')

fields = {
    "First Name": tk.StringVar(),
    "Last Name": tk.StringVar(),
    "Roll Number": tk.StringVar(),
    "Registration Number": tk.StringVar(),
    "Section": tk.StringVar(),
    "Major": tk.StringVar(),
    "Starting Year": tk.StringVar(),
    "Current Year": tk.StringVar(),
    "GPA": tk.StringVar()
}

font_style = ("Trebuchet MS", 20)
row = 0

for label, var in fields.items():
    tk.Label(container, text=label, font=font_style, fg=TEXT_COLOR, bg=BG_COLOR)\
        .grid(row=row, column=0, pady=10, padx=10, sticky='e')

    entry = tk.Entry(
        container,
        textvariable=var,
        font=font_style,
        bg=ENTRY_BG,
        fg=TEXT_COLOR,
        insertbackground="#00008B",
        highlightthickness=0,
        bd=0,
        relief='flat'
    )
    entry.grid(row=row, column=1, pady=10, padx=10, ipady=6, ipadx=8)
    row += 1

def register():
    values = {label: var.get() for label, var in fields.items()}
    if not values["First Name"] or not values["Roll Number"]:
        messagebox.showerror("Error", "First Name and Roll Number are required.")
        return

    cap = cv2.VideoCapture(0)
    messagebox.showinfo("Capture", "Press 's' to capture face, 'q' to quit without saving.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Capture Face", frame)
        key = cv2.waitKey(1)

        if key == ord('s'):
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            encodings = face_recognition.face_encodings(rgb)

            if not encodings:
                messagebox.showerror("Error", "No face found!")
                continue

            compressed_encoding = zlib.compress(pickle.dumps(encodings[0]))

            try:
                cursor.execute("""
                    INSERT INTO student (first_name, last_name, roll_number, reg_number, section, major,
                                         starting_year, current_year, gpa, face_encoding)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    values["First Name"],
                    values["Last Name"],
                    values["Roll Number"],
                    values["Registration Number"],
                    values["Section"],
                    values["Major"],
                    int(values["Starting Year"]),
                    int(values["Current Year"]),
                    float(values["GPA"]),
                    compressed_encoding
                ))
                db.commit()
                messagebox.showinfo("Success", "Student registered successfully!")
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", str(err))
            break

        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

register_btn = tk.Label(
    container,
    text="Register",
    bg=BUTTON_BG,
    fg=TEXT_COLOR,
    font=("Trebuchet MS", 20, "bold"),
    padx=25,
    pady=10,
    cursor="hand2"
)
register_btn.grid(row=row, column=0, columnspan=2, pady=30)
register_btn.bind("<Button-1>", lambda e: register())

window.mainloop()
