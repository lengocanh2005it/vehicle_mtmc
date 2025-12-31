import pandas as pd

# Danh sách 3 file MOT
files = ["1.txt", "2.txt", "3.txt"]

all_ids = set()  # dùng set để giữ id duy nhất

for f in files:
    # MOT có 10 cột, không header
    df = pd.read_csv(f, header=None, usecols=[1])  # chỉ đọc cột track_id
    ids = set(df[1].unique())
    all_ids.update(ids)

print(f"✅ Total unique track IDs in 3 cameras: {len(all_ids)}")
