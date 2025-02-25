# import cv2
# import numpy as np
# import math
# from ultralytics import YOLO
# from .src.detect_face import get_face_detector, find_faces
# from .src.facial_landmarks import get_landmark_model, detect_marks
# from .src.head_pose_estimation import *
# from .src.track_eye import *
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from reportlab.lib import colors
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
# from reportlab.lib.styles import getSampleStyleSheet
# from collections import defaultdict
# import os
# from datetime import timedelta

# # Initialize models
# face_model = get_face_detector()
# landmark_model = get_landmark_model()
# yolo_model = YOLO('src/models/yolov8n.pt')

# # Camera matrix (you might need to adjust these values)
# def get_camera_matrix(size):
#     focal_length = size[1]
#     center = (size[1]/2, size[0]/2)
#     camera_matrix = np.array(
#         [[focal_length, 0, center[0]],
#          [0, focal_length, center[1]],
#          [0, 0, 1]], dtype = "double"
#     )
#     return camera_matrix

# # Eye points
# left_eye = [36, 37, 38, 39, 40, 41]
# right_eye = [42, 43, 44, 45, 46, 47]

# def analyze_video(video_path, output_folder):
#     cap = cv2.VideoCapture(video_path)
#     fps = cap.get(cv2.CAP_PROP_FPS)
#     frame_count = 0
#     cheating_warnings = defaultdict(lambda: {'duration': 0, 'screenshots': []})
    
#     size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
#     camera_matrix = get_camera_matrix(size)

#     print(f"Starting video analysis. FPS: {fps}")

#     while cap.isOpened():
#         ret, img = cap.read()
#         if not ret:
#             break

#         frame_count += 1000
#         cheating_indicators = []

#         faces = find_faces(img, face_model)
#         # Object detection using YOLOv8
#         results = yolo_model(img)
        
#         person_count = 0
#         phone_detected = False
#         person_boxes = []
        
#         for result in results:
#             boxes = result.boxes.cpu().numpy()
#             for box in boxes:
#                 class_id = int(box.cls[0])
#                 if class_id == 0:  # Person
#                     person_count += 1
#                     person_boxes.append(box.xyxy[0].astype(int))
#                 elif class_id == 67:  # Cell phone
#                     phone_detected = True

#         if person_count == 0:
#             cheating_indicators.append('No person detected')
#         elif person_count > 1:
#             cheating_indicators.append('Multiple persons detected')

#         if phone_detected:
#             cheating_indicators.append('Mobile phone detected')

#         for face in faces:
#             marks = detect_marks(img, landmark_model, face)

#             # Head pose estimation
#             image_points = np.array([marks[30], marks[8], marks[36], marks[45], marks[48], marks[54]], dtype="double")
#             dist_coeffs = np.zeros((4,1))
#             (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_UPNP)

#             # Check head pose
#             try:
#                 m = (p2[1] - p1[1])/(p2[0] - p1[0])
#                 ang1 = int(math.degrees(math.atan(m)))
#             except:
#                 ang1 = 90
                
#             try:
#                 m = (x2[1] - x1[1])/(x2[0] - x1[0])
#                 ang2 = int(math.degrees(math.atan(-1/m)))
#             except:
#                 ang2 = 90
                
#             if ang1 >= 35 or ang1 <= -35 or ang2 >= 35 or ang2 <= -35:
#                 cheating_indicators.append('User looks away from screen')

#             # Eye gaze estimation
#             mask = np.zeros(img.shape[:2], dtype=np.uint8)
#             mask, end_points_left = eye_on_mask(mask, left_eye, marks)
#             mask, end_points_right = eye_on_mask(mask, right_eye, marks)
            
#             eyes = cv2.bitwise_and(img, img, mask=mask)
#             mask = (eyes == [0, 0, 0]).all(axis=2)
#             eyes[mask] = [255, 255, 255]
#             mid = int((marks[42][0] + marks[39][0]) // 2)
#             eyes_gray = cv2.cvtColor(eyes, cv2.COLOR_BGR2GRAY)
            
#             threshold = 75
#             _, thresh = cv2.threshold(eyes_gray, threshold, 255, cv2.THRESH_BINARY)
#             thresh = process_thresh(thresh)
            
#             eyeball_pos_left = contouring(thresh[:, 0:mid], mid, img, end_points_left)
#             eyeball_pos_right = contouring(thresh[:, mid:], mid, img, end_points_right, True)
            
#             if eyeball_pos_left == 'right' and eyeball_pos_right == 'right':
#                 cheating_indicators.append('User eye gazes away from screen (right)')
#             elif eyeball_pos_left == 'left' and eyeball_pos_right == 'left':
#                 cheating_indicators.append('User eye gazes away from screen (left)')

#         # Object detection using YOLOv8
#         results = yolo_model(img)
        
#         person_count = 0
#         phone_detected = False
        
#         for result in results:
#             boxes = result.boxes.cpu().numpy()
#             for box in boxes:
#                 class_id = box.cls[0]
#                 if class_id == 0:  # Person
#                     person_count += 1
#                 elif class_id == 67:  # Cell phone
#                     phone_detected = True

#         if person_count > 1:
#             cheating_indicators.append('Multiple persons detected')
        
#         if phone_detected:
#             cheating_indicators.append('Mobile phone detected')

#         if cheating_indicators:
#             for indicator in cheating_indicators:
#                 cheating_warnings[indicator]['duration'] += 1
#                 # if cheating_warnings[indicator]['duration'] % int(fps * 5) == 0:  # Save screenshot every 5 seconds
#                 screenshot_path = os.path.join(output_folder, f"{indicator.replace(' ', '_')}_{frame_count}.jpg")
#                 cv2.imwrite(screenshot_path, img)
#                 cheating_warnings[indicator]['screenshots'].append(screenshot_path)

#         if frame_count % 100 == 0:
#             print(f"Processed {frame_count} frames. Current indicators: {cheating_indicators}")

#     cap.release()
#     print(f"Video analysis complete. Processed {frame_count} frames.")
#     return cheating_warnings, fps

# def generate_pdf_report(cheating_warnings, fps, output_path):
#     doc = SimpleDocTemplate(output_path, pagesize=letter)
#     styles = getSampleStyleSheet()
#     elements = []

#     # Title
#     elements.append(Paragraph("Proctoring Report", styles['Title']))
#     elements.append(Spacer(1, 12))

#     if not cheating_warnings:
#         elements.append(Paragraph("No suspicious activities detected.", styles['Normal']))
#     else:
#         for indicator, data in cheating_warnings.items():
#             # Lower the threshold to 1 second for debugging
#             if data['duration'] > 1:
#                 elements.append(Paragraph(f"Suspicious Activity: {indicator}", styles['Heading2']))
#                 # elements.append(Paragraph(f"Duration: {timedelta(seconds=int(data['duration']/fps))}", styles['Normal']))
#                 elements.append(Spacer(1, 12))

#                 for i, screenshot_path in enumerate(data['screenshots'][:3]):  # Limit to 3 screenshots
#                     if os.path.exists(screenshot_path):
#                         img = Image(screenshot_path, width=400, height=300)
#                         elements.append(img)
#                         elements.append(Paragraph(f"Screenshot {i+1}", styles['Normal']))
#                     else:
#                         elements.append(Paragraph(f"Screenshot {i+1} not found: {screenshot_path}", styles['Normal']))
#                     elements.append(Spacer(1, 12))

#                 elements.append(Spacer(1, 24))

#     doc.build(elements)
#     print(f"PDF report generated: {output_path}")

