from ImageSender import ImageSender
import face_recognition
import cv2
import numpy as np
import base64


TARCISIO_JPG = "imgs/tar.jpg"
FRANCA_JPG = "imgs/fran.jpg"
WAGNER_JPG = "imgs/wag.jpeg"

def load_encodings():
    def encoding_from_jpg(jpg):
        image = face_recognition.load_image_file(jpg)
        return face_recognition.face_encodings(image)[0]

    known_face_encodings = [
        encoding_from_jpg(TARCISIO_JPG),
        encoding_from_jpg(FRANCA_JPG),
        encoding_from_jpg(WAGNER_JPG)
    ]
    known_face_names = [
        "Tarcísio",
        "França",
        "Wagner"
    ]

    return (known_face_encodings, known_face_names)


def run_video_capture(known_face_encodings, known_face_names):
    video_capture = cv2.VideoCapture(0)
    
    sender = ImageSender("http://192.168.15.9:5003/api/ImageStore/Store")
    
    face_locations = []
    face_encodings = []
    face_names = []

    process_this_frame = True

    while True:
        ret, frame = video_capture.read()

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame
        if face_names:
            try:
                retval, buffer = cv2.imencode('.jpg', frame)
                jpg_as_text = base64.b64encode(buffer).decode('ascii')
                sender.send(jpg_as_text, face_names)
            except Exception as e:
                print(e)

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    
    encodings, face_names = load_encodings()

    run_video_capture(encodings, face_names)
    