import mysql.connector
import pickle
import zlib
import numpy as np

known_encodings = []
known_names = []
known_rolls = []

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

cursor = conn.cursor()

cursor.execute("SELECT first_name, roll_number, face_encoding FROM student")
data = cursor.fetchall()

for name, roll, enc_blob in data:
    try:

        encoding = pickle.loads(zlib.decompress(enc_blob))

        known_encodings.append(encoding)
        known_names.append(name)
        known_rolls.append(roll)

        print(f"\nStudent: {name} ({roll})")
        print("Face Encoding (first 5 values):")
        print(np.round(encoding[:5], 4))
        print("Encoding length:", len(encoding))

    except Exception as e:
        print(f"error decoding face for {name}: {e}")

cursor.close()
conn.close()

print("\n loaded all encodings from student ")
