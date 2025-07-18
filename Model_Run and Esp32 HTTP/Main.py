import cv2
from ultralytics import YOLO
import requests
import time

def check_esp32_connection(esp32_ip):
    print("Checking ESP32 connection...")
    while True:
        try:
            response = requests.get(f"{esp32_ip}/off")
            if response.status_code == 200:
                print("ESP32 connection established.")
                return True
        except requests.exceptions.ConnectionError:
            print("Wating for ESP32. Retrying in 2 seconds...")
            time.sleep(2)
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(2)

def detect_from_camera():
    print("Loading YOLO model...")
    yolo_model = YOLO('C:\\Users\\DEATHSEC\\Desktop\\New folder (2)\\train\\weights\\best.pt')

    ESP32_IP = "http://192.168.1.13"
    print(f"ESP32 IP set to: {ESP32_IP}")

    # Verify ESP32 connection
    check_esp32_connection(ESP32_IP)

    print("Opening camera...")
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("Error: Could not open the camera.")
        return

    print("Camera successfully opened. Starting detection...")

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Error: Failed to capture frame from the camera.")
            break

        results = yolo_model(frame)
        print("Frame captured and processed.")

        for result in results:
            classes = result.names
            cls = result.boxes.cls
            conf = result.boxes.conf
            detections = result.boxes.xyxy

            for pos, detection in enumerate(detections):
                if conf[pos] >= 0.5:
                    xmin, ymin, xmax, ymax = detection
                    label = f"{classes[int(cls[pos])]} {conf[pos]:.2f}"
                    color = (0, int(cls[pos]), 255)
                    cv2.rectangle(frame, (int(xmin), int(ymin)), (int(xmax), int(ymax)), color, 2)
                    cv2.putText(frame, label, (int(xmin), int(ymin) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)
                    print(f"Detected: {label}")

                    # Send command to ESP32 to light the corresponding LED
                    try:
                        if classes[int(cls[pos])] == 'Distracted':
                            requests.get(f"{ESP32_IP}/distracted")
                            print("Sent command to ESP32: Distracted")
                        elif classes[int(cls[pos])] == 'Drowsy':
                            requests.get(f"{ESP32_IP}/drowsy")
                            print("Sent command to ESP32: Drowsy")
                        elif classes[int(cls[pos])] == 'Mobile Use':
                            requests.get(f"{ESP32_IP}/mobileuse")
                            print("Sent command to ESP32: Mobile Use")
                        elif classes[int(cls[pos])] == 'Smoking':
                            requests.get(f"{ESP32_IP}/smoking")
                            print("Sent command to ESP32: Smoking")
                    except requests.exceptions.ConnectionError as e:
                        print(f"Error sending command to ESP32: {e}")
                        print("Rechecking ESP32 connection...")
                        check_esp32_connection(ESP32_IP)
                        continue

        # Display the resulting frame
        cv2.imshow('Detection', frame)

        # Check if the user pressed 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Quit signal received. Exiting...")
            break

    # Release the camera and close all OpenCV windows
    video_capture.release()
    cv2.destroyAllWindows()
    print("Camera released and all OpenCV windows closed.")

    # Send command to ESP32 to turn off all LEDs
    try:
        requests.get(f"{ESP32_IP}/off")
        print("Sent command to ESP32: All Off")
    except requests.exceptions.ConnectionError as e:
        print(f"Error sending 'off' command to ESP32: {e}")

# Start the detection process
detect_from_camera()