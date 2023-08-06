import cv2
import mouse
import keyboard
from .head import Head
from screeninfo import get_monitors
from time import time

if __name__ == "__main__":
    controllers = ["loc", "track", "pointing", "gaze"]
    trackers = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    DEBUG = True
    CONTROLLER = controllers[2]
    TRACKER = trackers[2]
    FOCUS_KEY = "left ctrl"

    FOCUS_MULTIPLIERS = [2.0, 2.0]

    # for low pass filter:
    ALPHA = 0.3
    ALPHA_FOCUS = 0.5

    # in ratio, [loc[0]/frame_size[0], loc[1]/frame_size[1]]
    LOC_LIMITS = [0.5, 0.5] # TODO make work
    # in pixels, [dx, dy]
    POINTING_LIMITS = [300, 100]
    # in pixels, [[gaze_x left, gaze_x right], [gaze_y top, gaze_y bottom]]
    GAZE_LIMIT = [[21.5,15.0], [7.5,9]]

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    ok, frame = cap.read()
    if not ok:
        raise RuntimeError("Camera did not return frame")

    frame_size = frame.shape
    head = Head(frame, TRACKER)
    monitor = get_monitors()[0] # assume only one monitor
    monitor.center = [monitor.width/2, monitor.height/2]

    focus_start_loc = None
    prev_x = monitor.center[0]
    prev_y = monitor.center[1]

    def frame_loc_to_monitor_loc(loc): # TODO käytä
        x =  monitor.width - loc[0]/frame_size[0] * monitor.width
        y = loc[1]/frame_size[1] * monitor.height
        return x, y

    start_time = time()
    frame_count = 0
    while True:
        frame_count += 1
        if frame_count % 25 == 0:
            print(f"FPS: {frame_count / (time() - start_time)}")
            start_time = time()
            frame_count = 0

        ok, frame = cap.read()
        if ok == True:
            x = None
            y = None
            if focus_start_loc is None and keyboard.is_pressed(FOCUS_KEY):
                print("focus started")
                focus_start_loc = head.start_tracking(frame)
                start_x, start_y = frame_loc_to_monitor_loc(focus_start_loc)
            elif focus_start_loc is not None and not keyboard.is_pressed(FOCUS_KEY):
                print("focus ended")
                focus_start_loc = None

            if keyboard.is_pressed(FOCUS_KEY):
                loc = head.track(frame)
                if loc is not None:
                    x, y = frame_loc_to_monitor_loc(loc)
                    x = -(start_x - x) + prev_x
                    y = -(start_y - y) + prev_y
            else:
                if CONTROLLER == "gaze":
                    gaze_x, gaze_y = head.get_gaze_values(frame)
                    # y-value feels almost like a guess...
                    if gaze_x is not None and gaze_y is not None:
                        x = monitor.width - ((gaze_x - GAZE_LIMIT[0][1]) / (GAZE_LIMIT[0][0] - GAZE_LIMIT[0][1])) * monitor.width
                        y = ((gaze_y - GAZE_LIMIT[1][0]) / (GAZE_LIMIT[1][1] - GAZE_LIMIT[1][0])) * monitor.height
                elif CONTROLLER == "track": # TODO does not work in focus mode
                    loc = head.track(frame)
                    if loc is not None:
                        x, y = frame_loc_to_monitor_loc(loc)
                else:
                    loc, dx, dy = head.get_location_and_pointing_direction(frame)
                    if loc is not None:
                        if CONTROLLER == "loc":
                            x = monitor.width-loc[0]/frame_size[0]*monitor.width
                            y = loc[1]/frame_size[1]*monitor.height
                        elif CONTROLLER == "pointing":
                            x = (monitor.center[0] + dx/POINTING_LIMITS[0]*monitor.width)
                            y = (monitor.center[1] + dy/POINTING_LIMITS[1]*monitor.height)
                        else:
                            raise RuntimeError("Unknown controller")

            # move only if new coordinates
            if x is not None: # 'and y is not None' is assumed
                if not keyboard.is_pressed(FOCUS_KEY):
                    x = ALPHA*x + (1-ALPHA)*prev_x
                    y = ALPHA*y + (1-ALPHA)*prev_y
                else:
                    x = ALPHA_FOCUS*x + (1-ALPHA_FOCUS)*prev_x
                    y = ALPHA_FOCUS*y + (1-ALPHA_FOCUS)*prev_y
                mouse.move(x,y)
                prev_x = x
                prev_y = y

            if DEBUG:
                # TODO tracking printing?
                if CONTROLLER == "gaze":
                    print(
                        f"gaze_x:{None if gaze_x is None else round(gaze_x, 2)}, "
                        f"gaze_y:{None if gaze_y is None else round(gaze_y, 2)}"
                    )
                elif CONTROLLER != "track" and not keyboard.is_pressed(FOCUS_KEY):
                    print(f"loc:{loc} dx:{dx} dy:{dy}")
                cv2.imshow('frame', head.annotate_latest(frame, landmarks=True))
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        else:
            raise RuntimeError("Camera did not return frame")

    cv2.destroyAllWindows()
    cap.release()