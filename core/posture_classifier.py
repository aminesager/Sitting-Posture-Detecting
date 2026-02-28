"""
Posture classification logic.
"""


class PostureClassifier:
    """Classifies posture as good or bad based on angles and confidence."""
    
    def __init__(self, neck_threshold, torso_threshold, confidence_threshold):
        """
        Initialize the posture classifier.
        
        Args:
            neck_threshold: Maximum acceptable neck angle
            torso_threshold: Maximum acceptable torso angle
            confidence_threshold: Minimum required landmark confidence
        """
        self.neck_threshold = neck_threshold
        self.torso_threshold = torso_threshold
        self.confidence_threshold = confidence_threshold
        self.consecutive_low_confidence = 0
    
    def classify_posture(self, neck_angle, torso_angle, landmarks_dict, posture_history):
        """
        Enhanced posture classification with confidence consideration.
        
        Args:
            neck_angle: Calculated neck angle
            torso_angle: Calculated torso angle
            landmarks_dict: Dictionary containing landmark confidence
            posture_history: Deque storing posture history
            
        Returns:
            tuple: (is_good_posture, low_confidence)
        """
        # Check landmark confidence
        confidence = landmarks_dict.get('confidence', 1.0)
        low_confidence = confidence < self.confidence_threshold
        
        if low_confidence:
            self.consecutive_low_confidence += 1
            # If low confidence for too long, mark as bad posture
            if self.consecutive_low_confidence > 10:
                is_good_posture = False
            else:
                # Maintain previous posture during low confidence
                if len(posture_history) > 0:
                    is_good_posture = posture_history[-1]
                else:
                    is_good_posture = False
        else:
            self.consecutive_low_confidence = 0
            is_good_posture = (neck_angle < self.neck_threshold and 
                              torso_angle < self.torso_threshold)
        
        posture_history.append(is_good_posture)
        
        # Enhanced consensus with weighted recent frames
        if len(posture_history) >= 8:
            recent_frames = list(posture_history)[-8:]  # Last 8 frames
            # Give more weight to recent frames
            weighted_votes = sum(1 if posture else 0 for posture in recent_frames)
            final_posture = weighted_votes >= len(recent_frames) * 0.7
        else:
            final_posture = is_good_posture
            
        return final_posture, low_confidence
