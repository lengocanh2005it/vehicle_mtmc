import os
import cv2
import pickle
import argparse
import numpy as np
from mtmc.multicam_tracklet import MulticamTracklet

def load_mtmc_tracklets(pkl_path):
    """Load MTMC tracklets từ file pickle"""
    with open(pkl_path, "rb") as f:
        return pickle.load(f)

def visualize_camera(camera_id, mtmc_tracks, video_path, output_path):
    """Vẽ bounding box + MTMC ID lên video"""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"[ERROR] Cannot open video: {video_path}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 20

    ret, frame = cap.read()
    if not ret:
        print(f"[ERROR] Cannot read first frame: {video_path}")
        return
    h, w = frame.shape[:2]

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    out = cv2.VideoWriter(
        output_path,
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (w, h)
    )

    # --- Tạo dict frame_id -> list of (bbox, MTMC_id) ---
    frame_dict = {}
    for mt in mtmc_tracks:
        for track in mt._tracks:
            if track.cam != camera_id:
                continue
            for fid, bbox in zip(track.frames, track.bboxes):
                frame_dict.setdefault(fid, []).append((bbox, mt.id))

    # --- Tạo màu cố định cho mỗi MTMC ID ---
    id_colors = {}

    # --- Quay lại đầu video ---
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    frame_id = 1  # CityFlow MTMC frames bắt đầu từ 1
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_id in frame_dict:
            for bbox, track_id in frame_dict[frame_id]:
                x, y, w_box, h_box = bbox
                x1, y1, x2, y2 = int(x), int(y), int(x + w_box), int(y + h_box)

                if track_id not in id_colors:
                    id_colors[track_id] = tuple(np.random.randint(0, 255, 3).tolist())
                color = id_colors[track_id]

                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, f"ID {track_id}", (x1, y1 - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        out.write(frame)
        frame_id += 1

    cap.release()
    out.release()
    print(f"[OK] Saved video: {output_path}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mtmc", required=True, help="Path tới mtmc_tracklets.pkl")
    parser.add_argument("--videos_dir", required=True, help="Folder chứa video gốc")
    parser.add_argument("--output_dir", required=True, help="Folder lưu video visualize")
    parser.add_argument("--cams", nargs="+", required=True, help="Camera ID, ví dụ 0 1 2")
    args = parser.parse_args()

    args.output_dir = os.path.abspath(args.output_dir)
    os.makedirs(args.output_dir, exist_ok=True)
    print(f"[INFO] Output folder: {args.output_dir}")

    mtmc_tracks = load_mtmc_tracklets(args.mtmc)
    print(f"[INFO] Loaded {len(mtmc_tracks)} MTMC tracks from {args.mtmc}")

    for cam_id in args.cams:
        cam_id_int = int(cam_id)
        video_path = os.path.join(args.videos_dir, f"{cam_id}.mp4")
        output_path = os.path.join(args.output_dir, f"{cam_id}_mtmc.mp4")
        visualize_camera(cam_id_int, mtmc_tracks, video_path, output_path)

if __name__ == "__main__":
    main()
