"""
simple_spectrum.py
Starter version of the spectrometer code.

Steps:
  1. Grab one frame from the camera (or open a saved image)
  2. Turn it into grayscale (brightness only)???????
  3. Average each column of pixels -> a 1D array (one number per column)
  4. Scale the array to 0-1
  5. Save a CSV and a graph (intensity vs. pixel)

Examples:
  python3 simple_spectrum.py                      # camera 0
  python3 simple_spectrum.py --camera 1           # a different camera
  python3 simple_spectrum.py --image photo.png    # a saved image instead
  python3 simple_spectrum.py --rows 300 420       # only the rows the spectrum is on
  python3 simple_spectrum.py --out sample1        # saves sample1.csv and sample1.png

Install:  pip install opencv-python numpy matplotlib
          (on the Pi: sudo apt install python3-opencv python3-numpy python3-matplotlib)
"""

import argparse
import csv
# 
import cv2
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def get_settings():
    p = argparse.ArgumentParser(description="One frame -> 1D spectrum (CSV + graph)")
    p.add_argument("--camera", type=int, default=0, help="camera number (default 0)")
    p.add_argument("--image", help="use a saved image instead of the camera")
    p.add_argument("--rows", nargs=2, type=int, metavar=("TOP", "BOTTOM"),
                   help="only average these rows (default: all rows)")
    p.add_argument("--out", default="spectrum", help="output name (default: spectrum)")
    return p.parse_args()


def get_frame(settings):
    """one frame from a saved image or the camera"""
    if settings.image:
        frame = cv2.imread(settings.image)
        if frame is None:
            raise SystemExit(f"Could not open image: {settings.image}")
        return frame

    camera = cv2.VideoCapture(settings.camera)
    if not camera.isOpened():
        raise SystemExit(f"Camera {settings.camera} did not open")
    ok, frame = camera.read()
    camera.release()
    if not ok:
        raise SystemExit("Camera opened but returned no frame")
    return frame


def frame_to_spectrum(frame, rows):
    """Steps 2-4: grayscale, average each column, scale to 0-1."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).astype(float)   # convert

    if rows:
        top, bottom = rows
        gray = gray[top:bottom, :]          # keep only the spectrum rows

    column_average = gray.mean(axis=0)      # one number per column
    scaled = column_average / column_average.max()   # brightest column = 1
    return column_average, scaled


def save_results(column_average, scaled, name):
    """save results with csv and save as image in png"""
    with open(f"{name}.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["pixel", "average_intensity", "intensity_0_to_1"])
        for pixel in range(len(column_average)):
            writer.writerow([pixel, round(column_average[pixel], 3), round(scaled[pixel], 5)])

    plt.figure(figsize=(10, 4))
    plt.plot(scaled)
    plt.xlabel("Pixel (column)")
    plt.ylabel("Intensity (0 to 1)")
    plt.ylim(0, 1.05)
    plt.title("Spectrum")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{name}.png", dpi=150)


def main():
    settings = get_settings()
    frame = get_frame(settings)
    print(f"Frame size: {frame.shape[1]} columns x {frame.shape[0]} rows")

    column_average, scaled = frame_to_spectrum(frame, settings.rows)
    save_results(column_average, scaled, settings.out)

    print(f"1D array has {len(column_average)} values")
    print(f"Brightest column: {column_average.argmax()}")
    print(f"Saved {settings.out}.csv and {settings.out}.png")


if __name__ == "__main__":
    main()
