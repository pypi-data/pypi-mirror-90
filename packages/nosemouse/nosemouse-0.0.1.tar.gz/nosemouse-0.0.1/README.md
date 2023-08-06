# nosemouse

Work in progress!

## Setup

Python 3.8 was used for development.

Install required dependencies with `pip install -r requirements.txt`

Download `deploy.prototxt`, `opencv_face_detector.pbtxt`, 
`opencv_face_detector_uint8.pb` and `res10_300x300_ssd_iter_140000.caffemodel`
from https://github.com/vardanagarwal/Proctoring-AI/tree/master/models
to `models/face_model`,

also download `variables/` and `saved_model.pb` from: 
https://github.com/vardanagarwal/Proctoring-AI/tree/master/models/pose_model
to `models/facial_landmark_model` 

and download `shape_predictor_68_face_landmarks.dat` from:
https://github.com/antoinelame/GazeTracking/tree/master/gaze_tracking/trained_models
to `models/gaze_model`