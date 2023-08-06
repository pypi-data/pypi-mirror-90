import cv2
import numpy as np
import math
from .gaze_detection import GazeTracking
from .facial_landmark_detection import get_face_detector, find_faces
from .facial_landmark_detection import get_facial_landmark_model, find_facial_landmarks

# These values, and head pose estimation calculations are from here:
# https://www.learnopencv.com/head-pose-estimation-using-opencv-and-dlib/
MODEL_POINTS = np.array([
                            (0.0, 0.0, 0.0),             # Nose tip
                            (0.0, -330.0, -65.0),        # Chin
                            (-225.0, 170.0, -135.0),     # Left eye left corner
                            (225.0, 170.0, -135.0),      # Right eye right corne
                            (-150.0, -150.0, -125.0),    # Left Mouth corner
                            (150.0, -150.0, -125.0)      # Right mouth corner
                        ])

class Head:
    def __init__(self, frame, tracker_name):
        if tracker_name == 'BOOSTING':
            self.tracker = cv2.TrackerBoosting_create()
        elif tracker_name == 'MIL':
            self.tracker = cv2.TrackerMIL_create()
        elif tracker_name == 'KCF':
            self.tracker = cv2.TrackerKCF_create()
        elif tracker_name == 'TLD':
            self.tracker = cv2.TrackerTLD_create()
        elif tracker_name == 'MEDIANFLOW':
            self.tracker = cv2.TrackerMedianFlow_create()
        elif tracker_name == 'GOTURN':
            self.tracker = cv2.TrackerGOTURN_create()
        elif tracker_name == 'MOSSE':
            self.tracker = cv2.TrackerMOSSE_create()
        elif tracker_name == "CSRT":
            self.tracker = cv2.TrackerCSRT_create()

        self.face_model = get_face_detector()
        self.landmark_model = get_facial_landmark_model()
        self.gaze = GazeTracking()

        # Camera internals
        self.size = frame.shape
        focal_length = self.size[1]
        center = (self.size[1]/2, self.size[0]/2)
        self.camera_matrix = np.array(
                                [[focal_length, 0, center[0]],
                                [0, focal_length, center[1]],
                                [0, 0, 1]], dtype = "double"
                                )
        self.dist_coeffs = np.zeros((4,1)) # Assuming no lens distortion
        self.face = None
        self.tracking = False

    def _detect_face(self, frame):
        faces = find_faces(frame, self.face_model)
        if len(faces) > 0: 
            self.face = faces[0] # TODO select the middle one
            self.facial_landmarks = find_facial_landmarks(frame, self.landmark_model, self.face)
            self.image_points = np.array([
                                    self.facial_landmarks[30],     # Nose tip
                                    self.facial_landmarks[8],      # Chin
                                    self.facial_landmarks[36],     # Left eye left corner
                                    self.facial_landmarks[45],     # Right eye right corne
                                    self.facial_landmarks[48],     # Left Mouth corner
                                    self.facial_landmarks[54],     # Right mouth corner
                                ], dtype="double")
            return True
        else:
            return False

    def start_tracking(self, frame):
        # face is correct only if
        # get_location_and_pointing_direction
        # is called before
        # (and face was found TODO?)

        # try detecting face if not found already
        if self.face is None:
            self._detect_face(frame)

        if self.face is not None: # TODO face might be old form other frame!
            self.tracking = True
            # bound the face horizontally between the eyebrows
            # and vertically between eyebrows and chin
            self.bbox =(
                    int(self.facial_landmarks[17][0]),
                    int(self.facial_landmarks[17][1]),
                    int(self.facial_landmarks[26][0])-int(self.facial_landmarks[17][0]),
                    int(self.image_points[1][1])-int(self.facial_landmarks[17][1])
                )
            self.tracker.init(frame, self.bbox)
            return [self.bbox[0], self.bbox[1]]

    def track(self, frame):
        if not self.tracking:
            ret = self.start_tracking(frame)
            if ret is not None:
                return ret

        if self.face is None:
            print("tracking failed, face not initialized")
            return

        ok, self.bbox = self.tracker.update(frame)
        if ok:
            return [self.bbox[0], self.bbox[1]]
        else:
            ret = self.start_tracking(frame)
            if ret is not None:
                return ret
            else:
                print("tracking failed, face not found")

    def get_location_and_pointing_direction(self, frame):
        self.tracking = False
        face_detected = self._detect_face(frame)
        if face_detected:
            (success, rotation_vector, translation_vector) = cv2.solvePnP(MODEL_POINTS, self.image_points, self.camera_matrix, self.dist_coeffs, flags=cv2.SOLVEPNP_UPNP) 
            (nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 1000.0)]), rotation_vector, translation_vector, self.camera_matrix, self.dist_coeffs)
            
            self.p1 = (int(self.image_points[0][0]), int(self.image_points[0][1]))
            self.p2 = (int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1]))

            self.dx = -(self.p2[0] - self.p1[0])
            self.dy = self.p2[1] - self.p1[1]
            return self.p1, self.dx, self.dy
        else:
            return None, None, None

    def get_gaze_values(self, frame):
        """Get gaze values in x and y directions
        
        This is a workaround as self.gaze.horizontal_ratio(), self.gaze.vertical_ratio()
        does not seem to work
        """
        # does not seem to work...
        self.gaze.refresh(frame)
        if self.gaze.pupils_located:
            gaze_x = (self.gaze.eye_left.pupil.x + self.gaze.eye_right.pupil.x) / 2
            gaze_y = (self.gaze.eye_left.pupil.y + self.gaze.eye_right.pupil.y) / 2
            return gaze_x, gaze_y
        else:
            return None, None

    def annotate_latest(self, frame, landmarks=False):
        if self.tracking:
            cv2.rectangle(
                        frame,
                        (int(self.bbox[0]), int(self.bbox[1])),
                        (int(self.bbox[0] + self.bbox[2]),
                        int(self.bbox[1] + self.bbox[3])),
                        (255,0,0),
                        2,
                        1
                    )
        elif self.face is not None:
            frame = self.gaze.annotated_frame(frame)

            if landmarks:
                for (x, y) in self.facial_landmarks:
                    cv2.circle(frame, (x, y), 4, (255, 255, 0), -1)

            for p in self.image_points:
                cv2.circle(frame, (int(p[0]), int(p[1])), 3, (0,0,255), -1)

            cv2.line(frame, self.p1, self.p2, (0, 255, 255), 2)
        
        frame = cv2.flip(frame, 1)

        # texts must be added after flipping
        if not self.tracking:
            try:
                m = self.dy/self.dx
                ang1 = int(math.degrees(math.atan(m)))
            except:
                ang1 = 90
            cv2.putText(frame, str(ang1), (self.size[0] - self.p1[0], self.p1[1]), cv2.FONT_HERSHEY_SIMPLEX, 2, (128, 255, 255), 3)
        
        return frame