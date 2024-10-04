from flask import Flask, render_template, request, jsonify
import subprocess
import os

app = Flask(__name__)

# Directory to store known faces
#known_faces_dir = "/Users/madanreddy/Desktop/frw/known_faces"

# Directory to store unknown faces
unknown_faces_dir = "/Users/madanreddy/Desktop/frw/static/unknown_faces"

# Define routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/datascript', methods=['POST'])
def run_face_recognition_script():
    try:
        # Get username and user ID from the form
        username = request.form.get('username')
        user_id = request.form.get('user_id')
        print(user_id,"\n",username)
        # Run the face recognition script using subprocess
        subprocess.run(['python', 'dataset_capture.py', username, user_id])
        
        return 'Script executed successfully', 200
    except Exception as e:
        return str(e), 500

@app.route('/test', methods=['POST'])
def test():
    try:
        subprocess.run(["python","face_recog.py"])
        return 'executed successfully...', 200
    except Exception as e:
        return str(e), 500
    
#page to display unknown persons

# @app.route('/unknown_persons', methods=['POST'])
# def unknown_persons_img():
#     try:
#         # Get paths of unknown images
#         unknown_images = []
#         for filename in os.listdir(unknown_faces_dir):
#             if filename.endswith('.jpg') or filename.endswith('.png'):
#                 image_path = os.path.join(unknown_faces_dir, filename)
#                 unknown_images.append(image_path)
        
#         return render_template('unknown_images.html', unknown_images=unknown_images), 200
#     except Exception as e:
#         return str(e), 500


@app.route('/unknown_persons', methods=['POST'])
def unknown_persons_img():
    try:
        # Get paths of unknown images relative to the static directory
        unknown_images = []
        for filename in os.listdir(unknown_faces_dir):
            if filename.endswith('.jpg') or filename.endswith('.png'):
                image_path = os.path.join('unknown_faces', filename)  # Relative path
                unknown_images.append(image_path)
        
        return render_template('unknown_images.html', unknown_images=unknown_images), 200
    except Exception as e:
        return str(e), 500



if __name__ == '__main__':
    app.run(debug=True)



## below code is flask web framework to display the unknown image in web page 

# import cv2
# import os
# import face_recognition
# import numpy as np
# import datetime
# from flask import Flask, render_template, Response
# from PIL import Image

# app = Flask(__name__)

# # Directory to store known faces
# known_faces_dir = "/Users/madanreddy/Desktop/frw/known_faces"

# # Directory to store unknown faces
# unknown_faces_dir = "/Users/madanreddy/Desktop/frw/unknown_faces"

# # Function to load known faces
# def load_known_faces(known_faces_dir):
#     known_face_encodings = []
#     known_face_names = []

#     # Load known faces
#     for filename in os.listdir(known_faces_dir):
#         if filename.endswith('.jpg') or filename.endswith('.png'):
#             image_path = os.path.join(known_faces_dir, filename)
#             image = face_recognition.load_image_file(image_path)
#             face_encoding = face_recognition.face_encodings(image)

#             # Ensure that at least one face is found and encoded
#             if len(face_encoding) > 0:
#                 known_face_encodings.append(face_encoding[0])
#                 known_face_names.append(os.path.splitext(filename)[0])
#             else:
#                 print("No face found in:", filename)

#     return known_face_encodings, known_face_names

# # Function to calculate Euclidean distance between two vectors
# def euclidean_distance(vector1, vector2):
#     return np.linalg.norm(vector1 - vector2)

# # Load known faces
# known_face_encodings, known_face_names = load_known_faces(known_faces_dir)

# # Initialize the webcam with custom resolution
# cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1500)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1000)

# # List to store captured unknown face encodings
# captured_unknown_face_encodings = []

# def generate_frames():
#     while True:
#         ret, frame = cap.read()

#         # Find all face locations and encodings in the current frame
#         face_locations = face_recognition.face_locations(frame)
#         face_encodings = face_recognition.face_encodings(frame, face_locations)

#         # Iterate through each face found in the frame
#         for face_location, face_encoding in zip(face_locations, face_encodings):
#             top, right, bottom, left = face_location  # Extract face coordinates

#             # Check if the face matches any known face
#             matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)

#             # If unknown face is detected and it's not already captured, save it
#             if not True in matches:
#                 is_duplicate = False
#                 for known_encoding in captured_unknown_face_encodings:
#                     distance = euclidean_distance(face_encoding, known_encoding)
#                     if distance < 0.6:  # Adjust the threshold as needed
#                         is_duplicate = True
#                         break
#                 if not is_duplicate:
#                     captured_unknown_face_encodings.append(face_encoding)
#                     face_image = frame[top:bottom, left:right]  # Crop the face from the frame
#                     # Append timestamp to the filename
#                     timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#                     image_path = os.path.join(unknown_faces_dir, f"unknown_{len(captured_unknown_face_encodings)}_{timestamp}.jpg")
#                     cv2.imwrite(image_path, face_image)
#                     print("Unknown face saved as:", image_path)

#                     yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', face_image)[1].tobytes() + b'\r\n')

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# if __name__ == "__main__":
#     app.run(debug=True)


# #below code is to display  multiple unknown images 

# import cv2
# import os
# import face_recognition
# import numpy as np
# import datetime
# from flask import Flask, render_template, Response
# from PIL import Image

# app = Flask(__name__)

# # Directory to store known faces
# known_faces_dir = "/Users/madanreddy/Desktop/frw/known_faces"

# # Directory to store unknown faces
# unknown_faces_dir = "/Users/madanreddy/Desktop/frw/unknown_faces"

# # Function to load known faces
# def load_known_faces(known_faces_dir):
#     known_face_encodings = []
#     known_face_names = []

#     # Load known faces
#     for filename in os.listdir(known_faces_dir):
#         if filename.endswith('.jpg') or filename.endswith('.png'):
#             image_path = os.path.join(known_faces_dir, filename)
#             image = face_recognition.load_image_file(image_path)
#             face_encoding = face_recognition.face_encodings(image)

#             # Ensure that at least one face is found and encoded
#             if len(face_encoding) > 0:
#                 known_face_encodings.append(face_encoding[0])
#                 known_face_names.append(os.path.splitext(filename)[0])
#             else:
#                 print("No face found in:", filename)

#     return known_face_encodings, known_face_names

# # Function to calculate Euclidean distance between two vectors
# def euclidean_distance(vector1, vector2):
#     return np.linalg.norm(vector1 - vector2)

# # Load known faces
# known_face_encodings, known_face_names = load_known_faces(known_faces_dir)

# # Initialize the webcam with custom resolution
# cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1500)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1000)

# # List to store captured unknown face images
# captured_unknown_faces = []

# def generate_frames():
#     while True:
#         ret, frame = cap.read()

#         # Find all face locations and encodings in the current frame
#         face_locations = face_recognition.face_locations(frame)
#         face_encodings = face_recognition.face_encodings(frame, face_locations)

#         # Iterate through each face found in the frame
#         for face_location, face_encoding in zip(face_locations, face_encodings):
#             top, right, bottom, left = face_location  # Extract face coordinates

#             # Check if the face matches any known face
#             matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)

#             # If unknown face is detected and it's not already captured, save it
#             if not True in matches:
#                 is_duplicate = False
#                 for known_encoding, unknown_face_image in captured_unknown_faces:
#                     distance = euclidean_distance(face_encoding, known_encoding)
#                     if distance < 0.6:  # Adjust the threshold as needed
#                         is_duplicate = True
#                         break
#                 if not is_duplicate:
#                     captured_unknown_faces.append((face_encoding, frame[top:bottom, left:right]))  # Store the face encoding and image

#         # Resize and concatenate unknown face images horizontally
#         unknown_images_resized = [cv2.resize(image, (captured_unknown_faces[0][1].shape[1], captured_unknown_faces[0][1].shape[0])) for _, image in captured_unknown_faces]
#         unknown_images_concatenated = np.concatenate(unknown_images_resized, axis=1) if unknown_images_resized else None

#         # Convert the concatenated image to JPEG format
#         if unknown_images_concatenated is not None:
#             _, jpeg = cv2.imencode('.jpg', unknown_images_concatenated)
#             frame = jpeg.tobytes()

#         yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# @app.route('/')
# def index():
#     return render_template('index1.html')

# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# if __name__ == "__main__":
#     app.run(debug=True)



