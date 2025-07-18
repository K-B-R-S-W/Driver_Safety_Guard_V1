# Driver Safety Guard 🚗⚠️

**Driving Safety, One Posture at a Time**

A real-time driver monitoring system that detects unsafe driving behaviors and provides immediate alerts through visual and auditory feedback.

## 🎯 Project Overview

Driver Safety Guard is an AI-powered system that enhances road safety by monitoring driver behavior and detecting potentially dangerous postures. The system uses computer vision to identify five key states: awake, distracted, drowsy, mobile use, and smoking, providing real-time alerts to help drivers correct their behavior.

## ✨ Features

- **Real-time Detection**: Continuous monitoring of driver postures using YOLOv8
- **Multi-sensory Alerts**: Visual (color-coded LEDs) and auditory (buzzer) feedback
- **Wireless Communication**: ESP32-based alert system with HTTP API
- **User-friendly Interface**: Intuitive color-coded alert system
- **Automatic Timeout**: LEDs automatically turn off after 5 seconds
- **Comprehensive Testing**: Built-in hardware testing sequence

## 🛠️ Technology Stack

- **Computer Vision**: YOLOv8 for object detection and posture classification
- **Data Management**: Roboflow for dataset labeling and preprocessing
- **Hardware**: ESP32 microcontroller for device control
- **Programming**: Python for AI model, C++ for Arduino/ESP32
- **Libraries**: OpenCV, Ultralytics, Requests

## 📋 System Requirements

### Software Dependencies
```bash
pip install ultralytics opencv-python requests
```

### Hardware Components
- ESP32 microcontroller
- Camera (USB webcam)
- 4 LEDs (Green, Red, Orange, Blue)
- Buzzer
- Resistors and connecting wires
- Breadboard or PCB

## 🔧 Hardware Setup

### Pin Configuration (ESP32)
- **Green LED**: GPIO 5 (Distracted)
- **Red LED**: GPIO 18 (Drowsy)
- **Orange LED**: GPIO 19 (Mobile Use)
- **Blue LED**: GPIO 17 (Smoking)
- **Buzzer**: GPIO 16

### LED Alert Mapping
- 🟢 **Green LED**: Distracted behavior detected
- 🔴 **Red LED**: Drowsy behavior detected
- 🟠 **Orange LED**: Mobile phone use detected
- 🔵 **Blue LED**: Smoking detected

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/K-B-R-S-W/driver-safety-guard.git
cd driver-safety-guard
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Hardware Setup
1. Connect LEDs and buzzer to ESP32 according to pin configuration
2. Flash the Arduino code (`Main_Arduino_code.ino`) to ESP32
3. Update WiFi credentials in the Arduino code
4. Note the ESP32's IP address from serial monitor

### 4. Configure Python Script
Update the ESP32 IP address in `Main.py`:
```python
ESP32_IP = "http://(YOUR_ESP32_IP)"
```

Update the model path in `Main.py`:
```python
yolo_model = YOLO('Model_Run and Esp32 HTTP\weights/best.pt')
```

## 🎮 Usage

### Running the System
1. Power on the ESP32 and ensure it's connected to WiFi
2. Run the main detection script:
```bash
python Main.py
```
3. The system will automatically:
   - Check ESP32 connection
   - Start camera feed
   - Begin real-time detection
   - Send alerts to ESP32 when unsafe behavior is detected

### Controls
- Press `q` to quit the application
- The system automatically turns off all LEDs when exiting

## 🧠 Model Training

The system uses a custom-trained YOLOv8 model. To retrain the model:

1. **Dataset Preparation**: Use Roboflow for data labeling and augmentation
2. **Training**: Run the training script in Google Colab:
```python
!yolo task=detect mode=train model=yolov8m.pt data=data.yaml epochs=100 imgsz=640 plots=True
```
3. **Model Export**: Save the trained model weights (`best.pt`)

### Training Features
- Data augmentation (rotation, flipping, scaling)
- Transfer learning with pre-trained YOLOv8m
- GPU acceleration for faster training
- Comprehensive validation metrics

## 📊 System Architecture

```
Camera → YOLOv8 Model → Classification → ESP32 → LED/Buzzer Alert
   ↑                                        ↓
   └─────────── Continuous Monitoring ←─────┘
```

## 🔧 API Endpoints

The ESP32 provides the following HTTP endpoints:

- `GET /distracted` - Activate green LED and buzzer
- `GET /drowsy` - Activate red LED and buzzer  
- `GET /mobileuse` - Activate orange LED and buzzer
- `GET /smoking` - Activate blue LED and buzzer
- `GET /off` - Turn off all LEDs and buzzer

## 🧪 Testing

### Hardware Testing
The ESP32 automatically tests all components during startup:
- Sequential LED testing
- Buzzer functionality test
- Network connectivity verification

### Performance Metrics
- **Detection Accuracy**: >95% on test dataset
- **Real-time Processing**: ~30 FPS
- **Response Time**: <100ms from detection to alert

## 🚧 Challenges & Solutions

### Data Collection
- **Challenge**: Limited diverse dataset
- **Solution**: Applied data augmentation and simulated controlled environments

### Real-time Processing
- **Challenge**: Balancing accuracy with speed
- **Solution**: Model optimization and GPU acceleration

### Hardware Integration
- **Challenge**: Seamless software-hardware communication
- **Solution**: Robust HTTP API with error handling and reconnection logic

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 🙏 Acknowledgments

- YOLOv8 by Ultralytics for object detection framework
- Roboflow for dataset management and preprocessing
- ESP32 community for hardware support and documentation

## 📞 Support

For questions or support, please open an issue in the GitHub repository or contact Me.

---

**⚠️ Safety Notice**: This system is designed to assist drivers but should not replace safe driving practices. Always maintain focus on the road and follow traffic regulations.
