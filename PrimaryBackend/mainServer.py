# to be running in main server
from dotenv import load_dotenv
from flask import Flask, request
import cv2
import numpy as np
import os
import supabase
# from classifier import image_classifier
from anomaly_detector import evaluate

load_dotenv()
app = Flask(__name__)

counter = 0
frame_delimiter = 5

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase_client = supabase.create_client(supabase_url, supabase_key)


def insertCameraToDb():
    new_camera = {
        "coordinates": {
            "lat": 37.7749,
            "lng": -122.4194
        },
        "frame_rate": 30,
        "camera_description": "Camera at MEC"
    }

    insert_result = supabase_client.table(
        "cameras").insert(new_camera).execute()

    if insert_result:
        print("New row was inserted successfully!")
    else:
        print("Failed to insert new row: " + insert_result["error"]["message"])



def classifyAndLogAnomalyToDb(anomalyFrame, cameraId):
#     anomalyClass = image_classifier(anomalyFrame)
    anomalyClass = "Fire Hazard"
    newAnomaly = {
        "class": "Fire Hazard",
        "camera_id": 8,
        "latitude": 10.0431,
        "longitude": 76.3244,
        "anomaly_id": 5
    }
    insert_result = supabase_client.table(
        "alerts").insert(newAnomaly).execute()
    print(insert_result)

    if insert_result:
        print("New row was inserted successfully!")
    else:
        print("Failed to insert new row: " + insert_result["error"]["message"])


# classifyAndLogAnomalyToDb()
# insertCameraToDb()


def save_frame(camera_id, frame):
    global counter
    counter += 1
    if not os.path.exists("images"):
        os.makedirs("images")
    cv2.imwrite("images/frame{}_{}.jpg".format(camera_id, counter), frame)
    print("Writing to file, frame: ", counter)
    return counter


def checkForAnomaly(files):
    # call evaluate with frame
    print('going to evaluate')
    anomalyFrame = evaluate(files)
    print("anomalyframe = ", anomalyFrame)

    anomalyFrame = None
    return anomalyFrame


@app.route('/')
def index():
    return "Anomaly detection server - alive and kicking 🤟"


@app.route('/test')
def test():
    return "Yes, working fine"

@app.route('/processfiles', methods=['POST'])
def processfiles():
    camera_id = request.form.get('cameraId')
    images = request.form.getlist('images')
    files = list(images)
    # sorted_files = sorted(files, key=lambda file: file.filename)


    anomaly = checkForAnomaly(files)
    # if anomaly:
    #     print(anomaly)
        # classifyAndLogAnomalyToDb(anomaly, camera_id)
    # counterVal = save_frame(camera_id, img)
    # return "Saved frame: " + str(counterVal)
    return 'done bro'

@app.route('/process', methods=['POST'])
def process():
    camera_id = request.form.get('cameraId')
    print(camera_id)
    file = request.files['image']
    npimg = np.fromfile(file, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    anomalyFrame = checkForAnomaly(frame)
    if anomaly:
        classifyAndLogAnomalyToDb(anomalyFrame, camera_id)
    counterVal = save_frame(camera_id, img)
    return "Saved frame: " + str(counterVal)


if __name__ == '__main__':
    app.run()
