import cv2
import tkinter as tk

from tkinter import messagebox
from PIL import Image, ImageTk

from pathlib import Path
from datetime import datetime

# CAMERA CONFIGURATION
CAMERA_INDEX = 0

CAMERA_WIDTH = 1920
CAMERA_HEIGHT = 1080

# Optional camera parameters.
# Support depends on the webcam/driver.
SHUTTER_SPEED = -5
ISO = 400

# Burst capture interval in milliseconds.
BURST_INTERVAL = 150

# APPLICATION CONFIGURATION
APP_TITLE = "IoT Camera Capture System"

BASE_DIR = Path(__file__).resolve().parent
CAPTURE_DIR = BASE_DIR / "captures"

CAPTURE_DIR.mkdir(parents=True, exist_ok=True)

# CAMERA APPLICATION
class CameraApp:

    def __init__(self, root):
        self.root = root

        self.root.title(APP_TITLE)
        self.root.geometry("1100x800")
        self.root.minsize(900, 700)

        self.camera = None
        self.running = False

        self.capture_count = 0
        self.burst_active = False

        self.last_frame = None

        self.create_interface()
        self.start_camera()

        # Keyboard mapping
        self.root.bind("<KeyPress-c>", self.handle_capture_key)
        self.root.bind("<KeyPress-C>", self.handle_capture_key)

        self.root.bind("<KeyPress-b>", self.start_burst)
        self.root.bind("<KeyPress-B>", self.start_burst)

        self.root.bind("<KeyRelease-b>", self.stop_burst)
        self.root.bind("<KeyRelease-B>", self.stop_burst)

        self.root.bind("<KeyPress-q>", self.close_application)
        self.root.bind("<KeyPress-Q>", self.close_application)

        self.root.protocol("WM_DELETE_WINDOW", self.close_application)

    # GUI
    def create_interface(self):

        # Main title
        title = tk.Label(
            self.root,
            text="IoT Camera Capture System",
            font=("Arial", 20, "bold")
        )

        title.pack(pady=10)

        # Camera preview area
        self.preview_label = tk.Label(
            self.root,
            text="Initializing camera...",
            bg="black",
            fg="white"
        )

        self.preview_label.pack(
            padx=20,
            pady=10,
            fill=tk.BOTH,
            expand=True
        )

        # Information frame
        info_frame = tk.Frame(self.root)
        info_frame.pack(fill=tk.X, padx=20, pady=5)

        self.resolution_label = tk.Label(
            info_frame,
            text=f"Resolution: {CAMERA_WIDTH} x {CAMERA_HEIGHT}",
            font=("Arial", 11)
        )

        self.resolution_label.pack(side=tk.LEFT)

        self.status_label = tk.Label(
            info_frame,
            text="Status: Initializing...",
            font=("Arial", 11)
        )

        self.status_label.pack(side=tk.RIGHT)

        # Button frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        capture_button = tk.Button(
            button_frame,
            text="Capture",
            width=15,
            height=2,
            command=self.capture_image
        )

        capture_button.pack(
            side=tk.LEFT,
            padx=5
        )

        exit_button = tk.Button(
            button_frame,
            text="Exit",
            width=15,
            height=2,
            command=self.close_application
        )

        exit_button.pack(
            side=tk.LEFT,
            padx=5
        )

        # Keyboard information
        keyboard_info = tk.Label(
            self.root,
            text=(
                "Keyboard: C = Capture | "
                "B = Burst Capture | "
                "Q = Exit"
            ),
            font=("Arial", 10)
        )

        keyboard_info.pack(pady=(5, 15))

    # START CAMERA
    def start_camera(self):

        self.camera = cv2.VideoCapture(CAMERA_INDEX)

        if not self.camera.isOpened():

            self.status_label.config(
                text="Status: Camera not available"
            )

            self.preview_label.config(
                text="Camera could not be opened."
            )

            messagebox.showerror(
                "Camera Error",
                (
                    "Camera tidak dapat dibuka.\n\n"
                    "Pastikan webcam tersedia dan tidak sedang "
                    "digunakan aplikasi lain."
                )
            )

            return

        # Set camera resolution
        self.camera.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            CAMERA_WIDTH
        )

        self.camera.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            CAMERA_HEIGHT
        )

        # Optional shutter speed
        if SHUTTER_SPEED is not None:

            self.camera.set(
                cv2.CAP_PROP_EXPOSURE,
                SHUTTER_SPEED
            )

        # Optional ISO
        if ISO is not None:

            self.camera.set(
                cv2.CAP_PROP_ISO_SPEED,
                ISO
            )

        self.running = True

        self.status_label.config(
            text="Status: Camera Active"
        )

        self.update_frame()

    # LIVE PREVIEW
    def update_frame(self):

        if not self.running:
            return

        ret, frame = self.camera.read()

        if not ret:

            self.status_label.config(
                text="Status: Failed to read camera"
            )

            self.root.after(
                100,
                self.update_frame
            )

            return

        self.last_frame = frame.copy()

        # Convert BGR -> RGB
        frame_rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # Convert OpenCV image to PIL
        image = Image.fromarray(frame_rgb)

        # Resize preview while maintaining aspect ratio
        preview_width = 1000
        preview_height = 600

        image.thumbnail(
            (preview_width, preview_height),
            Image.Resampling.LANCZOS
        )

        photo = ImageTk.PhotoImage(image=image)

        self.preview_label.config(
            image=photo,
            text=""
        )

        self.preview_label.image = photo

        # Continue preview
        self.root.after(
            15,
            self.update_frame
        )

    # CAPTURE IMAGE
    def capture_image(self):

        if self.last_frame is None:

            self.status_label.config(
                text="Status: No frame available"
            )

            return

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S_%f"
        )

        filename = (
            CAPTURE_DIR /
            f"capture_{timestamp}.jpg"
        )

        success = cv2.imwrite(
            str(filename),
            self.last_frame
        )

        if success:

            self.capture_count += 1

            self.status_label.config(
                text=(
                    f"Captured: {filename.name} "
                    f"({self.capture_count} files)"
                )
            )

        else:

            self.status_label.config(
                text="Status: Failed to save image"
            )

    # ========================================================
    # KEYBOARD CAPTURE
    # ========================================================

    def handle_capture_key(self, event):

        # C = single capture
        self.capture_image()

    # ========================================================
    # BURST CAPTURE
    # ========================================================

    def start_burst(self, event=None):

        if self.burst_active:
            return

        self.burst_active = True

        self.status_label.config(
            text="Status: Burst Capture Active"
        )

        self.burst_capture()

    def burst_capture(self):

        if not self.burst_active:
            return

        self.capture_image()

        self.root.after(
            BURST_INTERVAL,
            self.burst_capture
        )

    def stop_burst(self, event=None):

        self.burst_active = False

        if self.running:

            self.status_label.config(
                text="Status: Camera Active"
            )

    # CLOSE APPLICATION
    def close_application(self, event=None):

        self.running = False
        self.burst_active = False

        if self.camera is not None:

            self.camera.release()
            self.camera = None

        self.root.destroy()

# MAIN PROGRAM
if __name__ == "__main__":

    root = tk.Tk()

    app = CameraApp(root)

    root.mainloop()