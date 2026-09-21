import cv2
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from pathlib import Path
from datetime import datetime

# ============================================================
# WRAPSTATION - IoT CAMERA CAPTURE SYSTEM
# Modern split-panel UI
#
# Technical-test requirements:
# - Live camera preview
# - Keyboard key mapping for capture
# - Captured images saved locally
# - Simple, responsive UI
# ============================================================

WINDOW_WIDTH = 1050
WINDOW_HEIGHT = 680
MIN_WIDTH = 1050
MIN_HEIGHT = 680

CAMERA_INDEX = 0
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720

# Preview is intentionally limited so it does not take the whole laptop screen.
PREVIEW_WIDTH = 640
PREVIEW_HEIGHT = 360

CAPTURE_DIR = Path(__file__).resolve().parent.parent / "captures"
CAPTURE_DIR.mkdir(parents=True, exist_ok=True)


class CameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wrapstation • IoT Camera Capture")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(MIN_WIDTH, MIN_HEIGHT)
        self.root.resizable(True, True)

        self.camera = None
        self.running = False
        self.last_frame = None
        self.photo = None

        self.capture_count = 0
        self.capture_key = "SPACE"

        self.status_var = tk.StringVar(value="Connecting to camera...")
        self.counter_var = tk.StringVar(value="0 photos")
        self.key_var = tk.StringVar(value="SPACE")
        self.device_var = tk.StringVar(value="Camera 0")

        self.configure_style()
        self.build_ui()
        self.bind_keys()

        self.root.protocol("WM_DELETE_WINDOW", self.close_app)
        self.start_camera()

    # --------------------------------------------------------
    # UI
    # --------------------------------------------------------
    def configure_style(self):
        self.root.configure(bg="#0f172a")

        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "App.TFrame",
            background="#0f172a"
        )
        style.configure(
            "Card.TFrame",
            background="#111827"
        )
        style.configure(
            "Panel.TFrame",
            background="#172033"
        )
        style.configure(
            "Title.TLabel",
            background="#0f172a",
            foreground="#f8fafc",
            font=("Segoe UI", 20, "bold")
        )
        style.configure(
            "Subtitle.TLabel",
            background="#0f172a",
            foreground="#94a3b8",
            font=("Segoe UI", 9)
        )
        style.configure(
            "CardTitle.TLabel",
            background="#172033",
            foreground="#f8fafc",
            font=("Segoe UI", 12, "bold")
        )
        style.configure(
            "Normal.TLabel",
            background="#172033",
            foreground="#cbd5e1",
            font=("Segoe UI", 9)
        )
        style.configure(
            "Value.TLabel",
            background="#172033",
            foreground="#f8fafc",
            font=("Segoe UI", 10, "bold")
        )
        style.configure(
            "Primary.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(14, 10)
        )
        style.configure(
            "Secondary.TButton",
            font=("Segoe UI", 9),
            padding=(12, 8)
        )
        style.configure(
            "TCombobox",
            padding=5
        )

    def build_ui(self):
        outer = ttk.Frame(self.root, style="App.TFrame", padding=18)
        outer.pack(fill="both", expand=True)

        # Header
        header = ttk.Frame(outer, style="App.TFrame")
        header.pack(fill="x", pady=(0, 14))

        ttk.Label(
            header,
            text="IoT Camera Capture",
            style="Title.TLabel"
        ).pack(anchor="w")

        ttk.Label(
            header,
            text="Live preview and keyboard-controlled image capture",
            style="Subtitle.TLabel"
        ).pack(anchor="w", pady=(3, 0))

        # Main split layout: camera LEFT, controls RIGHT.
        content = ttk.Frame(outer, style="App.TFrame")
        content.pack(fill="both", expand=True)

        content.columnconfigure(0, weight=0)
        content.columnconfigure(1, weight=0)
        content.rowconfigure(0, weight=1)

        # ----------------------------------------------------
        # LEFT: camera preview
        # ----------------------------------------------------
        preview_card = ttk.Frame(
            content,
            style="Card.TFrame",
            padding=12,
            width=680,
            height=500
        )
        preview_card.grid(
            row=0,
            column=0,
            sticky="nw",
            padx=(0, 12)
        )
        preview_card.grid_propagate(False)

        preview_header = ttk.Frame(
            preview_card,
            style="Card.TFrame"
        )
        preview_header.pack(fill="x", pady=(0, 8))

        ttk.Label(
            preview_header,
            text="LIVE PREVIEW",
            style="CardTitle.TLabel"
        ).pack(side="left")

        self.live_badge = tk.Label(
            preview_header,
            text=" ● OFFLINE ",
            bg="#7f1d1d",
            fg="#fecaca",
            font=("Segoe UI", 8, "bold"),
            padx=6,
            pady=3
        )
        self.live_badge.pack(side="right")

        # Fixed initial preview dimensions. It will resize proportionally
        # when the window itself is resized.
        self.video_frame = tk.Frame(
            preview_card,
            width=PREVIEW_WIDTH,
            height=PREVIEW_HEIGHT,
            bg="#020617",
            highlightthickness=1,
            highlightbackground="#334155"
        )
        self.video_frame.pack(
            fill="both",
            expand=True
        )
        self.video_frame.pack_propagate(False)

        self.video_label = tk.Label(
            self.video_frame,
            text="Starting camera...",
            bg="#020617",
            fg="#94a3b8",
            font=("Segoe UI", 11),
            justify="center"
        )
        self.video_label.pack(
            fill="both",
            expand=True
        )

        ttk.Label(
            preview_card,
            text="Preview is automatically scaled to fit this panel.",
            style="Subtitle.TLabel"
        ).pack(anchor="w", pady=(8, 0))

        # ----------------------------------------------------
        # RIGHT: control panel
        # ----------------------------------------------------
        panel = ttk.Frame(
            content,
            style="Panel.TFrame",
            padding=18,
            width=315
        )
        panel.grid(
            row=0,
            column=1,
            sticky="ns"
        )
        panel.grid_propagate(False)

        ttk.Label(
            panel,
            text="CONTROL PANEL",
            style="CardTitle.TLabel"
        ).pack(anchor="w")

        ttk.Label(
            panel,
            text="Camera",
            style="Normal.TLabel"
        ).pack(anchor="w", pady=(22, 2))

        ttk.Label(
            panel,
            textvariable=self.device_var,
            style="Value.TLabel"
        ).pack(anchor="w")

        ttk.Separator(panel).pack(fill="x", pady=14)

        ttk.Label(
            panel,
            text="Capture Key",
            style="Normal.TLabel"
        ).pack(anchor="w", pady=(0, 5))

        key_box = ttk.Combobox(
            panel,
            textvariable=self.key_var,
            values=("SPACE", "ENTER"),
            state="readonly",
            width=18
        )
        key_box.pack(fill="x")
        key_box.bind(
            "<<ComboboxSelected>>",
            self.change_capture_key
        )

        self.capture_button = ttk.Button(
            panel,
            text="📷  CAPTURE PHOTO",
            style="Primary.TButton",
            command=self.capture_image
        )
        self.capture_button.pack(
            fill="x",
            pady=(18, 8)
        )

        ttk.Label(
            panel,
            text="Keyboard shortcut",
            style="Normal.TLabel"
        ).pack(anchor="w")

        ttk.Label(
            panel,
            text="Press SPACE or ENTER",
            style="Value.TLabel"
        ).pack(anchor="w", pady=(2, 0))

        ttk.Separator(panel).pack(fill="x", pady=18)

        ttk.Label(
            panel,
            text="CAPTURED",
            style="Normal.TLabel"
        ).pack(anchor="w")

        ttk.Label(
            panel,
            textvariable=self.counter_var,
            style="Value.TLabel"
        ).pack(anchor="w", pady=(3, 0))

        ttk.Separator(panel).pack(fill="x", pady=18)

        ttk.Label(
            panel,
            text="STATUS",
            style="Normal.TLabel"
        ).pack(anchor="w")

        self.status_label = ttk.Label(
            panel,
            textvariable=self.status_var,
            style="Normal.TLabel",
            wraplength=270,
            justify="left"
        )
        self.status_label.pack(
            anchor="w",
            fill="x",
            pady=(5, 0)
        )

        ttk.Button(
            panel,
            text="⏹  EXIT APPLICATION",
            style="Secondary.TButton",
            command=self.close_app
        ).pack(
            fill="x",
            side="bottom",
            pady=(12, 0)
        )

        ttk.Label(
            panel,
            text="ESC = Exit",
            style="Subtitle.TLabel"
        ).pack(
            side="bottom",
            anchor="w",
            pady=(0, 8)
        )

    # --------------------------------------------------------
    # Keyboard mapping
    # --------------------------------------------------------
    def bind_keys(self):
        self.root.bind("<Escape>", self.close_app)
        self.root.bind("<space>", self.handle_capture)
        self.root.bind("<Return>", self.handle_capture)

    def change_capture_key(self, _event=None):
        self.capture_key = self.key_var.get()
        self.status_var.set(
            f"Ready • Capture key: {self.capture_key}"
        )

    def handle_capture(self, event=None):
        # Only the selected key triggers capture.
        pressed = "ENTER" if event and event.keysym == "Return" else "SPACE"

        if pressed == self.capture_key:
            self.capture_image()
            return "break"

    # --------------------------------------------------------
    # Camera
    # --------------------------------------------------------
    def start_camera(self):
        # CAP_DSHOW is generally reliable on Windows.
        self.camera = cv2.VideoCapture(
            CAMERA_INDEX,
            cv2.CAP_DSHOW
        )

        if not self.camera.isOpened():
            self.camera.release()
            self.camera = cv2.VideoCapture(CAMERA_INDEX)

        if not self.camera.isOpened():
            self.running = False
            self.live_badge.config(
                text=" ● ERROR ",
                bg="#7f1d1d",
                fg="#fecaca"
            )
            self.status_var.set(
                "Camera could not be opened."
            )
            self.video_label.config(
                text=(
                    "CAMERA NOT AVAILABLE\n\n"
                    "Check camera permission,\n"
                    "USB connection, or another app\n"
                    "using the camera."
                )
            )
            self.capture_button.state(["disabled"])

            messagebox.showerror(
                "Camera Error",
                "Kamera tidak dapat dibuka.\n\n"
                "Pastikan kamera tidak sedang digunakan "
                "oleh aplikasi lain."
            )
            return

        self.camera.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            CAMERA_WIDTH
        )
        self.camera.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            CAMERA_HEIGHT
        )

        self.running = True
        self.live_badge.config(
            text=" ● LIVE ",
            bg="#14532d",
            fg="#bbf7d0"
        )
        self.status_var.set(
            f"Ready • Capture key: {self.capture_key}"
        )

        self.update_frame()

    def update_frame(self):
        if not self.running or self.camera is None:
            return

        ok, frame = self.camera.read()

        if not ok:
            self.status_var.set(
                "Camera frame could not be read."
            )
            self.root.after(100, self.update_frame)
            return

        self.last_frame = frame.copy()

        frame_rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # Fit inside the LEFT panel while preserving aspect ratio.
        target_w = max(
            self.video_label.winfo_width(),
            PREVIEW_WIDTH
        )
        target_h = max(
            self.video_label.winfo_height(),
            PREVIEW_HEIGHT
        )

        scale = min(
            target_w / frame_rgb.shape[1],
            target_h / frame_rgb.shape[0]
        )

        # Do not enlarge a frame beyond its natural size.
        scale = min(scale, 1.0)

        new_w = max(
            1,
            int(frame_rgb.shape[1] * scale)
        )
        new_h = max(
            1,
            int(frame_rgb.shape[0] * scale)
        )

        resized = cv2.resize(
            frame_rgb,
            (new_w, new_h),
            interpolation=cv2.INTER_AREA
        )

        image = Image.fromarray(resized)
        self.photo = ImageTk.PhotoImage(image=image)

        self.video_label.configure(
            image=self.photo,
            text=""
        )

        self.root.after(20, self.update_frame)

    # --------------------------------------------------------
    # Capture
    # --------------------------------------------------------
    def capture_image(self):
        if not self.running or self.last_frame is None:
            self.status_var.set(
                "Capture failed: camera frame unavailable."
            )
            return

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S_%f"
        )[:-3]

        filename = (
            CAPTURE_DIR /
            f"capture_{timestamp}.jpg"
        )

        success = cv2.imwrite(
            str(filename),
            self.last_frame,
            [cv2.IMWRITE_JPEG_QUALITY, 95]
        )

        if not success:
            self.status_var.set(
                "ERROR: Image could not be saved."
            )
            return

        if not filename.exists() or filename.stat().st_size <= 0:
            self.status_var.set(
                "ERROR: Capture file is empty."
            )
            return

        self.capture_count += 1
        self.counter_var.set(
            f"{self.capture_count} "
            f"{'photo' if self.capture_count == 1 else 'photos'}"
        )
        self.status_var.set(
            f"Saved successfully: {filename.name}"
        )

        # Short visual feedback.
        self.capture_button.state(["disabled"])
        self.root.after(
            180,
            lambda: self.capture_button.state(["!disabled"])
        )

    # --------------------------------------------------------
    # Cleanup
    # --------------------------------------------------------
    def close_app(self, _event=None):
        if not self.running and self.camera is None:
            self.root.destroy()
            return

        self.running = False

        if self.camera is not None:
            self.camera.release()
            self.camera = None

        self.photo = None

        try:
            cv2.destroyAllWindows()
        except Exception:
            pass

        self.root.destroy()


def main():
    root = tk.Tk()
    CameraApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()