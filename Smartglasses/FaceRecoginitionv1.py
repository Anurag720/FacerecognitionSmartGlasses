# -*- coding: utf-8 -*-
import face_recognition
import cv2
import numpy as np
import pyttsx3
import time
from Bluetin_Echo import Echo

TRIGGER_PIN = 27
ECHO_PIN = 22
speed_of_sound = 315
echo = Echo(TRIGGER_PIN, ECHO_PIN, speed_of_sound)
video_capture = cv2.VideoCapture(0)
#list of known family members for 
# Family member 1
ashwini_image = face_recognition.load_image_file("F:\Smartglasses\WhatsApp Image 2023-01-18 at 9.38.55 PM.jpeg")
ashwini_face_encoding = face_recognition.face_encodings(ashwini_image)[0]
vishal_image = face_recognition.load_image_file("F:\Smartglasses\WhatsApp Image 2023-01-18 at 4.51.27 PM.jpeg")
vishal_face_encoding = face_recognition.face_encodings(vishal_image)[0]


#Family member 2

# Create arrays of known face encodings and their names
known_face_encodings = [
    ashwini_face_encoding,
    vishal_face_encoding
    
]
known_face_names = [
    "Ashwini kumar sinha",
    "vishal smarty"
    
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    result = echo.read()
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            
            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index] and result < 15.0  :
                name = known_face_names[best_match_index]
                #espeak.synth("Hey I Can Identify your face")
                #espeak.synth("Your name is")
                #espeak.synth(name)
                #espeak.set_voice("whisper")
                #espeak.set_voice("f5")
                #espeak.synth("कोई नजदीक आ रहा है ")
                engine = pyttsx3.init()
                engine.say("kooi passs aa raha hai")
                face_names.append(name)
                engine.say(name)
                engine.runAndWait()
                time.sleep(2)
                #you can change the voice and language from here 
                

            face_names.append(name)
            
    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
