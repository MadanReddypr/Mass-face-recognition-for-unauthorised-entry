# import cv2
# import os
# import sys

# # Directory to store known faces
# known_faces_dir = "/Users/madanreddy/Desktop/frw/known_faces"
# person_name=sys.argv[1]
# id=sys.argv[2]
# print(person_name,id)
# # Create the directory if it doesn't exist
# if not os.path.exists(known_faces_dir):
#     os.makedirs(known_faces_dir)

# # Function to capture and save images
# def capture_images():
#     # Initialize the webcam
#     cap = cv2.VideoCapture(0)
    

#     # Define the number of images to capture
#     num_images_to_capture = 30

#     # Counter for naming the images
#     count = 0

#     while count < num_images_to_capture:
#         # Capture frame-by-frame
#         ret, frame = cap.read()

#         # Display the frame
#         cv2.imshow('Capture Frame', frame)

#         # Wait for 's' key to save the image
#         if cv2.waitKey(500) :
#             # Save the captured image with the user-provided name
#             image_path = os.path.join(known_faces_dir, f"{person_name}_{id}_{count}.jpg")
#             cv2.imwrite(image_path, frame)
#             print("Image saved as:", image_path)
#             count += 1

#         # Adjust the angle slightly after each capture
#         # Example: flip the image horizontally
#         frame = cv2.flip(frame, 1)
#         key = cv2.waitKey(1) & 0xFF
#         # Break the loop if the desired number of images are captured
#         if count >= num_images_to_capture:
#             break
#         elif key == ord('q'):  # Break the loop if 'q' key is pressed
#             break
#     # Release the webcam and close all windows
#     cap.release()
#     cv2.destroyAllWindows()

# # Call the function to capture images
# capture_images()

import cv2
import os
import sys
import face_recognition

# Directory to store known faces
known_faces_dir = "/Users/madanreddy/Desktop/frw/known_faces"
person_name = sys.argv[1]
id = sys.argv[2]
print(person_name, id)

# Create the directory if it doesn't exist
if not os.path.exists(known_faces_dir):
    os.makedirs(known_faces_dir)

# Function to capture and save images
def capture_images():
    # Initialize the webcam
    cap = cv2.VideoCapture(0)

    # Counter for captured images
    images_captured = 0

    while images_captured < 30:
        ret, frame = cap.read()
        if not ret:
            break

        # Find face locations in the frame
        face_locations = face_recognition.face_locations(frame)

        # Draw a rectangle around the detected face(s)
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Display the frame
        cv2.imshow('Capture Frame', frame)

        # Wait for 's' key to save the image
        if cv2.waitKey(500):
            # Save the captured image with the user-provided name
            image_path = os.path.join(known_faces_dir, f"{person_name}_{id}_{images_captured}.jpg")
            cv2.imwrite(image_path, frame)
            print("Image saved as:", image_path)
            images_captured += 1

        # Break the loop if 'q' key is pressed
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    # Release the webcam and close all windows
    cap.release()
    cv2.destroyAllWindows()

# Call the function to capture images
capture_images()
