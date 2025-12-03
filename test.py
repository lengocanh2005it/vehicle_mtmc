import cv2

input_video = "datasets/IMG_4015.MOV"
output_video = "video_cut.mp4"

# Thời gian bắt đầu và kết thúc: phút + giây
start_minute, start_second = 0, 49
end_minute, end_second = 10, 49 

# Chuyển sang giây
start_time = start_minute * 60 + start_second
end_time = end_minute * 60 + end_second

cap = cv2.VideoCapture(input_video)

fps = cap.get(cv2.CAP_PROP_FPS)
start_frame = int(start_time * fps)
end_frame = int(end_time * fps)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

current_frame = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    if start_frame <= current_frame <= end_frame:
        out.write(frame)
    elif current_frame > end_frame:
        break
    current_frame += 1

cap.release()
out.release()
cv2.destroyAllWindows()
