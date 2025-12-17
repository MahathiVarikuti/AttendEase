# AttendEase

**A Facial Recognition Based Attendance Management System**

The current attendance systems in educational institutions are often prone to inaccuracies due to manual errors, delays, or proxy attendance. **AttendEase** solves this problem by using computer vision to recognize students' faces and instantly mark their attendance in a secure SQL database.

---

## Features

* **Automatic Face Detection & Recognition**
  Uses real-time webcam input to detect and recognize student faces.

* **Instant Attendance Marking**
  Automatically records the student’s name, roll number, date, and time upon successful recognition.

* **Live Dashboard (GUI)**
  A centralized graphical interface to manage student registration, attendance, and login modes.

* **Student Registration**
  Captures student details and facial embeddings, compresses them using `zlib`, and securely stores them in the database.

* **Student Login & Attendance Stats**
  Allows students to log in using face recognition to view their attendance history and attendance percentage.

---

## Tech Stack

* **Programming Language:** Python 3.x
* **Computer Vision:** OpenCV (`cv2`), `face_recognition`, `dlib`
* **GUI Framework:** Tkinter
* **Database:** MySQL (`mysql-connector-python`)
* **Data Handling:** NumPy, Pickle, Zlib
* **Configuration Management:** `python-dotenv`

---

## Installation & Setup

### 1. Prerequisites

* Python installed on your system
* MySQL Server (local or remote)
* **CMake** (required to compile the `dlib` dependency)

---

### 2. Install Dependencies

Install all required libraries using the following commands:

```bash
pip install -r requirements.txt
pip install python-dotenv
```

---

### 3. Database Configuration

The system requires a MySQL database. You must create the database and tables before running the application.

1. Open your MySQL client.
2. Create a database (example: `attendance_db`).
3. Run the following SQL commands:

```sql
CREATE TABLE student (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    roll_number VARCHAR(50),
    reg_number VARCHAR(50),
    section VARCHAR(10),
    major VARCHAR(50),
    starting_year INT,
    current_year INT,
    gpa FLOAT,
    face_encoding LONGBLOB
);

CREATE TABLE attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(100),
    roll_number VARCHAR(50),
    date DATE,
    time TIME
);
```

---

### 4. Environment Variables

Create a file named `.env` in the root directory of the project and add your database credentials:

```env
DB_HOST=localhost
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=attendance_db
```

---

## How to Run

### Start the Application

Run the homepage script to launch the main dashboard:

```bash
python homepage.py
```

---

### Using the Dashboard

* **Register New Student**
  Opens the registration form. Fill in the student details and press **`s`** to capture the face encoding or **`q`** to quit.

* **Mark Real-Time Attendance**
  Starts the webcam. The system detects known faces and automatically logs attendance in the database.

* **Login & View Attendance**
  Students can scan their face to view their personal attendance report and attendance percentage.

---

## Future Improvements

* Email or SMS notifications for absentee alerts
* Support for multi-class and multi-faculty attendance handling
* Cloud backup and analytics dashboard integration

---

## 📌 Note

This project is intended for academic and educational purposes and demonstrates the use of computer vision in real-world applications.
