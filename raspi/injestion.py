import os
import sys
import threading
import cv2
import requests
from dotenv import load_dotenv

load_dotenv()

FRAME_BATCH_SIZE = 20  # Number of frames to send in each batch
counter = 0
camera_id = 0
frame_buffer = []  # Buffer to store frames before sending them

BACKEND_SERVER_ENDPOINT = os.getenv("BACKEND_SERVER_ENDPOINT")

def capture_frames(video_source, frame_rate):
    global counter, frame_buffer
    capture = cv2.VideoCapture(video_source)

    # Check if the video source is opened
    if not capture.isOpened():
        print("Unable to open the video source")
        return

    # Read the first frame
    _, frame = capture.read()

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

        # Save the frame to the buffer
        frame_buffer.append(frame)

        # Send the frames in batches of FRAME_BATCH_SIZE
        if counter % FRAME_BATCH_SIZE == 0:
            print('inside')
            frames_to_send = frame_buffer
            frame_buffer = []  # Clear the buffer

            # Create an array of image data from the frames
            images = [cv2.imencode('.jpg', frame)[1].tobytes() for frame in frames_to_send]

            # Send the frames as an array to the endpoint
            response = requests.post(
                f'{BACKEND_SERVER_ENDPOINT}/processfiles',
                data={'cameraId': camera_id, 'images':images},
            )

            print('Response:', response.status_code, response.content)

        # Quit if the key "q" is pressed
        if cv2.waitKey(delay) & 0xFF == ord("q"):
            break

    # Release the video capture object
    capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    frame_rate = 30
    default_video_source = 0

    print(sys.argv)
    if len(sys.argv) > 2:
        # video_source = int(sys.argv[1])
        video_source = sys.argv[1]
        camera_id = sys.argv[2]
    else:
        video_source = 0
        camera_id = 0
    print(video_source)

    # Create and start the thread to capture frames from the camera
    threading.Thread(target=capture_frames, args=(
        video_source, frame_rate)).start()
