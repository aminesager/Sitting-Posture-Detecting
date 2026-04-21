# Sitting Posture Detector

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

A real-time sitting posture detection application built with Python, using computer vision and machine learning to analyze and classify sitting posture from webcam or video feeds.

## Features

- **Real-time Posture Analysis**: Continuous monitoring of sitting posture using advanced pose estimation
- **Intelligent Classification**: Automatic detection of good vs. poor posture based on neck, torso, and alignment angles
- **Visual Feedback**: Live visualization with color-coded posture indicators and landmark overlays
- **Smoothing Algorithms**: Reduces false positives with historical data smoothing
- **Statistics Tracking**: Comprehensive posture statistics and session summaries
- **Flexible Input Sources**: Support for webcam, video files, and image sequences
- **User-Friendly GUI**: Intuitive Tkinter-based interface for easy operation
- **Configurable Thresholds**: Customizable posture detection parameters
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Requirements

- Python 3.7 or higher
- Webcam or video input device
- Operating System: Windows, macOS, or Linux

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/aminesager/sitting-posture-detecting.git
   cd sitting-posture-detecting
   ```

2. **Create a virtual environment (recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

1. **Start the application:**

   ```bash
   python main.py
   ```

2. **Select input source:**
   - Use webcam (default)
   - Load video file via File menu
   - Configure settings in the Settings menu

3. **Monitor posture:**
   - Green overlay: Good posture
   - Red overlay: Poor posture
   - View real-time statistics in the status panel

### Configuration

Edit `config.py` to customize:

- MediaPipe pose detection parameters
- Posture classification thresholds
- UI appearance and behavior
- Smoothing and warning configurations

## Project Structure

```
sitting-posture-detecting/
├── main.py                 # Application entry point
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── core/                  # Core detection modules
│   ├── __init__.py
│   ├── landmark_processor.py  # MediaPipe landmark processing
│   ├── posture_classifier.py  # Posture classification logic
│   ├── posture_detector.py    # Main detector orchestration
│   └── visualizer.py          # Visualization and drawing
├── ui/                    # User interface
│   ├── __init__.py
│   └── posture_app.py     # Tkinter GUI application
└── utils/                 # Utility functions
    ├── __init__.py
    └── math_utils.py      # Mathematical helper functions
```

## How It Works

1. **Pose Estimation**: Uses MediaPipe's Pose solution to detect body landmarks from video frames
2. **Landmark Processing**: Extracts key points for neck, shoulders, hips, and spine
3. **Angle Calculation**: Computes neck inclination, torso lean, and spinal alignment angles
4. **Posture Classification**: Compares calculated angles against configurable thresholds
5. **Smoothing**: Applies temporal smoothing to reduce noise and false detections
6. **Visualization**: Renders posture feedback with color-coded overlays and statistics

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt  # If available

# Run tests
python -m pytest

# Format code
black .
isort .
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [MediaPipe](https://mediapipe.dev/) for pose estimation
- [OpenCV](https://opencv.org/) for computer vision utilities
- [NumPy](https://numpy.org/) for numerical computations
- [Pillow](https://python-pillow.org/) for image processing

## Support

If you find this project helpful, please give it a ⭐️!

For issues and questions:

- Open an issue on GitHub
- Check the [Wiki](https://github.com/yourusername/sitting-posture-detecting/wiki) for documentation

---

**Disclaimer**: This application is for educational and informational purposes. Always consult healthcare professionals for posture-related concerns.</content>
<parameter name="filePath">/home/falcao/Documents/localRepos/Sitting-Posture-Detecting/README.md
