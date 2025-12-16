# File: live_preview.py

from picamera2 import Picamera2
import cv2
import time

# --- Configuration ---
RESOLUTION = (1280, 720) # Standard HD resolution for the preview window
# Use an RGB format for display with OpenCV
FORMAT = "RGB888"

print("Initializing Pi Camera for Live Video...")
picam2 = Picamera2()

# Configure the camera for continuous preview mode
picam2.preview_configuration.main.size = RESOLUTION
picam2.preview_configuration.main.format = FORMAT
picam2.configure("preview")

print("Starting camera stream...")
picam2.start()
time.sleep(0.3)  # Short warm-up for stabilization

print("\nPress 'q' or ESC in the preview window to stop the stream.")

try:
    while True:
        # 1. Capture a frame from the stream as a NumPy array
        frame = picam2.capture_array()

        # 2. Display the frame in an OpenCV window
        # OpenCV expects BGR, but picamera2 gives RGB, so we convert it for correct color
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        cv2.imshow("Live Video Feed (PiCamera2)", frame_bgr)

        # 3. Check for the 'q' key press or ESC key to exit the loop
        # waitKey(1) makes the window responsive for 1 millisecond
        key = cv2.waitKey(1)
        if key == ord('q') or key == 27: # 27 is the ASCII code for ESC
            break

except KeyboardInterrupt:
    # Allows stopping the script by pressing Ctrl+C in the terminal
    pass

# --- Cleanup ---
print("\nStopping camera stream and closing window.")
picam2.stop()
cv2.destroyAllWindows()
print("Done.")
