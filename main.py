import cv2
import pygame
import mediapipe as mp
import math

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True)
mp_drawing = mp.solutions.drawing_utils

# Initialize Pygame Mixer for alarm
pygame.mixer.init()
pygame.mixer.music.load("alarm-301729.wav")  # Make sure this file exists

# Drowsiness detection parameters
DROWSINESS_THRESHOLD = 0.25
DROWSY_FRAME_COUNT = 20
counter = 0
alarm_on = False

# EAR calculation helper function
def euclidean(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def get_EAR(landmarks, left_indices, right_indices):
    # Left eye
    left_top = landmarks[left_indices[1]]
    left_bottom = landmarks[left_indices[5]]
    left_left = landmarks[left_indices[0]]
    left_right = landmarks[left_indices[3]]

    left_EAR = euclidean(left_top, left_bottom) / euclidean(left_left, left_right)

    # Right eye
    right_top = landmarks[right_indices[1]]
    right_bottom = landmarks[right_indices[5]]
    right_left = landmarks[right_indices[0]]
    right_right = landmarks[right_indices[3]]

    right_EAR = euclidean(right_top, right_bottom) / euclidean(right_left, right_right)

    return (left_EAR + right_EAR) / 2

# Eye indices (MediaPipe's refined mesh)
LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]

# Start webcam
cap = cv2.VideoCapture(0)

print("📸 Starting webcam... Press 'q' to quit.")

while True:
    success, frame = cap.read()
    if not success:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(frame_rgb)

    if results.multi_face_landmarks:
        face_landmarks = results.multi_face_landmarks[0].landmark

        ear = get_EAR(face_landmarks, LEFT_EYE, RIGHT_EYE)

        if ear < DROWSINESS_THRESHOLD:
            counter += 1
            if counter >= DROWSY_FRAME_COUNT and not alarm_on:
                pygame.mixer.music.play(-1)
                alarm_on = True
                print("⚠️ Drowsiness detected!")
        else:
            counter = 0
            if alarm_on:
                pygame.mixer.music.stop()
                alarm_on = False
                print("✅ Alert. Alarm off.")

       # Optional: draw landmarks
        mp_drawing.draw_landmarks(frame, results.multi_face_landmarks[0],
                                  mp_face_mesh.FACEMESH_CONTOURS,
                                  landmark_drawing_spec=None,
                                  connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1))
        
        if alarm_on:
            cv2.putText(frame, "DROWSINESS DETECTED!", (30, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3, cv2.LINE_AA)

    else:
        counter = 0
        if alarm_on:
            pygame.mixer.music.stop()
            alarm_on = False

    cv2.imshow("Drowsiness Detector", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
pygame.mixer.music.stop()
cv2.destroyAllWindows()
