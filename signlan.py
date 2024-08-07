import cv2
import mediapipe as mp
from xarm.wrapper import XArmAPI
from time import sleep

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Initialize the xArm6
arm = XArmAPI('192.168.1.206')  # Replace with your xArm's IP address
arm.motion_enable(enable=True)
arm.set_mode(0)
arm.set_state(state=0)

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Function to dynamically get current x and y positions
def get_current_position():
    status, position = arm.get_position(is_radian=False)
    if status == 0:
        print(f"Current position: X={position[0]}, Y={position[1]}")
        return position[0], position[1]
    else:
        print(f"Failed to get the current position. Status code: {status}")
        return None, None

# Drawing functions for each vowel
def move_arm_to_draw_A(start_x, start_y, letter_size=50):
    z_height = -43.3
    move_height = -40
    bottom_left = (start_x, start_y)
    top_middle = (start_x + letter_size / 2, start_y - letter_size)
    bottom_right = (start_x + letter_size, start_y)
    # Drawing sequence for 'A'
    arm.set_position(*bottom_left, move_height, speed=100, wait=True)
    arm.set_position(*bottom_left, z_height, speed=100, wait=True)
    arm.set_position(*top_middle, z_height, speed=100, wait=True)
    arm.set_position(*bottom_right, z_height, speed=100, wait=True)
    arm.set_position(*bottom_left, z_height, speed=100, wait=True)  # Draw base
    next_start_x = bottom_right[0] + 20
    arm.set_position(next_start_x, start_y, move_height, speed=100, wait=True)
    return next_start_x, start_y


def move_arm_to_draw_E(start_x, start_y, letter_size=50):
    # Set the height for drawing and moving
    z_height =  -44.3
    move_height = -40
    
    # Define the coordinates for the corners and midpoints of the letter 'E'
    top_left = (start_x, start_y - letter_size)
    bottom_left = (start_x, start_y)
    middle_left = (start_x, start_y - letter_size / 2)
    top_right = (start_x + letter_size, start_y - letter_size)
    middle_right = (start_x + letter_size, start_y - letter_size / 2)
    bottom_right = (start_x + letter_size, start_y)
    
    # Move arm to the top-left corner above the surface
    arm.set_position(*top_left, move_height, speed=100, wait=True)
    # Lower arm to start drawing
    arm.set_position(*top_left, z_height, speed=100, wait=True)
    # Draw top horizontal line of 'E'
    arm.set_position(*top_right, z_height, speed=100, wait=True)
    # Move back to the top-left corner
    arm.set_position(*top_left, z_height, speed=100, wait=True)
    # Draw vertical line from top-left to bottom-left
    arm.set_position(*bottom_left, z_height, speed=100, wait=True)
    # Draw middle horizontal line from left to right
    arm.set_position(*middle_left, z_height, speed=100, wait=True)
    arm.set_position(*middle_right, z_height, speed=100, wait=True)
    # Return to the middle-left position
    arm.set_position(*middle_left, z_height, speed=100, wait=True)
    # Draw vertical line to bottom-left corner
    arm.set_position(*bottom_left, z_height, speed=100, wait=True)
    # Draw bottom horizontal line from left to right
    arm.set_position(*bottom_right, z_height, speed=100, wait=True)
    
    # Calculate the starting point for the next character
    next_start_x = bottom_right[0] + 20
    # Move the arm to the new starting point above the surface
    arm.set_position(next_start_x, start_y, move_height, speed=100, wait=True)
    
    return next_start_x, start_y

def move_arm_to_draw_I(start_x, start_y, letter_size=50):
    z_height = -44.3
    move_height = -40
    
    # Define points for letter 'I'
    top_left = (start_x, start_y - letter_size)
    top_right = (start_x + letter_size, start_y - letter_size)
    bottom_left = (start_x, start_y)
    bottom_right = (start_x + letter_size, start_y)
    middle_top = (start_x + letter_size / 2, start_y - letter_size)
    middle_bottom = (start_x + letter_size / 2, start_y)
    
    # Move and draw top horizontal line
    arm.set_position(*top_left, move_height, speed=100, wait=True)
    arm.set_position(*top_left, z_height, speed=100, wait=True)
    arm.set_position(*top_right, z_height, speed=100, wait=True)
    
    # Move to the middle of the top horizontal line
    arm.set_position(*middle_top, move_height, speed=100, wait=True)
    # Draw vertical line
    arm.set_position(*middle_top, z_height, speed=100, wait=True)
    arm.set_position(*middle_bottom, z_height, speed=100, wait=True)
    
    # Move and draw bottom horizontal line
    arm.set_position(*bottom_left, move_height, speed=100, wait=True)
    arm.set_position(*bottom_left, z_height, speed=100, wait=True)
    arm.set_position(*bottom_right, z_height, speed=100, wait=True)
    
    # Calculate the starting point for the next character
    next_start_x = bottom_right[0] + 20
    arm.set_position(next_start_x, start_y, move_height, speed=100, wait=True)
    
    return next_start_x, start_y

def move_arm_to_draw_O(start_x, start_y, letter_size=50):
    z_height = -44.3
    move_height = -40
    # Define points for letter 'O'
    bottom_left = (start_x, start_y)
    bottom_right = (start_x + letter_size, start_y)
    top_right = (start_x + letter_size, start_y - letter_size)
    top_left = (start_x, start_y - letter_size)
    # Move and draw sequence
    arm.set_position(*bottom_left, move_height, speed=100, wait=True)
    arm.set_position(*bottom_left, z_height, speed=100, wait=True)
    arm.set_position(*bottom_right, z_height, speed=100, wait=True)
    arm.set_position(*top_right, z_height, speed=100, wait=True)
    arm.set_position(*top_left, z_height, speed=100, wait=True)
    arm.set_position(*bottom_left, z_height, speed=100, wait=True)  # Close the shape
    next_start_x = bottom_right[0] + 20
    arm.set_position(next_start_x, start_y, move_height, speed=100, wait=True)
    return next_start_x, start_y

def move_arm_to_draw_U(start_x, start_y, letter_size=50):
    z_height = -44.3
    move_height = -40
    # Define points for letter 'U'
    top_left = (start_x, start_y - letter_size)
    bottom_left = (start_x, start_y)
    bottom_right = (start_x + letter_size, start_y)
    top_right = (start_x + letter_size, start_y - letter_size)
    # Move and draw sequence
    arm.set_position(*top_left, move_height, speed=100, wait=True)
    arm.set_position(*top_left, z_height, speed=100, wait=True)
    arm.set_position(*bottom_left, z_height, speed=100, wait=True)
    arm.set_position(*bottom_right, z_height, speed=100, wait=True)
    arm.set_position(*top_right, z_height, speed=100, wait=True)
    next_start_x = bottom_right[0] + 20
    arm.set_position(next_start_x, start_y, move_height, speed=100, wait=True)
    return next_start_x, start_y

def move_arm_to_draw_vowel(letter, start_x, start_y):
    if letter == 'A':
        return move_arm_to_draw_A(start_x, start_y,letter_size=30)
    elif letter == 'E':
        return move_arm_to_draw_E(start_x, start_y,letter_size=30)
    elif letter == 'I':
        return move_arm_to_draw_I(start_x, start_y,letter_size=30)
    elif letter == 'O':
        return move_arm_to_draw_O(start_x, start_y,letter_size=30)
    elif letter == 'U':
        return move_arm_to_draw_U(start_x, start_y,letter_size=30)
    return start_x, start_y


def detect_vowel(hand_landmarks, mp_hands):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
    index_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]

    # Heuristic rules for each vowel based on the landmarks
    if thumb_tip.x < index_finger_tip.x and index_finger_tip.y < index_finger_mcp.y:
        return 'A'
    elif pinky_tip.y < ring_finger_tip.y and index_finger_tip.y < middle_finger_tip.y:
        return 'E'
    elif pinky_tip.y < middle_finger_tip.y and middle_finger_tip.y < index_finger_tip.y:
        return 'I'
    elif max(thumb_tip.y, index_finger_tip.y, middle_finger_tip.y, ring_finger_tip.y, pinky_tip.y) - \
         min(thumb_tip.y, index_finger_tip.y, middle_finger_tip.y, ring_finger_tip.y, pinky_tip.y) < 0.1:
        return 'O'
    elif middle_finger_tip.y < index_finger_tip.y and thumb_tip.x < index_finger_tip.x:
        return 'U'
    return 'Unknown'

# Define the fixed starting position (adjust these values as needed)
starting_x = 194
starting_y = 51.6
starting_z = -42.6

# Move the arm to the fixed starting position
arm.set_position(starting_x, starting_y, starting_z, speed=100, wait=True) 

# Main loop for detection and drawing
# List of vowels to simulate
vowels = ['A', 'E', 'I', 'O', 'U']
vowel_index = 0  # To cycle through vowels

while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    # Uncomment the following lines if you want to use real detection in the future
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # results = hands.process(image)
    # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # if results.multi_hand_landmarks:
    #     for hand_landmarks in results.multi_hand_landmarks:
    #         vowel = detect_vowel(hand_landmarks, mp_hands)
    #         ...

    # Simulated vowel detection
    vowel = vowels[vowel_index]
    cv2.putText(image, f"Simulated Vowel: {vowel}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    current_x, current_y = get_current_position()
    if current_x is not None and current_y is not None:
        current_x, current_y = move_arm_to_draw_vowel(vowel, current_x, current_y)

    # Update vowel_index to cycle through vowels
    vowel_index = (vowel_index + 1) % len(vowels)

    cv2.imshow('Vowel Simulation', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
arm.disconnect()
