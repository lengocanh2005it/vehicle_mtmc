import pandas as pd
import os
import cv2
from sklearn.model_selection import train_test_split

# -----------------------------
# Bước 0: Cấu hình
# -----------------------------
cams = ['cam1','cam2','cam3']
data_root = 'datasets/frames'  # folder chứa frames/cam1, cam2, cam3
save_root = 'datasets/Vehicle-ReID'
max_frame_per_cam = 5        # tối đa 5 frame/object/camera
min_total_per_object = 10    # mỗi object train ít nhất 10 frame
max_total_per_object = 20    # mỗi object train tối đa 20 frame

# -----------------------------
# Bước 1: Đọc nhãn tất cả camera
# -----------------------------
all_df = []

for cam_id, cam in enumerate(cams, 1):
    label_file = os.path.join(data_root, f'{cam}_labels.txt')
    df = pd.read_csv(label_file, header=None)
    
    # Chỉ lấy các cột cần thiết: frame_id, object_id, x, y, w, h
    df = df[[0,1,2,3,4,5]]  # cột 0=frame_id, 1=object_id, 2-5=bbox
    df.columns = ["frame_id","object_id","x","y","w","h"]
    
    df['cam_id'] = cam_id
    df['cam_name'] = cam
    
    # Bỏ object_id = -1
    df = df[df['object_id'] != -1]
    
    all_df.append(df)

all_df = pd.concat(all_df, ignore_index=True)
all_ids = all_df['object_id'].unique()

# -----------------------------
# Bước 2: Chia train/test theo object ID
# -----------------------------
train_ids, test_ids = train_test_split(all_ids, test_size=0.3, random_state=42)
train_df = all_df[all_df['object_id'].isin(train_ids)]
test_df  = all_df[all_df['object_id'].isin(test_ids)]

# -----------------------------
# Bước 3: Sample train: mỗi object từ 10–20 frame, mỗi camera tối đa 5 frame
# -----------------------------
def sample_train_per_object(df, max_per_cam=max_frame_per_cam, min_total=10, max_total=20):
    sampled_list = []

    for obj_id, group in df.groupby('object_id'):
        # Sample tối đa max_per_cam frame từ mỗi camera
        per_cam = group.groupby('cam_id', group_keys=False).apply(lambda x: x.sample(min(len(x), max_per_cam), random_state=42))
        
        # Reset index để dễ xử lý
        per_cam = per_cam.reset_index(drop=True)
        
        # Lấy index gốc của per_cam để loại ra khỏi group
        per_cam_index = per_cam.index if 'index' not in per_cam else per_cam['index']

        n = len(per_cam)
        
        # Nếu tổng số ảnh < min_total, thêm frame từ các camera (nếu còn)
        if n < min_total:
            remaining = group.drop(per_cam.index, errors='ignore')  # thêm errors='ignore'
            if len(remaining) > 0:
                extra = remaining.sample(min(min_total - n, len(remaining)), random_state=42)
                per_cam = pd.concat([per_cam, extra], ignore_index=True)
        
        # Nếu tổng số ảnh > max_total, sample ngẫu nhiên xuống còn max_total
        if len(per_cam) > max_total:
            per_cam = per_cam.sample(max_total, random_state=42).reset_index(drop=True)
        
        sampled_list.append(per_cam)

    sampled_df = pd.concat(sampled_list, ignore_index=True)
    return sampled_df


# Test: giữ 5 frame/object/camera
def sample_test_per_object_cam(df, max_per_cam=max_frame_per_cam):
    sampled_df = df.groupby(['object_id','cam_id']).apply(
        lambda x: x.sample(min(len(x), max_per_cam), random_state=42)
    ).reset_index(drop=True)
    return sampled_df

train_df = sample_train_per_object(train_df, max_per_cam=max_frame_per_cam,
                                   min_total=min_total_per_object, max_total=max_total_per_object)
test_df = sample_test_per_object_cam(test_df, max_per_cam=max_frame_per_cam)

# -----------------------------
# Bước 4: Crop bounding box và lưu ảnh
# -----------------------------
def crop_and_save(df, subset):
    folder = os.path.join(save_root, f'bounding_box_{subset}')
    os.makedirs(folder, exist_ok=True)

    for idx, row in df.iterrows():
        src = os.path.join(data_root, row.cam_name, f"frame_{row.frame_id}.jpg")
        dst_name = f"{row.object_id:04d}_c{row.cam_id}_f{row.frame_id:06d}.jpg"
        dst = os.path.join(folder, dst_name)

        if os.path.exists(src):
            img = cv2.imread(src)
            x1 = max(int(row['x']), 0)
            y1 = max(int(row['y']), 0)
            x2 = min(int(row['x'] + row['w']), img.shape[1])
            y2 = min(int(row['y'] + row['h']), img.shape[0])
            crop = img[y1:y2, x1:x2]
            if crop.size == 0:
                continue  # bỏ nếu bbox sai
            cv2.imwrite(dst, crop)

crop_and_save(train_df, 'train')
crop_and_save(test_df, 'test')

# -----------------------------
# Bước 5: Tạo query và gallery từ test folder
# -----------------------------
query_df = test_df.groupby('object_id').apply(lambda x: x.sample(1, random_state=42)).reset_index(drop=True)
gallery_df = test_df.drop(query_df.index)

# -----------------------------
# Bước 6: Lưu query.txt và gallery.txt
# Format: image_name object_id cam_id
# -----------------------------
def save_mapping(df, filename):
    with open(filename,'w') as f:
        for idx, row in df.iterrows():
            dst_name = f"{row.object_id:04d}_c{row.cam_id}_f{row.frame_id:06d}.jpg"
            f.write(f"{dst_name} {row.object_id} {row.cam_id}\n")

os.makedirs(save_root, exist_ok=True)
save_mapping(query_df, os.path.join(save_root,'query.txt'))
save_mapping(gallery_df, os.path.join(save_root,'gallery.txt'))

print("Hoàn tất: Dataset VeRi-776 multi-camera với ảnh crop bounding box, sample 10–20 frame/object!")
print(f"Train: {len(train_df)} ảnh, Test: {len(test_df)} ảnh, Query: {len(query_df)} ảnh, Gallery: {len(gallery_df)} ảnh")
