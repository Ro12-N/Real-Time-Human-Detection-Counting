import os
import threading
import time
from queue import Empty, Queue

import cv2
from PIL import Image
import customtkinter as ctk

from ui.theme import *
from ui.widgets import GlassCard, MetricBadge, AnimatedButton, StatusPill
from core.detector import DetectorAPI
from core.postprocessing import filter_and_draw_boxes
from core.counting import evaluate_crowd_density
from reports.plot_generator import generate_enumeration_plot, generate_accuracy_plot
from reports.pdf_generator import generate_pdf_report


class MainDashboard(ctk.CTkFrame):
    """Main operational dashboard with threaded detection and modern layout."""

    def __init__(self, master, on_show_results_callback, on_back_home_callback):
        super().__init__(master, fg_color=COLOR_BG_DARK)
        self.on_show_results_callback = on_show_results_callback
        self.on_back_home_callback = on_back_home_callback

        self.detector = None
        self.is_detecting = False
        self.input_mode = None
        self.selected_file_path = None
        self.cap = None

        self.counts_history = []
        self.accuracy_history = []
        self.timestamps_history = []
        self.total_frames = 0
        self.max_human_count = 0

        self._frame_image_ref = None
        self._ui_queue = Queue()

        self._build_layout()
        self._set_idle_state("Select image, video, or camera to begin.")

    def _build_layout(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_top_navbar()
        self._build_dashboard_body()

    def _build_top_navbar(self):
        top_bar = ctk.CTkFrame(self, fg_color=COLOR_BG_SURFACE, height=58, corner_radius=0)
        top_bar.grid(row=0, column=0, sticky="ew")
        top_bar.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            top_bar,
            text="Human Detection Dashboard",
            font=(FONT_FAMILY, 16, "bold"),
            text_color=COLOR_TEXT_PRIMARY
        ).grid(row=0, column=0, padx=(16, 10), pady=10, sticky="w")

        self.status_pill = StatusPill(top_bar, label="Idle", color=COLOR_TEXT_SECONDARY)
        self.status_pill.grid(row=0, column=1, sticky="w", padx=(4, 10))

        self.home_btn = AnimatedButton(
            top_bar,
            text="Splash",
            command=self.on_back_home_callback,
            primary=False,
            compact=True,
            width=96
        )
        self.home_btn.grid(row=0, column=2, padx=16, pady=10)

    def _build_dashboard_body(self):
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.grid(row=1, column=0, sticky="nsew", padx=16, pady=16)
        body.grid_columnconfigure(0, weight=2)
        body.grid_columnconfigure(1, weight=1)
        body.grid_rowconfigure(0, weight=1)

        # Main preview area
        left = ctk.CTkFrame(body, fg_color="transparent")
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        left.grid_columnconfigure(0, weight=1)
        left.grid_rowconfigure(2, weight=1)

        self.metrics_row = ctk.CTkFrame(left, fg_color="transparent")
        self.metrics_row.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        self.metrics_row.grid_columnconfigure((0, 1, 2), weight=1)

        self.badge_count = MetricBadge(self.metrics_row, title="Humans Detected", value="0", value_color=COLOR_SUCCESS)
        self.badge_count.grid(row=0, column=0, sticky="ew", padx=(0, 6))

        self.badge_fps = MetricBadge(self.metrics_row, title="Live FPS", value="0.0 FPS", value_color=COLOR_ACCENT_BLUE)
        self.badge_fps.grid(row=0, column=1, sticky="ew", padx=6)

        self.badge_status = MetricBadge(self.metrics_row, title="Detection State", value="Idle", value_color=COLOR_TEXT_SECONDARY)
        self.badge_status.grid(row=0, column=2, sticky="ew", padx=(6, 0))

        self.selection_hint = ctk.CTkLabel(
            left,
            text="No source selected",
            font=FONT_CAPTION,
            text_color=COLOR_WARNING,
            anchor="w"
        )
        self.selection_hint.grid(row=1, column=0, sticky="ew", pady=(0, 8))

        self.preview_card = GlassCard(left)
        self.preview_card.grid(row=2, column=0, sticky="nsew")
        self.preview_card.grid_rowconfigure(0, weight=1)
        self.preview_card.grid_columnconfigure(0, weight=1)

        self.display_label = ctk.CTkLabel(
            self.preview_card,
            text="Select an input source to preview frames.",
            font=FONT_BODY,
            text_color=COLOR_TEXT_SECONDARY,
            justify="center"
        )
        self.display_label.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)

        # Controls area
        right = GlassCard(body)
        right.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        right.grid_propagate(True)
        right.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(right, text="Input Source", font=FONT_CAPTION, text_color=COLOR_TEXT_MUTED).grid(row=0, column=0, sticky="w", padx=14, pady=(14, 6))

        self.btn_img = AnimatedButton(right, text="Select Image", command=self.select_image, primary=False)
        self.btn_img.grid(row=1, column=0, sticky="ew", padx=14, pady=4)

        self.btn_vid = AnimatedButton(right, text="Select Video", command=self.select_video, primary=False)
        self.btn_vid.grid(row=2, column=0, sticky="ew", padx=14, pady=4)

        self.btn_cam = AnimatedButton(right, text="Open Camera", command=self.select_camera, primary=False)
        self.btn_cam.grid(row=3, column=0, sticky="ew", padx=14, pady=4)

        ctk.CTkLabel(right, text="Detection Controls", font=FONT_CAPTION, text_color=COLOR_TEXT_MUTED).grid(row=4, column=0, sticky="w", padx=14, pady=(14, 6))

        self.btn_preview = AnimatedButton(right, text="Preview Source", command=self.preview_source, primary=False)
        self.btn_preview.grid(row=5, column=0, sticky="ew", padx=14, pady=4)

        self.btn_detect = AnimatedButton(right, text="Start Detection", command=self.start_detection, primary=True)
        self.btn_detect.configure(fg_color=COLOR_SUCCESS, hover_color="#16A34A")
        self.btn_detect.grid(row=6, column=0, sticky="ew", padx=14, pady=4)

        self.btn_stop = AnimatedButton(right, text="Stop Detection", command=self.stop_detection, primary=False)
        self.btn_stop.configure(fg_color="#3F1D24", hover_color="#5A1F2A", border_width=0)
        self.btn_stop.grid(row=7, column=0, sticky="ew", padx=14, pady=4)

        self.btn_results = AnimatedButton(right, text="View Analytics & PDF", command=self.open_analytics, primary=True)
        self.btn_results.grid(row=8, column=0, sticky="ew", padx=14, pady=(18, 10))

        self.state_message = ctk.CTkLabel(
            right,
            text="Status: waiting for source selection",
            text_color=COLOR_TEXT_SECONDARY,
            font=FONT_CAPTION,
            justify="left",
            wraplength=260
        )
        self.state_message.grid(row=9, column=0, sticky="ew", padx=14, pady=(0, 14))

    def _safe_ui(self, fn, *args, **kwargs):
        self._ui_queue.put((fn, args, kwargs))
        self.after(0, self._flush_ui_queue)

    def _flush_ui_queue(self):
        while True:
            try:
                fn, args, kwargs = self._ui_queue.get_nowait()
            except Empty:
                break
            fn(*args, **kwargs)

    def _set_idle_state(self, message):
        self.badge_status.update_value("Idle", COLOR_TEXT_SECONDARY)
        self.status_pill.update_status("Idle", COLOR_TEXT_SECONDARY)
        self.state_message.configure(text=f"Status: {message}")

    def _set_state(self, label, color, message=None):
        self.badge_status.update_value(label, color)
        self.status_pill.update_status(label, color)
        if message:
            self.state_message.configure(text=f"Status: {message}")

    def _set_source_selected(self, mode, path):
        label = f"{mode.upper()} selected"
        self.selection_hint.configure(text=label, text_color=COLOR_ACCENT_BLUE)
        if mode == "camera":
            readable = "Live camera"
        else:
            readable = os.path.basename(path)
        self._set_state("Ready", COLOR_ACCENT_BLUE, f"{mode.title()} source ready: {readable}")

    # Input Handlers
    def select_image(self):
        file_path = ctk.filedialog.askopenfilename(
            title="Select Image File",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")],
        )
        if file_path:
            self.input_mode = "image"
            self.selected_file_path = file_path
            self._set_source_selected("image", file_path)
            self.preview_source()

    def select_video(self):
        file_path = ctk.filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv")],
        )
        if file_path:
            self.input_mode = "video"
            self.selected_file_path = file_path
            self._set_source_selected("video", file_path)
            self.preview_source()

    def select_camera(self):
        self.input_mode = "camera"
        self.selected_file_path = 0
        self._set_source_selected("camera", "camera")
        self.preview_source()

    def preview_source(self):
        if not self.input_mode:
            self._set_state("Idle", COLOR_WARNING, "No input selected. Choose image, video, or camera first.")
            self.selection_hint.configure(text="No source selected", text_color=COLOR_WARNING)
            return

        if self.input_mode == "image" and self.selected_file_path:
            frame = cv2.imread(self.selected_file_path)
            self._render_frame(frame)
            self._set_state("Preview", COLOR_ACCENT_BLUE, "Image preview rendered.")
        elif self.input_mode in ["video", "camera"]:
            cap = cv2.VideoCapture(self.selected_file_path)
            ret, frame = cap.read()
            if ret:
                self._render_frame(frame)
                self._set_state("Preview", COLOR_ACCENT_BLUE, "Source preview rendered.")
            else:
                self._set_state("Error", COLOR_DANGER, "Unable to read from selected source.")
            cap.release()

    # Detection Loop
    def start_detection(self):
        if not self.input_mode:
            self._set_state("Blocked", COLOR_WARNING, "Select a source before starting detection.")
            return
        if self.is_detecting:
            return

        self.is_detecting = True
        self._set_state("Loading", COLOR_WARNING, "Loading model and starting detection thread...")

        self.counts_history.clear()
        self.accuracy_history.clear()
        self.timestamps_history.clear()
        self.total_frames = 0
        self.max_human_count = 0
        self.badge_count.update_value("0")
        self.badge_fps.update_value("0.0 FPS")

        threading.Thread(target=self._run_detection_thread, daemon=True).start()

    def stop_detection(self):
        self.is_detecting = False
        self._set_state("Stopped", COLOR_DANGER, "Detection stop requested.")

    def _run_detection_thread(self):
        try:
            if self.detector is None:
                self.detector = DetectorAPI()

            self._safe_ui(self._set_state, "Running", COLOR_SUCCESS, "Detection in progress...")
            start_time_global = time.time()

            if self.input_mode == "image":
                frame = cv2.imread(self.selected_file_path)
                if frame is not None:
                    boxes, scores, classes, num = self.detector.processFrame(frame)
                    annotated, count, avg_acc = filter_and_draw_boxes(frame, boxes, scores, classes, num, threshold=0.3)

                    self.max_human_count = count
                    self.counts_history.append(count)
                    self.accuracy_history.append(avg_acc)
                    self.timestamps_history.append(0.0)
                    self.total_frames = 1

                    self._safe_ui(self._render_frame, annotated)
                    self._safe_ui(self.badge_count.update_value, count)
                    self._safe_ui(self.badge_fps.update_value, "STATIC IMG")
                    self._safe_ui(self._set_state, "Finished", COLOR_SUCCESS, "Image detection complete.")
                self.is_detecting = False
                return

            self.cap = cv2.VideoCapture(self.selected_file_path)

            while self.is_detecting and self.cap.isOpened():
                t1 = time.time()
                ret, frame = self.cap.read()
                if not ret:
                    break

                boxes, scores, classes, num = self.detector.processFrame(frame)
                annotated, count, avg_acc = filter_and_draw_boxes(frame, boxes, scores, classes, num, threshold=0.3)

                t2 = time.time()
                fps = 1.0 / (t2 - t1) if (t2 - t1) > 0 else 0.0

                self.total_frames += 1
                if count > self.max_human_count:
                    self.max_human_count = count

                self.counts_history.append(count)
                self.accuracy_history.append(avg_acc)
                self.timestamps_history.append(round(t2 - start_time_global, 2))

                self._safe_ui(self._render_frame, annotated)
                self._safe_ui(self.badge_count.update_value, count)
                self._safe_ui(self.badge_fps.update_value, f"{fps:.1f} FPS")

            self.is_detecting = False
            if self.cap:
                self.cap.release()
            self._safe_ui(self._set_state, "Completed", COLOR_SUCCESS, "Detection run completed.")
        except Exception as exc:
            self.is_detecting = False
            if self.cap:
                self.cap.release()
            self._safe_ui(self._set_state, "Error", COLOR_DANGER, f"Detection failed: {exc}")

    def _render_frame(self, bgr_frame):
        if bgr_frame is None:
            return

        rgb_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
        h, w, _ = rgb_frame.shape

        target_w = max(self.preview_card.winfo_width() - 24, 320)
        target_h = max(self.preview_card.winfo_height() - 24, 240)

        scale = min(target_w / w, target_h / h)
        nw, nh = int(w * scale), int(h * scale)

        img = Image.fromarray(rgb_frame).resize((nw, nh), Image.Resampling.LANCZOS)
        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(nw, nh))

        self._frame_image_ref = ctk_img
        self.display_label.configure(image=ctk_img, text="")

    def open_analytics(self):
        """Compile plots, generate PDF report, and show results screen."""
        if not self.counts_history:
            self.counts_history = [0]
            self.accuracy_history = [0.0]
            self.timestamps_history = [0.0]
            self.total_frames = 1

        enum_path = generate_enumeration_plot(self.counts_history, self.timestamps_history, "enumeration_plot.png")
        acc_path = generate_accuracy_plot(self.accuracy_history, self.timestamps_history, "accuracy_plot.png")

        avg_c = sum(self.counts_history) / len(self.counts_history)
        avg_a = sum(self.accuracy_history) / len(self.accuracy_history)
        status_text, status_color = evaluate_crowd_density(self.max_human_count)

        generate_pdf_report(
            max_count=self.max_human_count,
            avg_count=avg_c,
            avg_accuracy=avg_a,
            total_frames=self.total_frames,
            crowd_status=status_text,
            enum_plot_path=enum_path,
            acc_plot_path=acc_path,
            output_path="Crowd_Report.pdf",
        )

        self.on_show_results_callback(enum_path, acc_path, self.max_human_count, avg_c, avg_a, status_text, status_color)
