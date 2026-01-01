import cv2

def concat_videos_opencv(
    video_paths,
    output_path,
    target_fps
):
    caps = [cv2.VideoCapture(p) for p in video_paths]

    # Lấy thông tin từ video đầu
    width = int(caps[0].get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(caps[0].get(cv2.CAP_PROP_FRAME_HEIGHT))
    orig_fps = caps[0].get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(
        output_path,
        fourcc,
        target_fps,
        (width, height)
    )

    for idx, cap in enumerate(caps):
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = fps / target_fps

        frame_count = 0
        print(f"Processing video {idx+1}, fps={fps}")

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Resize nếu khác resolution
            frame = cv2.resize(frame, (width, height))

            if int(frame_count % frame_interval) == 0:
                out.write(frame)

            frame_count += 1

        cap.release()

    out.release()
    print("Done!")

# Ví dụ
concat_videos_opencv(
    video_paths=["./cam3_out.mp4", "./cam3_out_1.mp4"],
    output_path="merged_video_3.mp4",
    target_fps=10
)

# 21:06 -> 29:06