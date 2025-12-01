# YOLO Model Setup

This project uses the **YOLO11n** model from the Ultralytics YOLO family for real-time object detection. The model provides a good balance between speed and accuracy and is suitable for deployment on edge devices and embedded systems when exported to formats such as **ONNX**.

---

## Model Overview

| Model | Parameters | Performance | Suitable For |
|-------|------------|-------------|---------------|
| `YOLO11n` | Lightweight | Fast inference | Edge devices / CPU / low-power systems |

YOLO models are introduced in the official documentation:
https://docs.ultralytics.com/models/yolo11/

---

## Downloading the Model

To locate and download the **YOLO11n** model, refer to the **Models** section here:
https://docs.ultralytics.com/tasks/detect/

You may download the model using the Ultralytics command-line interface or directly from the documentation download links.

---

## Exporting to ONNX Format

After downloading the model, follow the export instructions provided in the Ultralytics documentation to convert the model to **ONNX**:

```bash
yolo export model=yolo11n.pt format=onnx
````

Make sure that:

* The model file (`.pt`) is downloaded and available.
* The correct format is specified (`onnx`).
* The exported model is validated using a simple inference test.

Full export instructions are provided [ONNX Export for YOLO11 Models](https://docs.ultralytics.com/integrations/onnx/).

