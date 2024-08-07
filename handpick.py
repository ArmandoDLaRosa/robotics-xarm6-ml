import cv2
import mediapipe as mp
from xarm.wrapper import XArmAPI

# Initialize MediaPipe Hands
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Connect to xArm6
arm = XArmAPI('192.168.1.203')  # Replace with your xArm's IP address
arm.motion_enable(enable=True)
arm.set_mode(0)
arm.set_state(state=0)

# Function to determine the pointing direction of the index finger
def index_finger_pointing_direction(hand_landmarks):
    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    index_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]

    # Calculate vector from MCP to fingertip
    vector_x = index_finger_tip.x - index_finger_mcp.x
    vector_y = index_finger_tip.y - index_finger_mcp.y  # Correct use of y-coordinate

    # Determine the horizontal direction based on the x-component of the vector
    if vector_x > 0.1:
        return 'right'
    elif vector_x < -0.1:
        return 'left'
    if vector_y < -0.1:
        return 'up'
    elif vector_y > 0.1:
        return 'down'
    return 'none'

def is_fist(hand_landmarks):
    landmarks = hand_landmarks.landmark
    wrist = landmarks[mp_hands.HandLandmark.WRIST]
    return sum((landmarks[i].y > wrist.y for i in [
        mp_hands.HandLandmark.THUMB_TIP,
        mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP])) >= 4

def is_peace_sign(hand_landmarks):
    landmarks = hand_landmarks.landmark
    wrist = landmarks[mp_hands.HandLandmark.WRIST]
    peace_sign = (
        #landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y > wrist.y and
        #landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y > wrist.y and
        #landmarks[mp_hands.HandLandmark.RING_FINGER_TIP].y < wrist.y and
        landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y > wrist.y
    )
    return peace_sign

def is_palm_open(hand_landmarks):
    landmarks = hand_landmarks.landmark
    return (landmarks[mp_hands.HandLandmark.PINKY_TIP].x - landmarks[mp_hands.HandLandmark.THUMB_TIP].x) > 0.75

# Setup video capture
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Process the video frame
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        # Draw hand landmarks
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                if is_fist(hand_landmarks):
                    arm.set_cgpio_digital(0, 1, delay_sec=0)  # Gripper close
                elif is_peace_sign(hand_landmarks):
                    arm.set_position(z=-50, relative=True, wait=True, speed=20)  # Move down on peace sign
                elif is_palm_open(hand_landmarks):
                    arm.set_cgpio_digital(0, 0, delay_sec=0)  # Gripper open
                else:
                    direction = index_finger_pointing_direction(hand_landmarks)
                    if direction == 'left':
                        arm.set_position(y=-50, relative=True, wait=True, speed=20)
                    elif direction == 'right':
                        arm.set_position(y=50, relative=True, wait=True, speed=20)
                    elif direction == 'up':
                        arm.set_position(z=50, relative=True, wait=True, speed=20)
                    elif direction == 'down':
                        arm.set_position(z=-50, relative=True, wait=True, speed=20)

        # Display the image
        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
arm.disconnect()