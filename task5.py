import face_recognition
import cv2
import numpy as np


def load_face_encoding(image_path):
    
    image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(image)
    return encodings[0] if encodings else None


def detect_and_recognize_faces(target_image_path, known_encoding, known_label="Known Person"):

    image = face_recognition.load_image_file(target_image_path)
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)

    for location, encoding in zip(face_locations, face_encodings):
        top, right, bottom, left = location

    
        is_match = face_recognition.compare_faces([known_encoding], encoding)[0]
        label = known_label if is_match else "Unknown"

        
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(image, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    return image


def main():
    known_face_path = "known.jpeg"
    test_image_path = "unknown-group.avif"

    known_encoding = load_face_encoding(known_face_path)

    if known_encoding is None:
        print("No face found in known image.")
        return

    result_image = detect_and_recognize_faces(test_image_path, known_encoding)

    # Convert color space for OpenCV display
    result_bgr = cv2.cvtColor(result_image, cv2.COLOR_RGB2BGR)

    cv2.imshow("Face Recognition Result", result_bgr)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
