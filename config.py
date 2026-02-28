# MediaPipe Configuration
MEDIAPIPE_CONFIG = {
    'static_image_mode': False,
    'model_complexity': 1,
    'enable_segmentation': False,
    'min_detection_confidence': 0.7,
    'min_tracking_confidence': 0.7
}

# Posture Thresholds
POSTURE_THRESHOLDS = {
    'neck_angle': 35,
    'torso_angle': 8,
    'alignment': 80,
    'confidence': 0.6
}

# Smoothing Configuration
SMOOTHING_CONFIG = {
    'angle_history_maxlen': 8,
    'posture_history_maxlen': 15,
    'landmark_confidence_history_maxlen': 5
}

# Warning Configuration
WARNING_CONFIG = {
    'bad_posture_duration': 180  # seconds
}

# Colors (BGR format for OpenCV)
COLORS = {
    'good': (127, 255, 0),
    'bad': (50, 50, 255),
    'warning': (0, 255, 255),
    'info': (255, 127, 0),
    'landmarks': (255, 255, 0),
    'light_green': (127, 233, 100),
    'pink': (255, 0, 255),
    'low_confidence': (128, 128, 128)
}

# Video Configuration
VIDEO_CONFIG = {
    'default_fps': 30,
    'frame_delay_ms': 15,
    'stats_update_interval': 5  # frames
}

# UI Configuration
UI_CONFIG = {
    'window_title': "Enhanced Posture Detection App",
    'window_geometry': "1200x800",
    'stats_text_height': 15,
    'stats_text_width': 30
}