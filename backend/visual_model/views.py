from django.shortcuts import render
import base64
import cv2
import numpy as np
from django.core.files.base import ContentFile
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage
from ultralytics import YOLO
import mediapipe as mp
from .saved_video_analysis import *
from .models import *
import os, time
from manage import base_dir
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Load the YOLOv8 model
model = YOLO('src/models/yolov8n.pt')  # Replace this with the correct model path if needed

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)

# Function to calculate head movement based on landmarks
# def calculate_head_movement(landmarks):
#     nose_tip = np.array([landmarks[1][0], landmarks[1][1]])  # Nose tip landmark
#     chin = np.array([landmarks[152][0], landmarks[152][1]])  # Chin landmark
#     left_ear = np.array([landmarks[234][0], landmarks[234][1]])  # Left ear landmark
#     right_ear = np.array([landmarks[454][0], landmarks[454][1]])  # Right ear landmark
#     ear_midpoint = (left_ear + right_ear) / 2
#     movement_vector = nose_tip - ear_midpoint
#     vertical_movement_vector = nose_tip - chin
#     return movement_vector, vertical_movement_vector

# # Function to determine head movement direction
# def determine_head_direction(movement_vector, vertical_movement_vector):
#     x_movement = movement_vector[0]
#     y_movement = vertical_movement_vector[1]
#     # y_movement = movement_vector[1]
#     print(f"X movement: {x_movement}, Y movement: {y_movement}")
#     if abs(x_movement) > 15:
#         return "Looking Right" if x_movement < 0 else "Looking Left"

#     if abs(y_movement) > 60: 
#         return "Looking Up" if y_movement < 0 else "Looking Down"

#     return "Facing Forward"

# # Function to determine if the mouth is open
# def is_mouth_open(landmarks):
#     mouth_left = np.array(landmarks[61])  # Left corner of mouth
#     mouth_right = np.array(landmarks[291])  # Right corner of mouth
#     mouth_top = np.array(landmarks[0])  # Center of upper lip
#     mouth_bottom = np.array(landmarks[17])  # Center of lower lip

#     mouth_width = np.linalg.norm(mouth_left - mouth_right)
#     mouth_height = np.linalg.norm(mouth_top - mouth_bottom)

#     # Heuristic to determine if the mouth is open
#     return mouth_height > mouth_width * 0.6


def calculate_head_movement(landmarks):
    # Define key facial landmarks
    nose_tip = np.array([landmarks[1][0], landmarks[1][1]])      # Nose tip
    nose_bridge = np.array([landmarks[6][0], landmarks[6][1]])   # Bridge of nose
    chin = np.array([landmarks[152][0], landmarks[152][1]])      # Chin
    left_ear = np.array([landmarks[234][0], landmarks[234][1]])  # Left ear
    right_ear = np.array([landmarks[454][0], landmarks[454][1]]) # Right ear
    
    # Calculate face size for normalization
    face_width = np.linalg.norm(right_ear - left_ear)
    face_height = np.linalg.norm(nose_bridge - chin)
    face_size = np.sqrt(face_width * face_height)
    
    # Calculate ear midpoint (head center)
    ear_midpoint = (left_ear + right_ear) / 2
    
    # Calculate normalized vectors
    movement_vector = (nose_tip - ear_midpoint) / face_size
    vertical_movement_vector = (nose_tip - chin) / face_size
    
    # Calculate additional rotation metrics
    head_rotation = {
        'horizontal': movement_vector,
        'vertical': vertical_movement_vector,
        'face_size': face_size,
        # 'confidence': min(
        #     1.0,
        #     np.linalg.norm(movement_vector) * 2,  # Scale factor for confidence
        #     np.linalg.norm(vertical_movement_vector) * 2
        # )
    }
    
    return head_rotation


def determine_head_direction(head_rotation):
    # Extract normalized vectors
    movement_vector = head_rotation['horizontal']
    vertical_vector = head_rotation['vertical']
    # confidence = head_rotation['confidence']
    
    # Thresholds for movement detection (normalized values)
    HORIZONTAL_THRESHOLD = 0.20
    # VERTICAL_THRESHOLD = 0.20
    VERTICAL_THRESHOLD_1 = 0.70
    VERTICAL_THRESHOLD_2 = 0.55
    # MIN_CONFIDENCE = 0.6
    
    # Get magnitudes of movement
    horizontal_movement = movement_vector[0]
    vertical_movement = vertical_vector[1]
    
    # if confidence < MIN_CONFIDENCE:
    #     return {
    #         'direction': "Facing Forward",
    #         'confidence': confidence,
    #         'movement': {
    #             'horizontal': horizontal_movement,
    #             'vertical': vertical_movement
    #         }
    #     }
    
    # Determine primary direction based on largest movement
    if abs(horizontal_movement) > HORIZONTAL_THRESHOLD:
        direction = "Looking Right" if horizontal_movement < 0 else "Looking Left"
        movement_confidence = min(abs(horizontal_movement) / HORIZONTAL_THRESHOLD, 1.0)
    # elif abs(vertical_movement) > VERTICAL_THRESHOLD:
    #     direction = "Looking Up" if vertical_movement < 0 else "Looking Down"
    #     movement_confidence = min(abs(vertical_movement) / VERTICAL_THRESHOLD, 1.0)
    elif abs(vertical_movement) > VERTICAL_THRESHOLD_1:
        direction = "Looking Up"
        movement_confidence = min(abs(vertical_movement) / VERTICAL_THRESHOLD_1, 1.0)
    elif abs(vertical_movement) < VERTICAL_THRESHOLD_2:
        direction = "Looking Down"
        movement_confidence = min(abs(vertical_movement) / VERTICAL_THRESHOLD_2, 1.0)
    else:
        direction = "Facing Forward"
        movement_confidence = 1.0 - max(
            abs(horizontal_movement) / HORIZONTAL_THRESHOLD,
            abs(vertical_movement) / ((VERTICAL_THRESHOLD_1 + VERTICAL_THRESHOLD_2) / 2)
        )
    
    # print("Vertical movement: ", vertical_movement)
    
    return {
        'direction': direction,
        # 'confidence': movement_confidence * confidence,
        'movement': {
            'horizontal': horizontal_movement,
            'vertical': vertical_movement
        }
    }

def is_mouth_open(landmarks):
    # Additional landmark points for better accuracy
    upper_lip_points = [0, 37, 39, 40, 267, 269, 270]  # Upper lip landmarks
    lower_lip_points = [17, 84, 91, 314, 321, 375]     # Lower lip landmarks
    
    # Get average positions
    upper_lip = np.mean([np.array(landmarks[p]) for p in upper_lip_points], axis=0)
    lower_lip = np.mean([np.array(landmarks[p]) for p in lower_lip_points], axis=0)
    
    # Calculate face proportions for normalization
    face_height = np.linalg.norm(
        np.array(landmarks[152]) -  # Chin
        np.array(landmarks[10])     # Upper nose
    )
    
    # Calculate mouth metrics
    mouth_height = np.linalg.norm(upper_lip - lower_lip)
    mouth_ratio = mouth_height / face_height
    
    # Dynamic thresholding based on face proportions
    threshold = 0.12  # Normalized threshold (12% of face height)
    # print(f"Mouth ratio: {mouth_ratio}")
    
    return {
        'is_open': mouth_ratio >= threshold,
        'confidence': min(mouth_ratio / threshold, 100),
        'ratio': mouth_ratio
    }



def save_suspicious_activity(image, activity_type, id):
    print("Saving suspicious activity")

    # Get the student
    student = Student.objects.get(id=id)
    
    # Prepare the image data
    _, img_encoded = cv2.imencode('.jpg', image)
    img_io = img_encoded.tobytes()
    
    # Generate file name
    timestamp = datetime.datetime.now()  # Current time in milliseconds
    # file_name = f"{activity_type}_{timestamp}.jpg"
    file_name = f"suspicious_activity_{int(time.time())}.jpg"
    
    # Construct the relative path within the static folder
    relative_path = os.path.join('backend','dashboard', 'static', 'suspicious_activities', student.email)
    
    # Get the full path
    full_path = os.path.join(base_dir, relative_path)
    
    # Ensure the directory exists
    os.makedirs(full_path, exist_ok=True)
    
    # Full file path
    file_path = os.path.join(full_path, file_name)
    
    # Use FileSystemStorage to save the file
    fs = FileSystemStorage(location=os.path.dirname(file_path))
    
    try:
        # filename = fs.save(file_path, ContentFile(img_io))
        # file_url = fs.url(os.path.join(relative_path, filename))
        base_filename = os.path.basename(file_path)
        filename = fs.save(base_filename, ContentFile(img_io))
        full_saved_path = os.path.join(fs.location, filename)
        print(f"File saved successfully at: {full_saved_path}")
    except Exception as e:
        print(f"Error saving file: {e}")
        return
    
    # Create a new SuspiciousActivity instance
    SuspiciousActivity.objects.create(
        student=student,
        activity_type=activity_type,
        screenshot=file_name,
        timestamp=timestamp
    )
    
    print(f"Saved suspicious activity: {activity_type} at {file_path}")
    

@api_view(['POST'])
def detect_mobile(request):
    # Parse image from request
    image_data = request.data['image']
    id = request.data['id']
    format, imgstr = image_data.split(';base64,')
    img_data = ContentFile(base64.b64decode(imgstr), name='temp.jpg')

    # Convert image to OpenCV format
    # model.cpu()
    nparr = np.frombuffer(img_data.read(), np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # img_np.cpu()

    # Perform YOLO detection
    warning = ''

    # Process for head movement detection
    rgb_frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            landmarks = [(int(landmark.x * img_np.shape[1]), int(landmark.y * img_np.shape[0])) for landmark in face_landmarks.landmark]

            # Calculate head movement and mouth status
            # movement_vector, vertical_movement_vector = calculate_head_movement(landmarks)
            # head_direction = determine_head_direction(movement_vector, vertical_movement_vector)
            # talking = is_mouth_open(landmarks)

            head_rotation = calculate_head_movement(landmarks)
            head_direction = determine_head_direction(head_rotation)
            talking = is_mouth_open(landmarks)


# TESTING CODE
            # warning = f"""
            # direction: {head_direction["direction"]}
            # horizontal: {head_direction["movement"]["horizontal"]:.2f}
            # vertical: {head_direction["movement"]["vertical"]:.2f}
            # Speaking: {talking["confidence"]:.2f}
            # Speaking: {talking["is_open"]}
            # Speaking: {talking["ratio"]:.2f}
            # """ 
            # save_suspicious_activity(img_np, warning, id)
# TESTING CODE
            
            if talking['is_open']:
                # warning = f'Speaking detected with confidence: {talking["confidence"]:.2f}'
                warning = f'Speaking detected'
                save_suspicious_activity(img_np, warning, id)

            if head_direction['direction'] != "Facing Forward":
                # warning = f'Head movement detected: {head_direction} with confidence: {head_direction["confidence"]:.2f}'
                warning = f'Head movement detected: {head_direction["direction"]}'
                save_suspicious_activity(img_np, warning, id)            

    results = model(img_np)  # Run inference

    # Initialize counters and flags
    mobile_detected = False
    person_count = 0

    # Process results from YOLO
    for result in results[0].boxes.data.tolist():
        x1, y1, x2, y2, confidence, cls = result
        class_id = int(cls)
        
        if class_id == 0:  # Class ID for person
            person_count += 1
            cv2.rectangle(img_np, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
            cv2.putText(img_np, 'Person', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
        
        if class_id == 67:  # Class ID for mobile phone
            mobile_detected = True
            cv2.rectangle(img_np, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
            cv2.putText(img_np, 'Mobile Phone', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    # Determine warnings based on detections
    if person_count == 0:
        warning = 'No person detected! Please return to the frame ASAP!'
        save_suspicious_activity(img_np, warning, id)
    elif person_count > 1:
        warning = 'Multiple people detected! This exam session is being recorded and monitored. Please ensure only you are visible in the frame.'
        save_suspicious_activity(img_np, warning, id)

    if mobile_detected:
        warning = 'Mobile phone detected! Please remove it immediately to avoid disqualification.'
        save_suspicious_activity(img_np, warning, id)



    return Response({'warning': warning})