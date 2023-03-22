# to be running in raspberry pi

import cv2
import requests
import threading

frame_delimeter = 20
counter = 0


BACKEND_SERVER_ENDPOINT = "http://127.0.0.1:5000"


def capture_frames(video_source, frame_rate):
    global counter
    capture = cv2.VideoCapture(video_source)

    # Check if the video source is opened
    if not capture.isOpened():
        print("Unable to open the video source")
        return

    # Read the first frame
    _, frame = capture.read()

    # cv2.imshow('frame', frame) # add only if you want to see a live camera feed.

    # Set the delay based on the frame rate
    delay = int(1000 / frame_rate)

    while True:
        # Read frames
        _, frame = capture.read()

        if frame is None:
            print("Error in reading frame correctly")
            break

        # Increment the counter
        counter += 1

        # Save every 20th frame to file
        if counter % frame_delimeter == 0:
            _, img_encoded = cv2.imencode('.jpg', frame)

            cv2.imshow('frame', frame)
            response = requests.post(f'{BACKEND_SERVER_ENDPOINT}/process',
                                     files={'image': ('image.jpg', img_encoded.tobytes())})
            print('Response:', response.status_code, response.content)

        # quit if the key "q" is pressed
        if cv2.waitKey(delay) & 0xFF == ord("q"):
            break
    # Release the video capture object
    capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    video_source = 0
    frame_rate = 30

    # Create and start the thread to capture frames from the camera
    threading.Thread(target=capture_frames, args=(
        video_source, frame_rate)).start()
