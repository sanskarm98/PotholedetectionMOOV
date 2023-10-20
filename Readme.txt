POTHOLE DETECTION THROUGH LIVE-FEED

Run make run, it will create a virtual environment (if not already created), activate it, 
install the required dependencies, and finally run your Python script.

Note: Make sure that you have make and python3-venv installed on your system. You can install them using:
sudo apt-get install make python3-venv

Files:
sampledetection.py: for an example to run on computers, input a video file to detect potholes in it
realtimedetection.py: this file will actually be working with the vehicle's webcam
realtimedetection_with_aws_sdk.py: this will be our approach for saving metadata to cloud storage and notification 
