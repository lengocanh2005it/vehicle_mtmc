import os
import cv2
import pickle
import argparse
from mtmc.multicam_tracklet import MulticamTracklet
import numpy as np

def load_mtmc_tracklets(path):
    """Load MTMC tracklets từ file .pkl"""
    with open(path, "rb") as f:
        return pickle.load(f)

def visualize_camera(camera_id, mtmc_tracks, video_path, output_path):
    """Vẽ bounding box và ID của MTMC lên video"""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"[ERROR] Cannot open video: {video_path}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 20  # fallback

    # Lấy kích thước video
    ret, frame = cap.read()
    if not ret:
        print(f"[ERROR] Cannot read first frame: {video_path}")
        return
    h, w = frame.shape[:2]

    # Tạo folder output cho video nếu chưa có
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # VideoWriter với codec mp4v
    out = cv2.VideoWriter(
        output_path,
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (w, h)
    )

    # --- Tạo dict map frame_id -> list of bbox, track_id ---
    frame_dict = {}
    for mtrack in mtmc_tracks:
        for track in mtrack.tracks:
            if str(track.cam) != str(camera_id):
                continue
            for fid, bbox in zip(track.frames, track.bboxes):
                frame_dict.setdefault(fid, []).append((bbox, mtrack.id))

    # --- Quay lại đầu video ---
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    frame_id = 1  # CityFlow tracklets bắt đầu từ frame 1
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_id in frame_dict:
            for bbox, track_id in frame_dict[frame_id]:
                x, y, w_box, h_box = bbox
                x1, y1, x2, y2 = int(x), int(y), int(x + w_box), int(y + h_box)
                # Vẽ bounding box
                color = (0, 255, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, f"ID {track_id}", (x1, y1 - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        out.write(frame)
        frame_id += 1

    cap.release()
    out.release()
    print(f"[OK] Saved: {output_path}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mtmc", required=True, help="Path tới mtmc_tracklets.pkl")
    parser.add_argument("--videos_dir", required=True, help="Thư mục chứa video gốc")
    parser.add_argument("--output_dir", required=True, help="Thư mục lưu video visualize")
    parser.add_argument("--cams", nargs="+", required=True, help="Danh sách camera ID cần visualize")
    args = parser.parse_args()

    # Tạo folder output tuyệt đối trước
    args.output_dir = os.path.abspath(args.output_dir)
    os.makedirs(args.output_dir, exist_ok=True)
    print(f"[INFO] Output folder: {args.output_dir}")

    # Load MTMC tracklets
    mtmc_tracks = load_mtmc_tracklets(args.mtmc)
    print(f"[INFO] Loaded {len(mtmc_tracks)} MTMC tracks from {args.mtmc}")

    # Duyệt từng camera
    for cam_id in args.cams:
        video_path = os.path.join(args.videos_dir, f"{cam_id}.mp4")
        output_path = os.path.join(args.output_dir, f"{cam_id}_mtmc.mp4")
        visualize_camera(cam_id, mtmc_tracks, video_path, output_path)

if __name__ == "__main__":
    main()
