import cv2

def time_to_frame(minutes, seconds, fps):
    """Chuyển phút + giây sang số frame"""
    return int((minutes * 60 + seconds) * fps)

def cut_video_opencv(input_path, output_path, start_min, start_sec, end_min, end_sec):
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print("Không mở được video")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    start_frame = time_to_frame(start_min, start_sec, fps)
    end_frame   = time_to_frame(end_min, end_sec, fps)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # hoặc 'XVID'
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    current_frame = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if current_frame >= start_frame and current_frame <= end_frame:
            out.write(frame)

        current_frame += 1
        if current_frame > end_frame:
            break

    cap.release()
    out.release()
    print(f"Done! Video đã được cắt từ frame {start_frame} đến {end_frame} -> {output_path}")

# -------------------------
# Ví dụ dùng
if __name__ == "__main__":
    cut_video_opencv(
        input_path="./datasets/train/camera-1.mp4",
        output_path="./datasets/train/train-camera-1.mp4",
        start_min=5,
        start_sec=0,
        end_min=10,
        end_sec=0
    )
