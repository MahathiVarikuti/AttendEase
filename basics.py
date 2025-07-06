import numpy as np
import cv2
import face_recognition

imgSara1 = face_recognition.load_image_file('/Users/aradhanasingh/PycharmProjects/FaceRecognition/ImagesBasic/sara1.jpg')
imgSara1 = cv2.cvtColor(imgSara1, cv2.COLOR_BGR2RGB)

imgSara2 = face_recognition.load_image_file('/Users/aradhanasingh/PycharmProjects/FaceRecognition/ImagesBasic/sara2.jpg')
imgSara2 = cv2.cvtColor(imgSara2, cv2.COLOR_BGR2RGB)

faceLoc=face_recognition.face_locations(imgSara1)[0]
encodeSara1=face_recognition.face_encodings(imgSara1)[0]
cv2.rectangle(imgSara1, (faceLoc[3],faceLoc[0]), (faceLoc[1],faceLoc[2]), (255,0,255), 2)

faceLocTest=face_recognition.face_locations(imgSara2)[0]
encodeSara2Test=face_recognition.face_encodings(imgSara2)[0]
cv2.rectangle(imgSara2, (faceLocTest[3],faceLocTest[0]), (faceLocTest[1],faceLocTest[2]), (255,0,255), 2)

results=face_recognition.compare_faces([encodeSara1], encodeSara2Test)
faceDis=face_recognition.face_distance([encodeSara1], encodeSara2Test)
print(results,faceDis)

#print result on img and round off to 2 dec places
# Font, Scale, Color (BGR), Thickness
cv2.putText(imgSara2, f'{results}, {round(faceDis[0], 2)}', (40,40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

cv2.imshow('Sara One', imgSara1)
cv2.imshow('Sara Two', imgSara2)
cv2.waitKey(0)

