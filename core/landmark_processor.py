"""
Landmark processing and analysis for posture detection.
"""
from utils.math_utils import find_distance, find_angle


class LandmarkProcessor:
    """Handles processing and analysis of MediaPipe pose landmarks."""
    
    def __init__(self, mp_pose):
        """
        Initialize the landmark processor.
        
        Args:
            mp_pose: MediaPipe pose solution instance
        """
        self.mp_pose = mp_pose
        self.lmPose = mp_pose.PoseLandmark
    
    def calculate_landmark_confidence(self, landmarks, required_landmarks):
        """
        Calculate average confidence of required landmarks.
        
        Args:
            landmarks: MediaPipe landmarks result
            required_landmarks: List of landmark indices to check
            
        Returns:
            float: Average confidence (0.0-1.0)
        """
        lm = landmarks.pose_landmarks
        if not lm:
            return 0.0
            
        total_confidence = 0.0
        valid_landmarks = 0
        
        for landmark_idx in required_landmarks:
            if landmark_idx < len(lm.landmark):
                confidence = lm.landmark[landmark_idx].visibility
                total_confidence += confidence
                valid_landmarks += 1
        
        return total_confidence / valid_landmarks if valid_landmarks > 0 else 0.0
    
    def get_most_visible_side(self, landmarks, frame_width, frame_height):
        """
        Determine which side of the body is more visible and reliable.
        
        Args:
            landmarks: MediaPipe landmarks result
            frame_width: Width of the frame
            frame_height: Height of the frame
            
        Returns:
            tuple: (landmarks_dict, side) where side is 'left' or 'right'
        """
        lm = landmarks.pose_landmarks
        
        # Required landmarks for each side
        left_landmarks_indices = [
            self.lmPose.LEFT_SHOULDER, self.lmPose.LEFT_EAR, 
            self.lmPose.LEFT_HIP, self.lmPose.LEFT_EYE
        ]
        right_landmarks_indices = [
            self.lmPose.RIGHT_SHOULDER, self.lmPose.RIGHT_EAR, 
            self.lmPose.RIGHT_HIP, self.lmPose.RIGHT_EYE
        ]
        
        # Calculate confidence for each side
        left_confidence = self.calculate_landmark_confidence(landmarks, left_landmarks_indices)
        right_confidence = self.calculate_landmark_confidence(landmarks, right_landmarks_indices)
        
        # Get landmarks for the more confident side
        if left_confidence >= right_confidence:
            side = 'left'
            landmarks_dict = {
                'shoulder': (int(lm.landmark[self.lmPose.LEFT_SHOULDER].x * frame_width),
                            int(lm.landmark[self.lmPose.LEFT_SHOULDER].y * frame_height)),
                'ear': (int(lm.landmark[self.lmPose.LEFT_EAR].x * frame_width),
                       int(lm.landmark[self.lmPose.LEFT_EAR].y * frame_height)),
                'hip': (int(lm.landmark[self.lmPose.LEFT_HIP].x * frame_width),
                       int(lm.landmark[self.lmPose.LEFT_HIP].y * frame_height)),
                'confidence': left_confidence
            }
        else:
            side = 'right'
            landmarks_dict = {
                'shoulder': (int(lm.landmark[self.lmPose.RIGHT_SHOULDER].x * frame_width),
                            int(lm.landmark[self.lmPose.RIGHT_SHOULDER].y * frame_height)),
                'ear': (int(lm.landmark[self.lmPose.RIGHT_EAR].x * frame_width),
                       int(lm.landmark[self.lmPose.RIGHT_EAR].y * frame_height)),
                'hip': (int(lm.landmark[self.lmPose.RIGHT_HIP].x * frame_width),
                       int(lm.landmark[self.lmPose.RIGHT_HIP].y * frame_height)),
                'confidence': right_confidence
            }
        
        return landmarks_dict, side
    
    def detect_side_preference(self, landmarks, frame_width, frame_height, confidence_history):
        """
        Enhanced side detection with confidence checking.
        
        Args:
            landmarks: MediaPipe landmarks result
            frame_width: Width of the frame
            frame_height: Height of the frame
            confidence_history: Deque to store confidence history
            
        Returns:
            tuple: (landmarks_dict, side)
        """
        lm = landmarks.pose_landmarks
        
        # Calculate overall pose confidence
        required_landmarks = [
            self.lmPose.LEFT_SHOULDER, self.lmPose.RIGHT_SHOULDER,
            self.lmPose.LEFT_HIP, self.lmPose.RIGHT_HIP,
            self.lmPose.LEFT_EAR, self.lmPose.RIGHT_EAR
        ]
        
        pose_confidence = self.calculate_landmark_confidence(landmarks, required_landmarks)
        confidence_history.append(pose_confidence)
        
        # Use the most visible side
        landmarks_dict, side = self.get_most_visible_side(landmarks, frame_width, frame_height)
        
        return landmarks_dict, side
    
    def get_shoulder_positions(self, landmarks, frame_width, frame_height):
        """
        Get left and right shoulder positions.
        
        Args:
            landmarks: MediaPipe landmarks result
            frame_width: Width of the frame
            frame_height: Height of the frame
            
        Returns:
            tuple: (left_shoulder, right_shoulder) as (x, y) tuples
        """
        lm = landmarks.pose_landmarks
        
        left_shoulder = (int(lm.landmark[self.lmPose.LEFT_SHOULDER].x * frame_width),
                        int(lm.landmark[self.lmPose.LEFT_SHOULDER].y * frame_height))
        right_shoulder = (int(lm.landmark[self.lmPose.RIGHT_SHOULDER].x * frame_width),
                         int(lm.landmark[self.lmPose.RIGHT_SHOULDER].y * frame_height))
        
        return left_shoulder, right_shoulder
    
    def get_hip_positions(self, landmarks, frame_width, frame_height):
        """
        Get left and right hip positions.
        
        Args:
            landmarks: MediaPipe landmarks result
            frame_width: Width of the frame
            frame_height: Height of the frame
            
        Returns:
            tuple: (left_hip, right_hip) as (x, y) tuples
        """
        lm = landmarks.pose_landmarks
        
        left_hip = (int(lm.landmark[self.lmPose.LEFT_HIP].x * frame_width),
                   int(lm.landmark[self.lmPose.LEFT_HIP].y * frame_height))
        right_hip = (int(lm.landmark[self.lmPose.RIGHT_HIP].x * frame_width),
                    int(lm.landmark[self.lmPose.RIGHT_HIP].y * frame_height))
        
        return left_hip, right_hip
    
    def check_alignment(self, left_shoulder, right_shoulder, threshold):
        """
        Enhanced alignment check with vertical component.
        
        Args:
            left_shoulder: (x, y) tuple for left shoulder
            right_shoulder: (x, y) tuple for right shoulder
            threshold: Alignment threshold value
            
        Returns:
            tuple: (is_aligned, alignment_score)
        """
        horizontal_offset = find_distance(left_shoulder[0], left_shoulder[1], 
                                        right_shoulder[0], right_shoulder[1])
        
        # Also check vertical alignment (shoulders should be roughly at same height)
        vertical_diff = abs(left_shoulder[1] - right_shoulder[1])
        
        # Combined alignment score (weighted)
        alignment_score = horizontal_offset * 0.7 + vertical_diff * 0.3
        is_aligned = alignment_score < threshold
        
        return is_aligned, alignment_score
    
    def calculate_neck_angle(self, shoulder, ear):
        """
        Calculate neck angle.
        
        Args:
            shoulder: (x, y) tuple for shoulder position
            ear: (x, y) tuple for ear position
            
        Returns:
            float: Neck angle in degrees
        """
        return find_angle(shoulder[0], shoulder[1], ear[0], ear[1])
    
    def calculate_torso_angle_enhanced(self, left_hip, right_hip, left_shoulder, right_shoulder):
        """
        Enhanced torso angle calculation using both sides.
        
        Args:
            left_hip: (x, y) tuple for left hip
            right_hip: (x, y) tuple for right hip
            left_shoulder: (x, y) tuple for left shoulder
            right_shoulder: (x, y) tuple for right shoulder
            
        Returns:
            float: Torso angle in degrees
        """
        # Calculate midpoints for more stable measurement
        hip_mid_x = (left_hip[0] + right_hip[0]) / 2
        hip_mid_y = (left_hip[1] + right_hip[1]) / 2
        shoulder_mid_x = (left_shoulder[0] + right_shoulder[0]) / 2
        shoulder_mid_y = (left_shoulder[1] + right_shoulder[1]) / 2
        
        # Calculate angle using midpoints
        torso_angle = find_angle(hip_mid_x, hip_mid_y, shoulder_mid_x, shoulder_mid_y)
        
        return torso_angle
