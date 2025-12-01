# MediaPipe Setup

This project relies on **MediaPipe’s Hand Gesture Recognizer Task**, which is a consolidated pipeline of multiple machine learning models provided by Google. The task handles **hand detection**, **landmark extraction**, **feature embedding**, and **gesture classification** in a unified workflow.

Below is a breakdown of its core components and overall workflow.

---

## Overview of the Hand Gesture Recognition Pipeline

The full pipeline consists of two main stages:

### **1. Hand Landmarking**

This stage detects hands and extracts 3D coordinates of keypoints from the image. It is composed of the following models:

| Component | Purpose |
|-----------|---------|
| **hand_detector** | Detects palm regions and outputs initial bounding boxes. |
| **hand_landmark_detector** | Predicts 21 anatomical hand landmarks (x, y, z) for each detected hand. |

These two models form the **hand_landmarker**, which provides accurate localization and pose estimation of the hand in real time.

---

### **2. Gesture Recognition**

After landmark extraction, the system interprets the hand posture as a specific gesture. This stage contains:

| Component | Purpose |
|-----------|---------|
| **gesture_embedder** | Converts landmark coordinates into a compact feature vector (embedding). |
| **canned_gesture_classifier** | Classifies the embedding to a predefined label using a trained classifier. |

The classifier is pre-trained on MediaPipe’s built-in gesture dataset. Custom gestures can be added by training on additional samples and expanding the label set.

---

## How to Setup

- Download the latest `HandGestureClassifier` from [models](https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer#models).
- This model can be unzipped and the following content should be available:

```
├── hand_gesture_recognizer
│   ├── canned_gesture_classifier.tflite
│   └── gesture_embedder.tflite
└── hand_landmarker
    ├── hand_detector.tflite
    └── hand_landmarks_detector.tflite

```

- These files are by default formatted as `.task` file. You can unzip them via the following command lines;

```
unzip gesture_recognizer.task -d extracted_folder
```

## Reference

The official documentation, model specifications, configuration options, and sample code can be found on the MediaPipe website:

- [Gesture recognition task guide](https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer)
- [Get started guide - Python](https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer/python)

