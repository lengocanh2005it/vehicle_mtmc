import cv2

def reduce_fps(
    input_video_path: str,
    output_video_path: str,
    target_fps: float
):
    cap = cv2.VideoCapture(input_video_path)

    if not cap.isOpened():
        raise RuntimeError("Không mở được video")

    original_fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(f"Original FPS: {original_fps}")

    # Nếu target fps >= fps gốc thì giữ nguyên
    if target_fps >= original_fps:
        raise ValueError("Target FPS phải nhỏ hơn FPS gốc")

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(
        output_video_path,
        fourcc,
        target_fps,
        (width, height)
    )

    frame_interval = original_fps / target_fps
    frame_count = 0
    saved_frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Chỉ lấy những frame phù hợp
        if int(frame_count % frame_interval) == 0:
            out.write(frame)
            saved_frame_count += 1

        frame_count += 1

    cap.release()
    out.release()

    print(f"Saved {saved_frame_count} frames")
    print("Done!")

# Ví dụ dùng
reduce_fps(
    input_video_path="input.mp4",
    output_video_path="output_15fps.mp4",
    target_fps=15
)
