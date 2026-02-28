"""
Visualization module for drawing posture information on frames.
"""
import cv2


class PostureVisualizer:
    """Handles drawing posture information on video frames."""
    
    def __init__(self, colors):
        """
        Initialize the visualizer.
        
        Args:
            colors: Dictionary of color definitions
        """
        self.colors = colors
        self.font = cv2.FONT_HERSHEY_SIMPLEX
    
    def draw_visualization(self, image, landmarks_dict, side, neck_angle, 
                         torso_angle, is_good_posture, alignment_info, low_confidence):
        """
        Enhanced visualization with confidence indicators.
        
        Args:
            image: The frame to draw on
            landmarks_dict: Dictionary containing landmark positions and confidence
            side: Which side is being analyzed ('left' or 'right')
            neck_angle: Calculated neck angle
            torso_angle: Calculated torso angle
            is_good_posture: Boolean indicating posture quality
            alignment_info: Tuple of (is_aligned, alignment_score)
            low_confidence: Boolean indicating low confidence detection
            
        Returns:
            np.ndarray: Image with visualizations drawn
        """
        h, w = image.shape[:2]
        
        # Get landmark coordinates
        shoulder = landmarks_dict['shoulder']
        ear = landmarks_dict['ear']
        hip = landmarks_dict['hip']
        confidence = landmarks_dict.get('confidence', 1.0)
        
        # Choose color based on posture and confidence
        if low_confidence:
            color = self.colors['low_confidence']
            angle_color = self.colors['low_confidence']
            status_color = self.colors['warning']
        else:
            color = self.colors['light_green'] if is_good_posture else self.colors['bad']
            angle_color = self.colors['light_green'] if is_good_posture else self.colors['bad']
            status_color = color
        
        # Draw landmarks with confidence-based appearance
        landmark_size = 5 if low_confidence else 7
        landmark_color = self.colors['low_confidence'] if low_confidence else self.colors['landmarks']
        
        cv2.circle(image, shoulder, landmark_size, landmark_color, -1)
        cv2.circle(image, ear, landmark_size, landmark_color, -1)
        cv2.circle(image, hip, landmark_size, landmark_color, -1)
        
        # Draw reference points (100px above actual points)
        if not low_confidence:
            cv2.circle(image, (shoulder[0], shoulder[1] - 100), landmark_size, landmark_color, -1)
            cv2.circle(image, (hip[0], hip[1] - 100), landmark_size, landmark_color, -1)
            
            # Draw lines only when confidence is good
            cv2.line(image, shoulder, ear, color, 3)
            cv2.line(image, shoulder, (shoulder[0], shoulder[1] - 100), color, 3)
            cv2.line(image, hip, shoulder, color, 3)
            cv2.line(image, hip, (hip[0], hip[1] - 100), color, 3)
        
        # Display angles near landmarks
        if not low_confidence:
            cv2.putText(image, str(int(neck_angle)), (shoulder[0] + 10, shoulder[1]), 
                       self.font, 0.9, angle_color, 2)
            cv2.putText(image, str(int(torso_angle)), (hip[0] + 10, hip[1]), 
                       self.font, 0.9, angle_color, 2)
        
        # Main status text
        if low_confidence:
            status_text = "LOW CONFIDENCE"
        else:
            status_text = "GOOD POSTURE" if is_good_posture else "BAD POSTURE"
        
        cv2.putText(image, status_text, (10, 30), self.font, 0.9, status_color, 2)
        
        # Angle text string
        if not low_confidence:
            angle_text_string = f'Neck: {int(neck_angle)}°  Torso: {int(torso_angle)}°'
            cv2.putText(image, angle_text_string, (10, 60), self.font, 0.9, status_color, 2)
        
        # Confidence indicator
        confidence_text = f'Conf: {confidence:.2f}'
        confidence_color = self.colors['good'] if confidence > 0.7 else self.colors['warning'] if confidence > 0.5 else self.colors['bad']
        cv2.putText(image, confidence_text, (w - 120, 60), self.font, 0.7, confidence_color, 2)
        
        # Alignment status
        is_aligned, alignment_score = alignment_info
        if not low_confidence:
            alignment_text = f'Align: {int(alignment_score)}'
            alignment_color = self.colors['good'] if is_aligned else self.colors['bad']
            cv2.putText(image, alignment_text, (w - 120, 30), self.font, 0.7, alignment_color, 2)
        
        return image
    
    def draw_time_info(self, image, good_time, bad_time, low_confidence):
        """
        Draw time information on the frame.
        
        Args:
            image: The frame to draw on
            good_time: Time spent in good posture
            bad_time: Time spent in bad posture
            low_confidence: Boolean indicating low confidence detection
            
        Returns:
            np.ndarray: Image with time information drawn
        """
        h = image.shape[0]
        
        time_color = self.colors['low_confidence'] if low_confidence else self.colors['good'] if good_time > 0 else self.colors['bad']
        
        if good_time > 0 and not low_confidence:
            time_text = f'Good Posture Time: {good_time:.1f}s'
            cv2.putText(image, time_text, (10, h - 20), self.font, 0.9, time_color, 2)
        elif not low_confidence:
            time_text = f'Bad Posture Time: {bad_time:.1f}s'
            cv2.putText(image, time_text, (10, h - 20), self.font, 0.9, time_color, 2)
        else:
            time_text = 'Analyzing...'
            cv2.putText(image, time_text, (10, h - 20), self.font, 0.9, time_color, 2)
        
        return image
    
    def draw_error_message(self, image, message):
        """
        Draw an error message on the frame.
        
        Args:
            image: The frame to draw on
            message: Error message to display
            
        Returns:
            np.ndarray: Image with error message drawn
        """
        cv2.putText(image, message, (10, 30), self.font, 0.7, self.colors['warning'], 2)
        return image
