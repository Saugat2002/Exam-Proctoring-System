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
def calculate_head_movement(landmarks):
    nose_tip = np.array([landmarks[1][0], landmarks[1][1]])  # Nose tip landmark
    chin = np.array([landmarks[152][0], landmarks[152][1]])  # Chin landmark
    left_ear = np.array([landmarks[234][0], landmarks[234][1]])  # Left ear landmark
    right_ear = np.array([landmarks[454][0], landmarks[454][1]])  # Right ear landmark
    ear_midpoint = (left_ear + right_ear) / 2
    movement_vector = nose_tip - ear_midpoint
    vertical_movement_vector = nose_tip - chin
    return movement_vector, vertical_movement_vector

# Function to determine head movement direction
def determine_head_direction(movement_vector, vertical_movement_vector):
    x_movement = movement_vector[0]
    y_movement = vertical_movement_vector[1]

    if abs(x_movement) > 30:
        return "Looking Right" if x_movement < 0 else "Looking Left"

    if abs(y_movement) > 60: 
        return "Looking Up" if y_movement < 0 else "Looking Down"

    return "Facing Forward"

# Function to determine if the mouth is open
def is_mouth_open(landmarks):
    mouth_left = np.array(landmarks[61])  # Left corner of mouth
    mouth_right = np.array(landmarks[291])  # Right corner of mouth
    mouth_top = np.array(landmarks[0])  # Center of upper lip
    mouth_bottom = np.array(landmarks[17])  # Center of lower lip

    mouth_width = np.linalg.norm(mouth_left - mouth_right)
    mouth_height = np.linalg.norm(mouth_top - mouth_bottom)

    # Heuristic to determine if the mouth is open
    return mouth_height > mouth_width * 0.4



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
        filename = fs.save(file_path, ContentFile(img_io))
        # file_url = fs.url(os.path.join(relative_path, filename))
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
        warning = ' Mobile phone detected! Please remove it immediately to avoid disqualification.'
        save_suspicious_activity(img_np, warning, id)

    # Process for head movement detection
    rgb_frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            landmarks = [(int(landmark.x * img_np.shape[1]), int(landmark.y * img_np.shape[0])) for landmark in face_landmarks.landmark]

            # Calculate head movement and mouth status
            movement_vector, vertical_movement_vector = calculate_head_movement(landmarks)
            head_direction = determine_head_direction(movement_vector, vertical_movement_vector)
            talking = is_mouth_open(landmarks)

            # Update warnings based on head movements
            if head_direction != "Facing Forward":
                warning = f'Head movement detected: {head_direction}'
                save_suspicious_activity(img_np, warning, id)
            # elif talking:
            #     warning = 'Speaking detected'
            #     save_suspicious_activity(img_np, warning)

    return Response({'warning': warning})


