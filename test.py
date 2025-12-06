import pickle
from mtmc.multicam_tracklet import MulticamTracklet

file_path = "output/cityflow_mtmc_eval/mtmc_tracklets.pkl"

with open(file_path, "rb") as f:
    mtmc_tracks = pickle.load(f)

# Tạo set chứa tất cả camera ID
camera_ids = set()

for mtrack in mtmc_tracks:
    for track in mtrack.tracks:
        camera_ids.add(track.cam)

print(f"Tổng số camera ID: {len(camera_ids)}")
print("Các camera ID:", sorted(camera_ids))
