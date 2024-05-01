import cv2
import dlib
import time

def detect_and_crop_face(frame):
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector(frame_gray)
    if faces:
        face_bb = faces[0]
        face_img = frame[face_bb.top():face_bb.bottom(), face_bb.left():face_bb.right()]
        return face_img
    else:
        return None

def frame_to_ascii(frame, output_width=150):
    aspect_ratio = frame.shape[0] / frame.shape[1]
    output_height = int(output_width * aspect_ratio)
    frame = cv2.resize(frame, (output_width, output_height))
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ascii_chars = "@%#*+=-:. "
    intensity_range = 255 / (len(ascii_chars) - 1)
    ascii_art = ""
    for y in range(output_height):
        for x in range(output_width):
            pixel_value = frame_gray[y, x]
            ascii_index = int(pixel_value / intensity_range)
            ascii_char = ascii_chars[ascii_index]
            if ascii_char == '*':
                ascii_char = ' '
            ascii_art += ascii_char
        ascii_art += '\n'
    return ascii_art

face_detector = dlib.get_frontal_face_detector()
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
time.sleep(5)
ret, frame = cap.read()
face_img = detect_and_crop_face(frame)
if face_img is not None:
    ascii_result = frame_to_ascii(face_img, output_width=150)
    print(ascii_result)

cap.release()
cv2.destroyAllWindows()
