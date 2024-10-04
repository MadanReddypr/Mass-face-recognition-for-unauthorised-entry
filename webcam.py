import cv2
import os
import face_recognition
import numpy as np
import datetime

# Directory to store known faces
known_faces_dir = "/Users/madanreddy/Desktop/frw/known_faces"

# Directory to store unknown faces
unknown_faces_dir = "/Users/madanreddy/Desktop/frw/unknown_faces"

# Function to load known faces
def load_known_faces(known_faces_dir):
    known_face_encodings = []
    known_face_names = []

    # Load known faces
    for filename in os.listdir(known_faces_dir):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            image_path = os.path.join(known_faces_dir, filename)
            image = face_recognition.load_image_file(image_path)
            face_encoding = face_recognition.face_encodings(image)

            # Ensure that at least one face is found and encoded
            if len(face_encoding) > 0:
                known_face_encodings.append(face_encoding[0])
                known_face_names.append(os.path.splitext(filename)[0])
            else:
                print("No face found in:", filename)

    return known_face_encodings, known_face_names

# Function to calculate Euclidean distance between two vectors
def euclidean_distance(vector1, vector2):
    return np.linalg.norm(vector1 - vector2)

# Load known faces
known_face_encodings, known_face_names = load_known_faces(known_faces_dir)

# Initialize the webcam with custom resolution
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1500)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1000)

# List to store captured unknown face encodings
captured_unknown_face_encodings = []

while True:
    ret, frame = cap.read()

    # Find all face locations and encodings in the current frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    # Iterate through each face found in the frame
    for face_location, face_encoding in zip(face_locations, face_encodings):
        # Draw a rectangle around the face
        top, right, bottom, left = face_location
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Check if the face matches any known face
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)

        # If known face is detected, display the name
        if True in matches:
            match_index = matches.index(True)
            name = known_face_names[match_index]
        else:
            name = "Unknown"
            
            # If unknown face is detected and it's not already captured, save it
            is_duplicate = False
            for known_encoding in captured_unknown_face_encodings:
                distance = euclidean_distance(face_encoding, known_encoding)
                if distance < 0.6:  # Adjust the threshold as needed
                    is_duplicate = True
                    break
            if not is_duplicate:
                captured_unknown_face_encodings.append(face_encoding)
                face_image = frame[top:bottom, left:right]
                # Append timestamp to the filename
                timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                image_path = os.path.join(unknown_faces_dir, f"unknown_{len(captured_unknown_face_encodings)}_{timestamp}.jpg")
                cv2.imwrite(image_path, face_image)
                print("Unknown face saved as:", image_path)

        # Display the name
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    # Display the frame
    cv2.imshow('Capture Frame', frame)
  

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
