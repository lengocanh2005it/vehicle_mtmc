import os
import cv2
import pickle
import argparse
from mtmc.multicam_tracklet import MulticamTracklet


def load_mtmc_tracklets(path):
    with open(path, "rb") as f:
        return pickle.load(f)

import os
import cv2

def visualize_camera(camera_id, mtmc_tracks, video_path, output_path):
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

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    out = cv2.VideoWriter(
        output_path,
        cv2.VideoWriter_fourcc(*"MJPG"),  # codec tương thích
        fps,
        (w, h)
    )

    # --- Tạo dict map frame_id -> list of bbox, id ---
    frame_dict = {}
    for mtrack in mtmc_tracks:
        for track in mtrack.tracks:
            if track.cam != camera_id:
                continue
            for fid, bbox in zip(track.frames, track.bboxes):
                frame_dict.setdefault(fid, []).append((bbox, mtrack.id))

    # --- Quay lại đầu video ---
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    frame_id = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_id in frame_dict:
            for bbox, track_id in frame_dict[frame_id]:
                x, y, w_box, h_box = bbox
                x1, y1, x2, y2 = int(x), int(y), int(x + w_box), int(y + h_box)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"ID {track_id}", (x1, y1 - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        out.write(frame)
        frame_id += 1

    cap.release()
    out.release()
    print(f"[OK] Saved: {output_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mtmc", required=True)
    parser.add_argument("--videos_dir", required=True)
    parser.add_argument("--output_dir", required=True)
    parser.add_argument("--cams", nargs="+", required=True)
    args = parser.parse_args()

    mtmc_tracks = load_mtmc_tracklets(args.mtmc)

    for cam_id in args.cams:
        cam_id = int(cam_id)
        video_path = os.path.join(args.videos_dir, f"camera-{cam_id}.mp4")
        output_path = os.path.join(args.output_dir, f"camera-{cam_id}_mtmc.mp4")
        visualize_camera(cam_id, mtmc_tracks, video_path, output_path)


if __name__ == "__main__":
    main()
