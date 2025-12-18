import os

image_dir = "datasets/Vehicle-ReID/bounding_box_train"   # 🔁 đổi path này
output_txt = "datasets/Vehicle-ReID/gallery.txt"

with open(output_txt, "w") as f:
    for filename in sorted(os.listdir(image_dir)):
        if not filename.lower().endswith(".jpg"):
            continue

        # Ví dụ: 0116_c1_f000879.jpg
        parts = filename.split("_")

        person_id = int(parts[0])      # "0116" -> 116
        cam_id = int(parts[1][1:])     # "c1" -> 1

        f.write(f"{filename} {person_id} {cam_id}\n")

print("Done! File saved as", output_txt)