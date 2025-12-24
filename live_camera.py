import signal
import sys
import cv2
from picamera2 import Picamera2

picam2 = Picamera2()

def cleanup_and_exit():
    print('\n[SYSTEM] Releasing camera...')
    picam2.stop()
    picam2.close() # Prevents "Device or resource busy"
    cv2.destroyAllWindows()
    sys.exit(0)

def signal_handler(sig, frame):
    cleanup_and_exit()

signal.signal(signal.SIGINT, signal_handler)

try:
    config = picam2.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)})
    picam2.configure(config)
    picam2.start()
    print("Live Stream Starting on VNC Desktop...")

    while True:
        frame = picam2.capture_array()
        
        # --- THIS LINE MUST BE UNCOMMENTED FOR LIVE VIEW ---
        cv2.imshow("Pi Camera Live Feed", frame)
        
        # Press 'q' on the video window to stop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except Exception as e:
    print(f"Error: {e}")
finally:
    cleanup_and_exit() # Ensures consistency
