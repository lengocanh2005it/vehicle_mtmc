import pandas as pd
import cv2
import os
from tqdm import tqdm

# ===========================
# Cấu hình
# ===========================
frame_folder = "images"          # folder chứa frame video gốc
mot_file = "mot_part1.txt"       # file nhãn MOT
output_folder = "reid_dataset"   # folder lưu ảnh crop theo object_id
os.makedirs(output_folder, exist_ok=True)

# File train/query/gallery
train_file = "train.txt"
query_file = "query.txt"
gallery_file = "gallery.txt"

# ===========================
# Load nhãn MOT và làm sạch
# ===========================
df = pd.read_csv(mot_file, header=None)
df = df.dropna()
df = df[df[2] != -1]  # loại bỏ object_id = -1
df = df.drop_duplicates()

# Lấy danh sách object_id
object_ids = df[2].unique()
train_ids = object_ids[:700]
test_ids = object_ids[700:]

# ===========================
# Hàm crop và lưu ảnh
# ===========================
def crop_and_save(row):
    frame_id = int(row[0])
    camera_id = int(row[1])
    object_id = int(row[2])
    x, y, w, h = int(row[3]), int(row[4]), int(row[5]), int(row[6])
    
    img_path = os.path.join(frame_folder, f"frame_{frame_id}.jpg")
    if not os.path.exists(img_path):
        return None
    
    img = cv2.imread(img_path)
    x, y = max(0, x), max(0, y)
    x2, y2 = min(x + w, img.shape[1]), min(y + h, img.shape[0])
    crop_img = img[y:y2, x:x2]
    
    # Folder riêng cho mỗi object_id
    obj_folder = os.path.join(output_folder, str(object_id))
    os.makedirs(obj_folder, exist_ok=True)
    
    # Tên ảnh: <object_id>_<camera_id>_<frame_id>.jpg
    crop_name = f"{object_id}_{camera_id}_{frame_id}.jpg"
    crop_path = os.path.join(obj_folder, crop_name)
    
    cv2.imwrite(crop_path, crop_img)
    return crop_path, object_id

# ===========================
# Crop và chia train/query/gallery
# ===========================
train_list = []
query_list = []
gallery_list = []

print("Crop ảnh và chia train/query/gallery...")
for obj_id in tqdm(object_ids):
    obj_df = df[df[2] == obj_id]
    
    if obj_id in train_ids:
        # tất cả ảnh vào train
        for _, row in obj_df.iterrows():
            res = crop_and_save(row)
            if res: train_list.append(res)
    else:
        # test: query 1-3 ảnh đầu, phần còn lại gallery
        n_query = min(3, len(obj_df))
        for _, row in obj_df.iloc[:n_query].iterrows():
            res = crop_and_save(row)
            if res: query_list.append(res)
        for _, row in obj_df.iloc[n_query:].iterrows():
            res = crop_and_save(row)
            if res: gallery_list.append(res)

# ===========================
# Xuất file txt 2 cột: path,object_id
# ===========================
pd.DataFrame(train_list, columns=["path","id"]).to_csv(train_file, index=False, header=False)
pd.DataFrame(query_list, columns=["path","id"]).to_csv(query_file, index=False, header=False)
pd.DataFrame(gallery_list, columns=["path","id"]).to_csv(gallery_file, index=False, header=False)

print("Hoàn tất: ảnh crop + train/query/gallery")
