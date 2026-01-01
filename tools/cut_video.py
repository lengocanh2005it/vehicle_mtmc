import cv2

def time_to_frame(minutes, seconds, fps):
    """Chuyển phút + giây sang số frame"""
    return int((minutes * 60 + seconds) * fps)

def cut_video_opencv(
    input_path,
    output_path,
    start_min,
    start_sec,
    end_min,
    end_sec,
    target_fps=10
):
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print("Không mở được video")
        return

    fps_in = cap.get(cv2.CAP_PROP_FPS)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    start_frame = time_to_frame(start_min, start_sec, fps_in)
    end_frame   = time_to_frame(end_min, end_sec, fps_in)

    # Tỉ lệ lấy frame
    step = max(int(round(fps_in / target_fps)), 1)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, target_fps, (width, height))

    current_frame = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if start_frame <= current_frame <= end_frame:
            # Chỉ ghi mỗi step frame
            if (current_frame - start_frame) % step == 0:
                out.write(frame)

        current_frame += 1
        if current_frame > end_frame:
            break

    cap.release()
    out.release()

    print(
        f"Done! Cắt từ {start_min}:{start_sec:02d} "
        f"đến {end_min}:{end_sec:02d}, "
        f"fps gốc={fps_in:.2f} → fps mới={target_fps}"
    )

# -------------------------
# Ví dụ dùng
if __name__ == "__main__":
    cut_video_opencv(
        input_path="./datasets/cam3_1.MOV",
        output_path="./cam3_out_1.mp4",
        start_min=0,
        start_sec=0,
        end_min=4,
        end_sec=8,
        target_fps=10
    )