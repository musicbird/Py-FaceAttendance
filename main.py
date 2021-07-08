import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

path = 'ImagesAttendance'
images = []
classNames = []
myList = os.listdir(path) #     i i        ,                      ]]]]]]]]]]
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0]) #   'Bill Gates' instead of 'Bill Gates.jpg'
print(classNames)  # Output ['Bill Gates', 'Elon Musk', 'Jack Ma']
# Customize a function that finds the image encoding in Images, returns a list of encoding with each image
def findEncodings(images):
    encodeList =[] # Initialize image coding empty list
    for img in images:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

# Customize a function that records attendance names and time, when an individual appears, then recorded in the CSV file in the form of Name, TIME
def markAttendance(name):
    with open('Attendance.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',') #entry=['name','time']
            #print(entry[0])
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString =now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')
encodeListKnown = findEncodings(images)
#Print (Len (encodelistknown) # has three encoding 3

print('Encoding Complete')
# Capture photos from the lens
cap = cv2.VideoCapture(0)

while True:
    success,img =cap.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS) # Get the face coordinates of the current frame
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame) # Get the code under the picture coordinates

    for encodeFace , faceLoc in zip(encodesCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
       #print (facedis) display matching value
        matchIndex = np.argmin(faceDis) #matchindex is the smallest subscript of Facedis, which is the coordinate of the most matching picture.

        # If the captured and the picture are matched, the output of the matching picture is output.
        if matches[matchIndex]:# < 0.50:
            name =classNames[matchIndex].upper()
        else: name = 'Unknown'
        print(name)
        y1,x2,y2,x1 =faceLoc
        y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4  ## The face coordinates have been reduced by 4 times, and now it is coming back.
        cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
        cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
        cv2.putText(img, 'press q to exit' , (30,200), cv2.FONT_HERSHEY_COMPLEX, 0.7, (99,99,99),2)
        cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
        markAttendance(name)
    cv2.imshow('Wecam',img)
    #This breaks on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

VideoCapture.release()
cv2.destroyAllWindows()




# I am not sure that you are writing your file name correctly. I've never seen a file 
# directory like 'car video.mp4'. When you are using the zero based index your webcam and 
# cv2.VideoCapture works fine; however VideoCapture cannot read a file like 'car(space)video.mp4' 
# A working code is something like this;

# import numpy as np
# import cv2

# cap = cv2.VideoCapture('video.mp4')

# while(cap.isOpened()):

#     ret, frame = cap.read()

#     if ret==True:

#         cv2.imshow('frame',frame)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#     else:
#         break

# # Release everything if job is finished
# cap.release()
# cv2.destroyAllWindows()
