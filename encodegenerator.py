import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage


cred = credentials.Certificate("service.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendence-ac24e-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendence-ac24e.appspot.com"
})


# Importing student images
folderPath = 'images'
pathList = os.listdir(folderPath)
# print(pathList)

imgList = []
studentIds = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])
    # print(path)
    # print(os.path.splitext(path)[0])

    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

print(studentIds)

def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        # this we have converted from bgr to rgb because face recognition uses this format
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # this is the format when we have used 0 after the image to get the first element
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

print("Encoding Started ...")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, studentIds]
print("Encoding Complete")

file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("File Saved")