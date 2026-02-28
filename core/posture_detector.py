"""
Main posture detector class that orchestrates all components.
"""
import cv2
import mediapipe as mp
import logging
from collections import deque

from config import MEDIAPIPE_CONFIG, POSTURE_THRESHOLDS, SMOOTHING_CONFIG, WARNING_CONFIG, COLORS
from core.landmark_processor import LandmarkProcessor
from core.posture_classifier import PostureClassifier
from core.visualizer import PostureVisualizer

logger = logging.getLogger(__name__)


class PostureDetector:
    """Main class for detecting and analyzing posture from video frames."""
    
    def __init__(self):
        """Initialize the posture detector with all components."""
        # Enhanced MediaPipe configuration
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(**MEDIAPIPE_CONFIG)
        
        # Thresholds
        self.neck_angle_threshold = POSTURE_THRESHOLDS['neck_angle']
        self.torso_angle_threshold = POSTURE_THRESHOLDS['torso_angle']
        self.alignment_threshold = POSTURE_THRESHOLDS['alignment']
        self.confidence_threshold = POSTURE_THRESHOLDS['confidence']
        
        # Smoothing with weighted history
        self.angle_history = deque(maxlen=SMOOTHING_CONFIG['angle_history_maxlen'])
        self.posture_history = deque(maxlen=SMOOTHING_CONFIG['posture_history_maxlen'])
        self.landmark_confidence_history = deque(maxlen=SMOOTHING_CONFIG['landmark_confidence_history_maxlen'])
        
        # Counters
        self.good_frames = 0
        self.bad_frames = 0
        self.total_frames = 0
        
        # Initialize components
        self.landmark_processor = LandmarkProcessor(self.mp_pose)
        self.classifier = PostureClassifier(
            self.neck_angle_threshold,
            self.torso_angle_threshold,
            self.confidence_threshold
        )
        self.visualizer = PostureVisualizer(COLORS)
        
        # Warning configuration
        self.warning_duration = WARNING_CONFIG['bad_posture_duration']
    
    def send_warning(self, bad_time):
        """
        Send warning for prolonged bad posture.
        
        Args:
            bad_time: Duration of bad posture in seconds
        """
        logger.warning(f"Poor posture detected for {bad_time:.1f} seconds!")
    
    def process_frame(self, image, fps):
        """
        Enhanced frame processing with better error handling.
        
        Args:
            image: Input frame from video
            fps: Frames per second of the video
            
        Returns:
            np.ndarray: Processed frame with visualizations
        """
        self.total_frames += 1
        h, w = image.shape[:2]
        
        # Convert to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        try:
            results = self.pose.process(rgb_image)
        except Exception as e:
            logger.error(f"MediaPipe error: {e}")
            return self.visualizer.draw_error_message(image, "Processing error")
        
        if not results.pose_landmarks:
            return self.visualizer.draw_error_message(image, "No pose detected")
        
        try:
            # Detect side and get landmarks with confidence
            landmarks_dict, side = self.landmark_processor.detect_side_preference(
                results, w, h, self.landmark_confidence_history
            )
            
            # Check overall pose confidence
            confidence = landmarks_dict.get('confidence', 0.0)
            low_confidence = confidence < self.confidence_threshold
            
            # Get shoulder and hip positions
            left_shoulder, right_shoulder = self.landmark_processor.get_shoulder_positions(results, w, h)
            left_hip, right_hip = self.landmark_processor.get_hip_positions(results, w, h)
            
            # Check alignment
            alignment_info = self.landmark_processor.check_alignment(
                left_shoulder, right_shoulder, self.alignment_threshold
            )
            
            # Calculate angles
            neck_angle = self.landmark_processor.calculate_neck_angle(
                landmarks_dict['shoulder'], landmarks_dict['ear']
            )
            
            torso_angle = self.landmark_processor.calculate_torso_angle_enhanced(
                left_hip, right_hip, left_shoulder, right_shoulder
            )
            
            # Classify posture with confidence consideration
            is_good_posture, low_confidence_flag = self.classifier.classify_posture(
                neck_angle, torso_angle, landmarks_dict, self.posture_history
            )
            
            # Update counters
            if is_good_posture and not low_confidence_flag:
                self.good_frames += 1
                self.bad_frames = 0
            elif not low_confidence_flag:
                self.bad_frames += 1
                self.good_frames = 0
            # Don't update counters during low confidence periods
            
            # Calculate times
            good_time = self.good_frames / fps if fps > 0 else 0
            bad_time = self.bad_frames / fps if fps > 0 else 0
            
            # Check for warnings (only when confidence is good)
            if bad_time > self.warning_duration and not low_confidence_flag:
                self.send_warning(bad_time)
            
            # Draw enhanced visualization
            image = self.visualizer.draw_visualization(
                image, landmarks_dict, side, neck_angle, torso_angle, 
                is_good_posture, alignment_info, low_confidence_flag
            )
            
            # Display time information
            image = self.visualizer.draw_time_info(image, good_time, bad_time, low_confidence_flag)
                
        except Exception as e:
            logger.error(f"Frame processing error: {e}")
            image = self.visualizer.draw_error_message(image, f"Error: {str(e)[:50]}")
        
        return image    