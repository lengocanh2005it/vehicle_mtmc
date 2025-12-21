import cv2
import os

video_path = "./datasets/train/10fps-cam3-5p-sau.mp4" 
output_folder = "images"   
os.makedirs(output_folder, exist_ok=True)

cap = cv2.VideoCapture(video_path)
frame_id = 1

while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imwrite(os.path.join(output_folder, f"frame_{frame_id}.jpg"), frame)
    frame_id += 1

cap.release()
print(f"Hoàn tất tách video ra {frame_id-1} frame!")
