import pandas as pd

def cut_first_frames_mot(
    input_file: str,
    output_file: str,
    cut_frames: int = 70
):
    columns = [
        "frame", "track_id", "x", "y", "w", "h",
        "conf", "col8", "col9", "col10"
    ]

    df = pd.read_csv(input_file, header=None, names=columns)

    df = df[df["frame"] > cut_frames].copy()
    df["frame"] = df["frame"] - cut_frames

    df.to_csv(output_file, header=False, index=False)

    print(f"✅ Done! Saved to {output_file}")
    print(f"Remaining frames: {df['frame'].min()} → {df['frame'].max()}")


if __name__ == "__main__":
    # 🔧 chỉnh đường dẫn cho đúng
    input_file = "mot_final.txt"
    output_file = "mot_final_out.txt"
    cut_frames = 70

    cut_first_frames_mot(input_file, output_file, cut_frames)
