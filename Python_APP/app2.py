import cv2  # Import OpenCV library for computer vision tasks
import dlib  # Import dlib library for face detection
from PIL import Image  # Import Image module from PIL for image processing

# Function to detect and crop the face from a given frame
def detect_and_crop_face(frame):
    # Convert the frame to grayscale
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the grayscale frame using the face detector
    faces = face_detector(frame_gray)
    
    # Check if any faces are detected
    if faces:
        # Get the bounding box of the first detected face
        face_bb = faces[0]
        # Crop the face from the original frame using the bounding box
        face_img = frame[face_bb.top():face_bb.bottom(), face_bb.left():face_bb.right()]
        return face_img  # Return the cropped face image
    else:
        return None  # Return None if no faces are detected

# Function to convert a frame to ASCII art
def frame_to_ascii(frame, output_width=100):
    # Calculate the aspect ratio of the frame
    aspect_ratio = frame.shape[0] / frame.shape[1]
    # Calculate the output height based on the output width and aspect ratio
    output_height = int(output_width * aspect_ratio)
    # Resize the frame to the specified output width and height
    frame = cv2.resize(frame, (output_width, output_height))
    # Convert the resized frame to grayscale
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Define the ASCII characters to represent pixel intensity
    ascii_chars = "@%#*+=-:. "
    # Calculate the intensity range for mapping pixel values to ASCII characters
    intensity_range = 255 / (len(ascii_chars) - 1)
    
    # Initialize an empty string to store the ASCII art
    ascii_art = ""
    
    # Iterate over each pixel in the frame
    for y in range(output_height):
        for x in range(output_width):
            # Get the pixel value at the current position
            pixel_value = frame_gray[y, x]
            # Calculate the index of the ASCII character based on pixel intensity
            ascii_index = int(pixel_value / intensity_range)
            # Get the corresponding ASCII character
            ascii_char = ascii_chars[ascii_index]
            # Replace '*' with ' ' for better visualization
            if ascii_char == '*':
                ascii_char = ' '
            # Append the ASCII character to the ASCII art string
            ascii_art += ascii_char
        ascii_art += '\n'  # Add a newline character at the end of each row
    
    return ascii_art  # Return the generated ASCII art

# Initialize the face detector using dlib
face_detector = dlib.get_frontal_face_detector()

# Initialize the webcam capture
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Set the frame width to 640 pixels
cap.set(4, 480)  # Set the frame height to 480 pixels

# Main loop to capture frames from the webcam and perform face detection
while True:
    # Read a frame from the webcam
    ret, frame = cap.read()
    
    # Detect and crop the face from the frame
    face_img = detect_and_crop_face(frame)
    
    # Check if a face is detected
    if face_img is not None:
        # Convert the cropped face to ASCII art
        ascii_result = frame_to_ascii(face_img, output_width=100)
        print(ascii_result)  # Print the generated ASCII art
    
    # Display the original frame with the detected face
    cv2.imshow('Original Frame', frame)
    
    # Check for key presses (to exit the loop)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break  # Break the loop if 'q' key is pressed

# Release the webcam capture
cap.release()

# Close all OpenCV windows
cv2.destroyAllWindows()
