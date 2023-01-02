import cv2
import threading

# Define the video source for device 1
video_source_1 = "http://192.168.45.45:8080/video"

# Define the video source for device 2
video_source_2 = "http://192.168.45.45:8080/video"

# Define the frame rate for both devices
frame_rate_1 = 30
frame_rate_2 = 30

# Initialize the variables for saving frames
counter = 0

# Define the function to save frames from both devices
def save_frames(video_source, frame_rate):
  global counter

  # Create a VideoCapture object
  cap = cv2.VideoCapture(video_source)

  # Check if the video source is opened
  if not cap.isOpened():
    print("Unable to open the video source")
    return

  # Read the first frame
  _, frame = cap.read()

  # Set the delay based on the frame rate
  delay = int(1000 / frame_rate)

  while True:
    # Read a new frame
    _, frame = cap.read()

    # Check if the frame was correctly read
    if frame is None:
      break

    # Increment the counter
    counter += 1

    # Save every 20th frame
    if counter % 20 == 0:
      # Save the frame to the "images" folder
      cv2.imwrite("images/frame_{}.jpg".format(counter), frame)

    # Check if the user pressed "q"
    if cv2.waitKey(delay) & 0xFF == ord("q"):
      break

# Create and start the threads
thread1 = threading.Thread(target=save_frames, args=(video_source_1, frame_rate_1))
thread2 = threading.Thread(target=save_frames, args=(video_source_2, frame_rate_2))
thread1.start()
thread2.start()

