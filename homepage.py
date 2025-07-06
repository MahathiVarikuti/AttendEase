import tkinter as tk
import subprocess

BG_COLOR = "#fffdf5"
TEXT_COLOR = "#364c84"
BUTTON_BG = "#e7f1a8"
FONT = ("Trebuchet MS", 20, "bold")

def open_register():
    subprocess.Popen(["python", "reg_gui.py"])

def open_login():
    subprocess.Popen(["python", "login.py"])

def open_attendance():
    subprocess.Popen(["python", "AttendanceProject.py"])

window = tk.Tk()
window.title("AttendEase - Home")
window.geometry("1000x700")
window.configure(bg=BG_COLOR)

tk.Label(window, text="Welcome to AttendEase", font=("Trebuchet MS", 34, "bold"),
         fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=50)

container = tk.Frame(window, bg=BG_COLOR)
container.place(relx=0.5, rely=0.5, anchor='center')

def make_button(text, cmd, row):
    btn = tk.Label(container, text=text, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT, padx=40, pady=15, cursor="hand2")
    btn.grid(row=row, column=0, pady=20)
    btn.bind("<Button-1>", lambda e: cmd())

make_button("Register New Student", open_register, 0)
make_button("Login & View Attendance", open_login, 1)
make_button("Mark Real-Time Attendance", open_attendance, 2)

window.mainloop()
