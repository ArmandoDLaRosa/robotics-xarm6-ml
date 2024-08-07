import cv2
import mediapipe as mp

# Initialize MediaPipe Hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Initialize the webcam
cap = cv2.VideoCapture(0)

def is_A(hand_landmarks, mp_hands):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_finger_base = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
    return thumb_tip.x > index_finger_base.x  # Adjust based on hand orientation

def is_E(hand_landmarks, mp_hands):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    fingertips = [hand_landmarks.landmark[i] for i in [4, 8, 12, 16]]
    close_to_thumb = all(fingertip.y < thumb_tip.y + 0.05 for fingertip in fingertips)  # Small threshold to allow some distance
    return close_to_thumb

def is_I(hand_landmarks, mp_hands):
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
    pinky_base = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]
    other_fingertips = [hand_landmarks.landmark[i] for i in [4, 8, 12]]  # Indices for thumb, index, and middle fingertips
    return pinky_tip.y < pinky_base.y and all(f.y > pinky_base.y for f in other_fingertips)

def is_O(hand_landmarks, mp_hands):
    tips = [hand_landmarks.landmark[i] for i in [4, 8, 12, 16, 20]]
    average_x = sum(tip.x for tip in tips) / 5
    return all(abs(tip.x - average_x) < 0.02 for tip in tips)  # Fingers should be aligned vertically

def is_U(hand_landmarks, mp_hands):
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    return (index_tip.y < ring_tip.y and middle_tip.y < ring_tip.y)  # Both index and middle are higher than the ring finger

def detect_vowel(hand_landmarks, mp_hands):
    if is_A(hand_landmarks, mp_hands):
        return 'A'
    elif is_E(hand_landmarks, mp_hands):
        return 'E'
    elif is_I(hand_landmarks, mp_hands):
        return 'I'
    elif is_O(hand_landmarks, mp_hands):
        return 'O'
    elif is_U(hand_landmarks, mp_hands):
        return 'U'
    else:
        return 'Unknown'

while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    # Convert the BGR image to RGB before processing
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # Convert the image back to BGR for displaying
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Draw the hand annotations on the image
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            vowel = detect_vowel(hand_landmarks, mp_hands)
            cv2.putText(image, vowel, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow('Vowel Detection', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
