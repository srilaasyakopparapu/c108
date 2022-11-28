import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)

tipIds = [4, 8, 12, 16, 20]

# Define a function to count fingers
def countFingers(image, hand_landmarks, handNo=0):
    if hand_landmarks:
       landmarks=hand_landmarks[handNo].landmark
       #print(landmarks)
       fingers=[]
       for index in tipIds:
        fingertip_y=landmarks[index].y
        fingerbottom_y=landmarks[index-2].y
        if index !=4:
            if fingertip_y<fingerbottom_y:
                fingers.append(1)
                print("finger with ID ", index, "is open")
            if fingertip_y>fingerbottom_y:
                fingers.append(0)
                print("finger with ID", index, "is closed")
        totalFingers=fingers.count(1)
        text=f'fingers={totalFingers}'
        cv2.putText(image, text, (50, 50), cv2.FONT_HERSHEY_COMPLEX,1, (255, 0, 0), 2)
        
# Define a function to 
def drawHandLanmarks(image, hand_landmarks):

    # Darw connections between landmark points
    if hand_landmarks:

      for landmarks in hand_landmarks:
               
        mp_drawing.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTIONS)


while True:
    success, image = cap.read()

    image = cv2.flip(image, 1)
    
    # Detect the Hands Landmarks 
    results = hands.process(image)

    # Get landmark position from the processed result
    hand_landmarks = results.multi_hand_landmarks

    # Draw Landmarks
    drawHandLanmarks(image, hand_landmarks)

    # Get Hand Fingers Position        
    countFingers(image,hand_landmarks)

    cv2.imshow("Media Controller", image)

    # Quit the window on pressing Sapcebar key
    key = cv2.waitKey(1)
    if key == 32:
        break

cv2.destroyAllWindows()
