import pandas as pd

# Tên file nhãn gốc
input_file = "mot_part1.txt"

# Load file nhãn
df = pd.read_csv(input_file, header=None)

# Loại bỏ các dòng có object_id = -1 hoặc frame_id = -1
df = df[(df[0].notna()) & (df[2] != -1)]

# Nếu muốn loại bỏ duplicate hoàn toàn
df = df.drop_duplicates()

# Cột object_id là cột 2 (0-based index)
object_ids = df[2].unique()

# Chia object_id
train_ids = object_ids[:700]
test_ids = object_ids[700:]

# Tạo dataframe train
train_df = df[df[2].isin(train_ids)]

# Tạo dataframe test (query và gallery)
query_list = []
gallery_list = []

for obj_id in test_ids:
    obj_df = df[df[2] == obj_id]
    # 1 → 3 ảnh đầu vào query (nếu ít hơn 3 thì lấy hết)
    n_query = min(3, len(obj_df))
    query_list.append(obj_df.iloc[:n_query])
    # Phần còn lại vào gallery
    if len(obj_df) > n_query:
        gallery_list.append(obj_df.iloc[n_query:])

query_df = pd.concat(query_list)
gallery_df = pd.concat(gallery_list)

# Xuất ra file với tên rõ ràng
train_df.to_csv("labels_train.txt", index=False, header=False)
query_df.to_csv("labels_query.txt", index=False, header=False)
gallery_df.to_csv("labels_gallery.txt", index=False, header=False)

print("Chia xong: train/query/gallery")
