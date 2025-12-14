import cv2
import pandas as pd
import os

frame_folder = "cam3"
mot_file = "mot_part1.txt"
output_video = "visual_bbox.avi"

# Load nhãn
df = pd.read_csv(mot_file, header=None)
df = df.dropna()

# bỏ dòng object_id = -1 (ở cột 1)
df = df[df[1] != -1]

# Lấy frame_size từ 1 frame đầu
first_frame_path = os.path.join(frame_folder, "frame_1.jpg")
frame = cv2.imread(first_frame_path)
height, width = frame.shape[:2]

# VideoWriter
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(output_video, fourcc, 20.0, (width, height))

# Lặp qua từng frame_id
frame_ids = sorted(df[0].unique())

for fid in frame_ids:
    frame_path = os.path.join(frame_folder, f"frame_{int(fid)}.jpg")

    if not os.path.exists(frame_path):
        print("Không tìm thấy frame:", frame_path)
        continue

    img = cv2.imread(frame_path)

    # Lấy object trong frame này
    objs = df[df[0] == fid]

    for _, row in objs.iterrows():
        track_id = int(row[1])       # đúng: track_id ở cột 1
        x = int(row[2])              # bbox x
        y = int(row[3])              # bbox y
        w = int(row[4])              # bbox width
        h = int(row[5])              # bbox height

        cv2.rectangle(img, (x, y), (x + w, y + h), (0,255,0), 2)
        cv2.putText(img, str(track_id), (x, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)

    out.write(img)

out.release()
print("Hoàn tất video visual bbox:", output_video)
