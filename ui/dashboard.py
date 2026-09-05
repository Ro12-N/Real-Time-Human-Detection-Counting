import os
import time
import threading
import cv2
from PIL import Image, ImageTk
import customtkinter as ctk
from ui.theme import *
from ui.widgets import GlassCard, MetricBadge
from core.detector import DetectorAPI
from core.postprocessing import filter_and_draw_boxes
from core.counting import evaluate_crowd_density
from reports.plot_generator import generate_enumeration_plot, generate_accuracy_plot
from reports.pdf_generator import generate_pdf_report

class MainDashboard(ctk.CTkFrame):
    """Main Operational Dashboard View."""
    def __init__(self, master, on_show_results_callback, on_back_home_callback):
        super().__init__(master, fg_color=COLOR_BG_DARK)
        self.on_show_results_callback = on_show_results_callback
        self.on_back_home_callback = on_back_home_callback

        # State Variables
        self.detector = None
        self.is_detecting = False
        self.input_mode = None  # 'image', 'video', 'camera'
        self.selected_file_path = None
        self.cap = None

        # Analytics Accumulator Data
        self.counts_history = []
        self.accuracy_history = []
        self.timestamps_history = []
        self.total_frames = 0
        self.max_human_count = 0

        # Building UI Layout
        self._build_top_navbar()
        self._build_body_layout()

    def _build_top_navbar(self):
        self.top_bar = ctk.CTkFrame(self, fg_color=COLOR_CARD_BG, height=60, corner_radius=0)
        self.top_bar.pack(fill="x", side="top")

        self.logo_label = ctk.CTkLabel(
            self.top_bar,
            text="👁  REAL-TIME HUMAN DETECTION & COUNTING",
            font=(FONT_FAMILY, 15, "bold"),
            text_color=COLOR_TEXT_PRIMARY
        )
        self.logo_label.pack(side="left", padx=20)

        self.home_btn = ctk.CTkButton(
            self.top_bar,
            text="🏠 SPLASH SCREEN",
            font=(FONT_FAMILY, 12, "bold"),
            fg_color=COLOR_CARD_BORDER,
            hover_color=COLOR_ACCENT_PURPLE,
            width=140,
            command=self.on_back_home_callback
        )
        self.home_btn.pack(side="right", padx=20, pady=10)

    def _build_body_layout(self):
        self.body_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.body_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Left Control Panel Sidebar
        self.sidebar = GlassCard(self.body_frame, width=280)
        self.sidebar.pack(side="left", fill="y", padx=(0, 10))

        # INPUT SOURCE Section
        ctk.CTkLabel(self.sidebar, text="INPUT SOURCE", font=FONT_CAPTION, text_color=COLOR_TEXT_SECONDARY).pack(anchor="w", padx=15, pady=(15, 5))
        
        self.btn_img = ctk.CTkButton(self.sidebar, text="🖼  Select Image", fg_color=COLOR_CARD_BORDER, hover_color=COLOR_ACCENT_BLUE, command=self.select_image)
        self.btn_img.pack(fill="x", padx=15, pady=4)

        self.btn_vid = ctk.CTkButton(self.sidebar, text="🎬  Select Video", fg_color=COLOR_CARD_BORDER, hover_color=COLOR_ACCENT_BLUE, command=self.select_video)
        self.btn_vid.pack(fill="x", padx=15, pady=4)

        self.btn_cam = ctk.CTkButton(self.sidebar, text="📷  Open Camera", fg_color=COLOR_CARD_BORDER, hover_color=COLOR_ACCENT_BLUE, command=self.select_camera)
        self.btn_cam.pack(fill="x", padx=15, pady=4)

        # ACTIONS Section
        ctk.CTkLabel(self.sidebar, text="ACTIONS", font=FONT_CAPTION, text_color=COLOR_TEXT_SECONDARY).pack(anchor="w", padx=15, pady=(20, 5))
        
        self.btn_preview = ctk.CTkButton(self.sidebar, text="👁  Preview Stream", fg_color=COLOR_CARD_BORDER, hover_color=COLOR_ACCENT_PURPLE, command=self.preview_source)
        self.btn_preview.pack(fill="x", padx=15, pady=4)

        self.btn_detect = ctk.CTkButton(self.sidebar, text="🚀  START DETECTION", fg_color=COLOR_SUCCESS, hover_color="#059669", font=(FONT_FAMILY, 13, "bold"), command=self.start_detection)
        self.btn_detect.pack(fill="x", padx=15, pady=6)

        self.btn_stop = ctk.CTkButton(self.sidebar, text="⏹  Stop Detection", fg_color=COLOR_DANGER, hover_color="#DC2626", command=self.stop_detection)
        self.btn_stop.pack(fill="x", padx=15, pady=4)

        # REPORTS Section
        ctk.CTkLabel(self.sidebar, text="REPORTS & ANALYTICS", font=FONT_CAPTION, text_color=COLOR_TEXT_SECONDARY).pack(anchor="w", padx=15, pady=(20, 5))

        self.btn_results = ctk.CTkButton(self.sidebar, text="📈  View Analytics & PDF", fg_color=COLOR_ACCENT_PURPLE, hover_color=COLOR_ACCENT_BLUE, command=self.open_analytics)
        self.btn_results.pack(fill="x", padx=15, pady=4)

        # Right Main Workspace Canvas
        self.main_area = GlassCard(self.body_frame)
        self.main_area.pack(side="right", fill="both", expand=True)

        # Metrics Header Bar above Video Display
        self.metrics_bar = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.metrics_bar.pack(fill="x", padx=15, pady=10)

        self.badge_count = MetricBadge(self.metrics_bar, title="Humans Detected", value="0", value_color=COLOR_SUCCESS)
        self.badge_count.pack(side="left", padx=(0, 10))

        self.badge_fps = MetricBadge(self.metrics_bar, title="Live Performance", value="0.0 FPS", value_color=COLOR_ACCENT_BLUE)
        self.badge_fps.pack(side="left", padx=5)

        self.badge_status = MetricBadge(self.metrics_bar, title="System State", value="IDLE", value_color=COLOR_TEXT_SECONDARY)
        self.badge_status.pack(side="right", padx=(10, 0))

        # Central Video Canvas Container
        self.canvas_frame = ctk.CTkFrame(self.main_area, fg_color=COLOR_BG_DARK, corner_radius=12)
        self.canvas_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        self.display_label = ctk.CTkLabel(self.canvas_frame, text="[ Select an Image, Video, or Camera input source to begin ]", font=FONT_BODY, text_color=COLOR_TEXT_SECONDARY)
        self.display_label.pack(fill="both", expand=True)

    # Input Handlers
    def select_image(self):
        file_path = ctk.filedialog.askopenfilename(title="Select Image File", filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")])
        if file_path:
            self.input_mode = 'image'
            self.selected_file_path = file_path
            self.badge_status.update_value("IMAGE READY", COLOR_ACCENT_BLUE)
            self.preview_source()

    def select_video(self):
        file_path = ctk.filedialog.askopenfilename(title="Select Video File", filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv")])
        if file_path:
            self.input_mode = 'video'
            self.selected_file_path = file_path
            self.badge_status.update_value("VIDEO READY", COLOR_ACCENT_BLUE)
            self.preview_source()

    def select_camera(self):
        self.input_mode = 'camera'
        self.selected_file_path = 0
        self.badge_status.update_value("CAMERA READY", COLOR_ACCENT_BLUE)
        self.preview_source()

    def preview_source(self):
        if not self.input_mode:
            return
        if self.input_mode == 'image' and self.selected_file_path:
            frame = cv2.imread(self.selected_file_path)
            self._render_frame(frame)
        elif self.input_mode in ['video', 'camera']:
            cap = cv2.VideoCapture(self.selected_file_path)
            ret, frame = cap.read()
            if ret:
                self._render_frame(frame)
            cap.release()

    # Detection Loop
    def start_detection(self):
        if not self.input_mode:
            return
        if self.is_detecting:
            return

        self.is_detecting = True
        self.badge_status.update_value("LOADING MODEL...", COLOR_WARNING)
        
        # Reset Session Analytics Data
        self.counts_history.clear()
        self.accuracy_history.clear()
        self.timestamps_history.clear()
        self.total_frames = 0
        self.max_human_count = 0

        # Run Detection in Background Thread to Keep UI Responsive
        threading.Thread(target=self._run_detection_thread, daemon=True).start()

    def stop_detection(self):
        self.is_detecting = False
        self.badge_status.update_value("STOPPED", COLOR_DANGER)

    def _run_detection_thread(self):
        if self.detector is None:
            self.detector = DetectorAPI()

        self.badge_status.update_value("DETECTING...", COLOR_SUCCESS)
        start_time_global = time.time()

        if self.input_mode == 'image':
            frame = cv2.imread(self.selected_file_path)
            if frame is not None:
                boxes, scores, classes, num = self.detector.processFrame(frame)
                annotated, count, avg_acc = filter_and_draw_boxes(frame, boxes, scores, classes, num, threshold=0.3)
                
                self.max_human_count = count
                self.counts_history.append(count)
                self.accuracy_history.append(avg_acc)
                self.timestamps_history.append(0.0)
                self.total_frames = 1

                self._render_frame(annotated)
                self.badge_count.update_value(count)
                self.badge_fps.update_value("STATIC IMG")
                self.badge_status.update_value("FINISHED", COLOR_SUCCESS)
            self.is_detecting = False

        elif self.input_mode in ['video', 'camera']:
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

                self._render_frame(annotated)
                self.badge_count.update_value(count)
                self.badge_fps.update_value(f"{fps:.1f} FPS")

            if self.cap:
                self.cap.release()
            self.is_detecting = False
            self.badge_status.update_value("COMPLETED", COLOR_SUCCESS)

    def _render_frame(self, bgr_frame):
        if bgr_frame is None:
            return
        rgb_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
        h, w, _ = rgb_frame.shape
        
        # Scale to canvas size while preserving visual aspect ratio
        target_w, target_h = 720, 480
        scale = min(target_w / w, target_h / h)
        nw, nh = int(w * scale), int(h * scale)
        
        img = Image.fromarray(rgb_frame).resize((nw, nh), Image.Resampling.LANCZOS)
        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(nw, nh))
        
        self.display_label.configure(image=ctk_img, text="")

    def open_analytics(self):
        """Compile plots, generate PDF report, and show results screen."""
        if not self.counts_history:
            # Fallback data if user opens analytics before running detection
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
            output_path="Crowd_Report.pdf"
        )

        self.on_show_results_callback(enum_path, acc_path, self.max_human_count, avg_c, avg_a, status_text, status_color)
