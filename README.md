# 🎯 Camera Calibration Scripts

This is a small collection of camera calibration scripts using OpenCV. Nothing groundbreaking — just a clean and practical setup I put together (mostly for a project called Nebula, but figured it might be useful to me some other time).

If you're new to camera calibration, you can always check the [OpenCV documentation](https://docs.opencv.org/) — this project is basically a simplified and organized implementation of it.

## 📦 What's Inside

This mini toolchain includes 3 scripts:

- `capture_calibration_images.py`  
  Opens your camera and lets you capture frames of a chessboard pattern. Just press 'c' to snap a frame. Saves to a folder.

- `camera_calibration.py`  
  Calibrates your camera using the captured images. Generates the camera matrix, distortion coefficients, and saves them as `.pkl` and `.txt`.

- `live_undistortion.py`  
  Opens a live camera feed and shows the real-time undistorted view using your calibration data. You can toggle correction with 'd'.

## 🚀 Example Usage

```bash
# Capture chessboard images
python capture.py \
  --camera_id 0 \
  --chessboard_rows 23 \
  --chessboard_cols 15 \
  --output_dir calibration_images
```

```bash
# Calibrate the camera using captured images
python calibrate.py \
  --chessboard_rows 23 \
  --chessboard_cols 15 \
  --square_size 2.5 \
  --calibration_path "calibration_images/*.jpg" \
  --output_dir "output" \
  --save_undistorted
```

```bash
# Live undistortion demo
python live_undistort.py \
  --camera_id 0 \
  --calibration_file output/calibration_data.pkl
```

