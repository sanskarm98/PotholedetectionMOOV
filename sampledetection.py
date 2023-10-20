import os
import cv2
import math
from ultralytics import YOLO

# Specify the path to the video file or image file
input_path = "test3.mp4"

# Output directory for saving results
output_directory = "D:/potholemoov3/pyoutput/"

# model
model = YOLO("best.pt")

# object classes
classNames = ["Potholes"]

confidence_threshold = 0.25  # set your confidence threshold here

# Check if the input is a video file or an image file
if input_path.endswith('.mp4') or input_path.endswith('.avi'):
    # Open the video file
    cap = cv2.VideoCapture(input_path)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    output_file_name = os.path.basename(input_path)
    output_file_path = os.path.join(output_directory, output_file_name)
    out = cv2.VideoWriter(output_file_path, cv2.VideoWriter_fourcc(*'XVID'), 20, (frame_width, frame_height))

    while True:
        success, img = cap.read()
        if not success:
            break

        results = model(img, stream=True)

        # coordinates
        for r in results:
            boxes = r.boxes

            for box in boxes:
                if math.ceil((box.conf[0] * 100)) / 100 > confidence_threshold:
                    # bounding box
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # convert to int values

                    # put box in cam
                    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

                    # confidence
                    confidence = math.ceil((box.conf[0] * 100)) / 100
                    # class name
                    cls = int(box.cls[0])
                    class_name = classNames[cls]

                    # Draw class label inside the box
                    label = f'{class_name}: {confidence}'
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 0.8
                    font_thickness = 1
                    label_size = cv2.getTextSize(label, font, font_scale, font_thickness)[0]
                    label_x = x1
                    label_y = y1 - label_size[1]

                    cv2.putText(img, label, (label_x, label_y), font, font_scale, (255, 255, 255), font_thickness,
                                lineType=cv2.LINE_AA)

        out.write(img)
        cv2.imshow('Video', img)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

elif input_path.endswith('.jpg') or input_path.endswith('.png'):
    # Read the image file
    img = cv2.imread(input_path)
    results = model(img)

    # coordinates
    for r in results:
        boxes = r.boxes

        for box in boxes:
            if math.ceil((box.conf[0] * 100)) / 100 > confidence_threshold:
                # bounding box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # convert to int values

                # put box in image
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

                # confidence
                confidence = math.ceil((box.conf[0] * 100)) / 100
                # class name
                cls = int(box.cls[0])
                class_name = classNames[cls]

                # Draw class label inside the box
                label = f'{class_name}: {confidence}'
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.8
                font_thickness = 1
                label_size = cv2.getTextSize(label, font, font_scale, font_thickness)[0]
                label_x = x1
                label_y = y1 - label_size[1]

                cv2.putText(img, label, (label_x, label_y), font, font_scale, (255, 255, 255), font_thickness,
                            lineType=cv2.LINE_AA)

    # Construct output file path
    input_file_name = os.path.basename(input_path)
    output_file_path = os.path.join(output_directory, input_file_name)

    cv2.imwrite(output_file_path, img)
    cv2.imshow('Image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

else:
    print("Invalid file format. Supported formats are: .mp4, .avi, .jpg, .png")
