import cv2
import mediapipe as mp


import os
import sys
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from xarm.wrapper import XArmAPI
#Config robot
#######################################################
"""
Just for test example
"""
if len(sys.argv) >= 2:
    ip = sys.argv[1]
else:
    try:
        from configparser import ConfigParser
        parser = ConfigParser()
        parser.read('../robot.conf')
        ip = parser.get('xArm', 'ip')
    except:
        ip = input('Please input the xArm ip address:')
        if not ip:
            print('input error, exit')
            sys.exit(1)
########################################################

def hangle_err_warn_changed(item):
    print('ErrorCode: {}, WarnCode: {}'.format(item['error_code'], item['warn_code']))
    # TODO：Do different processing according to the error code


arm = XArmAPI(ip, do_not_open=True)
arm.register_error_warn_changed_callback(hangle_err_warn_changed)
arm.connect()

# enable motion
arm.motion_enable(enable=True)
# set mode: position control mode
arm.set_mode(0)
# set state: sport state
arm.set_state(state=0)



#Config camara
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    static_image_mode = False,
    max_num_hands = 1,
    min_detection_confidence = 0.7) as hands:
    
    while True:
        ret, frame = cap.read()
        #Obtain the dimension of the video
        height, width, _ = frame.shape
        if ret == False:
            break
            
        height, width, _ = frame.shape
        frame = cv2.flip(frame,1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)
        
        if results.multi_hand_landmarks is not None:
        
            for num, hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS, 
                       mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                       mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),)
                distance =(hand.landmark[mp_hands.HandLandmark.THUMB_TIP].x)-(hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x)
                distance_y =(hand.landmark[mp_hands.HandLandmark.THUMB_TIP].y)-(hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y)                
                if distance > 0.1 and distance_y < abs(0.1):
                    print("abrir")
                    arm.set_cgpio_digital(5, 0, delay_sec=0)
                elif distance < 0.05 and distance > 0 and distance_y < abs(0.1):
                    print("cerrar")
                    arm.set_cgpio_digital(5, 1, delay_sec=0)
                else:
                    print("nada")
                    
                #vertical movement
                palma_y = hand.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y
                if palma_y > 0.7:
                    arm.set_position(z=-10, relative=True, wait=True)
                elif palma_y < 0.3:
                    arm.set_position(z=10, relative=True, wait=True)
                else:
                    print("no movement")
                    
                #lateral movement
                palma_x = hand.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x
                if palma_x > 0.7:
                    arm.set_position(y=10, relative=True, wait=True)
                elif palma_x < 0.3:
                    arm.set_position(y=-10, relative=True, wait=True)
                else:
                    print("no movement")
         
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
time.sleep(5)
arm.disconnect()          
cap.release()
cv2.destroyAllWindows()
