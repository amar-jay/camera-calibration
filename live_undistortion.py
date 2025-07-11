import cv2
import os
import pickle

def live_undistortion(camera_id, calibration_file):
    """
    Demonstrate live camera undistortion using calibration results.
    """
    if not os.path.exists(calibration_file):
        print(f"Error: Calibration file not found at {calibration_file}")
        print("Please run camera_calibration.py first to generate calibration data.")
        return

    with open(calibration_file, 'rb') as f:
        calibration_data = pickle.load(f)

    mtx = calibration_data['camera_matrix']
    dist = calibration_data['distortion_coefficients']

    print("Loaded camera calibration data:")
    print(f"Camera Matrix:\n{mtx}")
    print(f"Distortion Coefficients: {dist.ravel()}")

    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        print(f"Error: Could not open camera {camera_id}")
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"Camera resolution: {width}x{height}")

    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (width, height), 1, (width, height))
    mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (width, height), 5)

    print("Press 'q' to quit, 'd' to toggle distortion correction")

    correct_distortion = True

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image")
            break

        if correct_distortion:
            undistorted = cv2.remap(frame, mapx, mapy, cv2.INTER_LINEAR)
            x, y, w, h = roi
            undistorted = undistorted[y:y+h, x:x+w]
            undistorted = cv2.resize(undistorted, (width, height))
            cv2.putText(undistorted, "Undistorted", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('Camera Feed', undistorted)
        else:
            cv2.putText(frame, "Original", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow('Camera Feed', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('d'):
            correct_distortion = not correct_distortion
            print(f"Distortion correction {'ON' if correct_distortion else 'OFF'}")

    cap.release()
    cv2.destroyAllWindows()

def parse_args():
    parser = argparse.ArgumentParser(description="Live undistortion using camera calibration data.")
    parser.add_argument('--camera_id', type=int, default=0, help='Camera device ID (default: 0)')
    parser.add_argument('--calibration_file', type=str, default='output/calibration_data.pkl',
                        help='Path to calibration data file (pickle format)')
    return parser.parse_args()

if __name__ == "__main__":
    import argparse
    args = parse_args()
    live_undistortion(args.camera_id, args.calibration_file)

