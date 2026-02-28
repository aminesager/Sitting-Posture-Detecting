"""
Mathematical utility functions for posture detection.
"""
import math as m


def find_distance(x1, y1, x2, y2):
    """
    Calculate Euclidean distance between two points.
    
    Args:
        x1, y1: Coordinates of first point
        x2, y2: Coordinates of second point
        
    Returns:
        float: Euclidean distance
    """
    return m.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def find_angle(x1, y1, x2, y2, reference_vertical=True):
    """
    Calculate angle between two points with respect to vertical or horizontal axis.
    Enhanced with better angle calculation.
    
    Args:
        x1, y1: Coordinates of first point
        x2, y2: Coordinates of second point
        reference_vertical: If True, calculate from vertical axis, else from horizontal
        
    Returns:
        float: Angle in degrees (0-90)
    """
    if reference_vertical:
        # Calculate angle from vertical axis with improved formula
        dx = x2 - x1
        dy = y2 - y1
        
        # Handle division by zero and edge cases
        if abs(dy) < 0.001:
            return 90.0  # Perfectly horizontal
        
        angle_rad = m.atan2(abs(dx), abs(dy))
        degree = m.degrees(angle_rad)
        
        # Ensure angle is always positive and reasonable
        degree = min(90.0, max(0.0, degree))
    else:
        # Calculate angle from horizontal axis
        dx = x2 - x1
        dy = y2 - y1
        
        if abs(dx) < 0.001:
            return 90.0  # Perfectly vertical
            
        angle_rad = m.atan2(abs(dy), abs(dx))
        degree = m.degrees(angle_rad)
        degree = min(90.0, max(0.0, degree))
    
    return degree