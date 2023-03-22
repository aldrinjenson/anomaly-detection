# to be running in main server
from flask import Flask, request
import cv2
import numpy as np
import os

app = Flask(__name__)

counter = 0
frame_delimiter = 20


def save_frame(frame):
    global counter
    counter += 1
    if not os.path.exists("images"):
        os.makedirs("images")
    cv2.imwrite("images/frame_{}.jpg".format(counter), frame)
    print("Writing to file, frame: ", counter)
    return counter


@app.route('/process', methods=['POST'])
def process():
    file = request.files['image']
    npimg = np.fromfile(file, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # isAnomalyFound(frmae)
    # Process the frame and save it if anomalous
    counterVal = save_frame(img)
    return "Saved frame: " + str(counterVal)


if __name__ == '__main__':
    app.run()
