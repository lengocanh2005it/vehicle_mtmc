import pickle
import sys

sys.path.append("E:/vehicle_mtmc")

input_pkl = "mtmc_tracklets.pkl"
output_txt = "labels.txt"

with open(input_pkl, "rb") as f:
    data = pickle.load(f)   # list[MulticamTracklet]

with open(output_txt, "w") as out:
    for multi in data:
        multi_id = multi.id       # id toàn cục
        tracks = multi._tracks    # list các Tracklet

        for t in tracks:

            # track id nội bộ (thường cùng multi.id)
            track_id = t.track_id

            frames = t.frames     # list frame number
            bboxes = t.bboxes     # list np.array([x, y, w, h])

            for frame_id, bbox in zip(frames, bboxes):
                x, y, w, h = map(float, bbox)

                # Format MOT
                line = f"{frame_id}, {track_id}, {x:.2f}, {y:.2f}, {w:.2f}, {h:.2f}, 1, -1, -1\n"
                out.write(line)

print("✔ Done! Đã tạo file nhãn:", output_txt)
