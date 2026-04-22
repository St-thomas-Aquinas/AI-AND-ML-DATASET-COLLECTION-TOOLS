# 🎥 Frame Extractor for Machine Learning Datasets

## Overview

This script captures a video using OpenCV and automatically splits it into individual image frames. These frames can then be used to build datasets for training machine learning models, particularly for computer vision tasks.

## Use Case

A typical use case involves placing an object—such as a **banana plant**—in front of the camera.  
The camera is then **rotated around the object** to capture it from multiple angles.

Once the video is recorded, the script extracts individual frames and saves them as image files.  
These images can be used to train computer vision models for:

- ✅ Object classification  
- ✅ Object detection  
- ✅ Object recognition  

## Requirements

- Python 3.x  
- OpenCV (`opencv-python`)

## Installation

```bash
pip install opencv-python
```

## How to Use

1. Record a video by rotating the camera around the object.
2. Run the script to extract and save the frames.
3. Use the extracted images as a dataset for your machine learning pipeline.

## License

MIT License
