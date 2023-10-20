from ultralytics import YOLO
import cv2
import math 
import time
import boto3
from geopy.geocoders import Nominatim
from geopy.point import Point
import json

# start webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 640)

# model
model = YOLO("best.pt")

# object classes
classNames = ["Potholes"]

fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
duration_minutes = total_frames / fps

# Initialize counters
detections_count = 0
frame_number = 0

confidence_threshold = 0.65  # set your confidence threshold here

# database implementation:
dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

# Table defination
table = dynamodb.create_table(
    TableName='Potholes',
    KeySchema=[
        {
            'AttributeName': 'pothole_id',
            'KeyType': 'N'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'pothole_id',
            'AttributeType': 'N'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
) 

# load data in table
def load_data(potholes, dynamodb=None):
    dynamodb = boto3.resource(
        'dynamodb', endpoint_url="http://localhost:8000")

    potholes_table = dynamodb.Table('Potholes')
    for pothole in potholes:
        pothole_id = (pothole['pothole_id'])
        print("Loading Potholes Data:", pothole_id)
        potholes_table.put_item(Item=pothole)


# put data in table
def put_pothole(pothole_id, data, dynamodb=None):
    dynamodb = boto3.resource(
        'dynamodb', endpoint_url="http://localhost:8000")
    # Specify the table
    potholes_table = dynamodb.Table('Potholes')
    response = potholes_table.put_item(
        # Data to be inserted
        Item={
            'pothole_id': pothole_id,
            'info': {
                'latitude':                    data['latitude'],
                'longitude':                   data['longitude'],
                'vehicle_registration_number': data['vehicle_registration_number'],
                'area':                        data['area'],
                'area_type':                   data['area_type'],
                'time_of_capture':             data['time_of_capture']
            }
        }
    )
    return response

while True:
    success, img = cap.read()
    results = model(img, stream=True)

    # coordinates
    for r in results:
        predictions = r.boxes

        for prediction in predictions:
            if math.ceil((prediction.conf[0]*100))/100 > confidence_threshold:
                # bounding prediction
                x1, y1, x2, y2 = prediction.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

                # put prediction in cam
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

                # confidence
                confidence = round((prediction.conf[0]*100)/100, 1)
                print("Confidence --->",confidence)

                if confidence > 0.5:
                    detections_count += 1

                # class name
                cls = int(prediction.cls[0])
                print("Class name -->", classNames[cls])

                # object details
                org = [x1, y1]
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 1
                color = (255, 0, 0)
                thickness = 2

                cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)

                #store this info to db
                loc = Nominatim(user_agent="Get Location")
                lat = 28.510319
                long = 77.0530094
                location = loc.reverse(str(lat) + ", " + str(long)) # Used for example. will be fetched from vehicle/user's location
                data = {
                    "latitude": lat,
                    "longitude": long,
                    "road_condition":prediction,
                    "vehicle_registration_number":1234, # for compliance
                    "area": loc,
                    "area_type": "urban", # Needs to be classified from a saved registery
                    "time_of_capture": time.time()
                }
                put_pothole(3, data)

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) == ord('q'):
        break

def check_and_notify(dynamodb=None):
    start_time = time.time()
    one_hour_ago = start_time - 3600

    # Read data between range of time
    dynamodb = boto3.resource(
        'dynamodb', endpoint_url="http://localhost:8000")
    # Specify the table to read from
    potholes_table  = dynamodb.Table('Potholes')
    now             = start_time.strftime('%FT%T+13:00')
    one_hour_ago    = one_hour_ago.strftime('%FT%T+13:00')
    fe = boto3.dynamodb.conditions.Attr('time_of_capture')

    response = potholes_table.scan(
                    FilterExpression=fe
                )
    
    # logic for notifying
    # Create a dictionary to store the counts of each area within the past hour

    area_counts = {}

    for entry in response:
        area = entry["area"]
        capture_time = entry["time_of_capture"]

        if capture_time >= one_hour_ago:
            if area in area_counts:
                area_counts[area] += 1
            else:
                area_counts[area] = 1
    
    for entry in response:
        area = entry.get("area")
        if area and area in area_counts and area_counts[area] >= 100 and area not in notification_sent:
            send_notification(entry)
            notification_sent[area] = True


# Track whether notification has been sent for each area
notification_sent = {}
          
def send_notification(data):
    print("Sending notification:", data)

# Track whether notification has been sent for each area
notification_sent = {}
check_and_notify()

cap.release()
cv2.destroyAllWindows()