"""
Main GUI application for posture detection.
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
import time
from PIL import Image, ImageTk
import threading

from config import VIDEO_CONFIG, UI_CONFIG
from core import PostureDetector


class PostureApp:
    """Main GUI application for posture detection."""
    
    def __init__(self, root):
        """
        Initialize the application.
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title(UI_CONFIG['window_title'])
        self.root.geometry(UI_CONFIG['window_geometry'])
        
        # Initialize detector
        self.detector = PostureDetector()
        
        # Video capture
        self.cap = None
        self.video_source = 0  # Default to webcam
        self.is_running = False
        self.fps = VIDEO_CONFIG['default_fps']
        self.delay = VIDEO_CONFIG['frame_delay_ms']
        
        # Statistics
        self.total_frames = 0
        self.good_frames = 0
        self.bad_frames = 0
        
        # Create UI
        self.create_widgets()
        
    def create_widgets(self):
        """Create all UI widgets."""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Video display
        self.video_label = ttk.Label(main_frame)
        self.video_label.grid(row=0, column=0, columnspan=3, sticky="nsew")
        
        # Controls frame
        controls_frame = ttk.Frame(main_frame)
        controls_frame.grid(row=1, column=0, columnspan=3, pady=10, sticky="ew")
        
        # Source selection
        ttk.Label(controls_frame, text="Video Source:").pack(side=tk.LEFT, padx=5)
        self.source_var = tk.StringVar(value="webcam")
        ttk.Radiobutton(controls_frame, text="Webcam", variable=self.source_var, 
                       value="webcam", command=self.update_source).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(controls_frame, text="File", variable=self.source_var, 
                       value="file", command=self.update_source).pack(side=tk.LEFT, padx=5)
        self.file_entry = ttk.Entry(controls_frame, width=40)
        self.file_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="Browse", command=self.browse_file).pack(side=tk.LEFT, padx=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=10, sticky="ew")
        
        self.start_button = ttk.Button(button_frame, text="Start", command=self.start_detection)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="Stop", command=self.stop_detection, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # Statistics frame
        stats_frame = ttk.LabelFrame(main_frame, text="Statistics")
        stats_frame.grid(row=0, column=3, rowspan=3, padx=10, pady=10, sticky="nsew")
        
        self.stats_text = tk.Text(
            stats_frame, 
            height=UI_CONFIG['stats_text_height'], 
            width=UI_CONFIG['stats_text_width']
        )
        self.stats_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
    def browse_file(self):
        """Open file dialog to select video file."""
        filename = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[("Video Files", "*.mp4 *.avi *.mov"), ("All Files", "*.*")]
        )
        if filename:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, filename)
            self.source_var.set("file")
    
    def update_source(self):
        """Update file entry state based on source selection."""
        if self.source_var.get() == "webcam":
            self.file_entry.config(state=tk.DISABLED)
        else:
            self.file_entry.config(state=tk.NORMAL)
    
    def start_detection(self):
        """Start posture detection."""
        if self.is_running:
            return
            
        source = self.source_var.get()
        if source == "webcam":
            self.video_source = 0
        else:
            file_path = self.file_entry.get()
            if not file_path:
                messagebox.showerror("Error", "Please select a video file")
                return
            self.video_source = file_path
        
        try:
            self.cap = cv2.VideoCapture(self.video_source)
            if not self.cap.isOpened():
                raise ValueError("Could not open video source")
            
            self.fps = int(self.cap.get(cv2.CAP_PROP_FPS)) or VIDEO_CONFIG['default_fps']
            self.is_running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            
            # Reset counters
            self.total_frames = 0
            self.good_frames = 0
            self.bad_frames = 0
            
            # Start video processing in a separate thread
            self.thread = threading.Thread(target=self.process_video, daemon=True)
            self.thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start video capture: {str(e)}")
            if self.cap:
                self.cap.release()
                self.cap = None
    
    def stop_detection(self):
        """Stop posture detection."""
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        
        if self.cap:
            self.cap.release()
            self.cap = None
        
        # Update statistics
        self.update_statistics()
    
    def process_video(self):
        """Process video frames in a separate thread."""
        while self.is_running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # Process frame
            processed_frame = self.detector.process_frame(frame, self.fps)
            
            # Update counters
            self.total_frames += 1
            if hasattr(self.detector, 'good_frames'):
                self.good_frames = self.detector.good_frames
                self.bad_frames = self.detector.bad_frames
            
            # Convert to RGB and display
            cv2image = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            
            # Update UI in main thread
            self.root.after(0, self.update_frame, imgtk)
            
            # Small delay to prevent UI freeze
            time.sleep(1/self.fps)
        
        # Video ended or stopped
        self.root.after(0, self.stop_detection)
    
    def update_frame(self, imgtk):
        """
        Update the displayed video frame.
        
        Args:
            imgtk: ImageTk photo image to display
        """
        if not self.is_running:
            return
            
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)
        
        # Update statistics periodically
        if self.total_frames % VIDEO_CONFIG['stats_update_interval'] == 0:
            self.update_statistics()
    
    def update_statistics(self):
        """Update the statistics display."""
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        
        if self.total_frames == 0:
            self.stats_text.insert(tk.END, "No data available")
            self.stats_text.config(state=tk.DISABLED)
            return
        
        total_time = self.total_frames / self.fps if self.fps > 0 else 0
        good_percentage = (self.good_frames / self.total_frames * 100) if self.total_frames > 0 else 0
        bad_percentage = (self.bad_frames / self.total_frames * 100) if self.total_frames > 0 else 0
        
        stats = [
            f"Total Frames: {self.total_frames}",
            f"Total Time: {total_time:.2f}s",
            f"Good Posture: {self.good_frames} ({good_percentage:.1f}%)",
            f"Bad Posture: {self.bad_frames} ({bad_percentage:.1f}%)",
            "\nEnhanced Thresholds:",
            f"Neck Angle: {self.detector.neck_angle_threshold}°",
            f"Torso Angle: {self.detector.torso_angle_threshold}°",
            f"Alignment: {self.detector.alignment_threshold}px",
            f"Confidence: {self.detector.confidence_threshold}",
            "\nFeatures:",
            "• Smart side selection",
            "• Confidence tracking",
            "• Enhanced angle calculation",
            "• Noise filtering"
        ]
        
        self.stats_text.insert(tk.END, "\n".join(stats))
        self.stats_text.config(state=tk.DISABLED)
    
    def on_closing(self):
        """Handle application closing."""
        self.stop_detection()
        self.root.destroy()
