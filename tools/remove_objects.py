# file: remove_objects.py

input_file = "0_mot.txt"
output_file = "mot_out.txt"

# danh sách object_id cần xoá
object_ids_to_remove = [
 28, 30, 32, 58, 103, 105, 60, 125, 126, 127, 129, 130, 131, 242, 268, 277, 349, 350, 351, 361,
 45, 6, 7, 9, 13, 10, 17, 13, 24, 81, 80, 90, 113, 110 ,119, 224, 243, 23
]

with open(input_file, "r") as fin, open(output_file, "w") as fout:
    for line in fin:
        line = line.strip()
        if not line:
            continue

        parts = line.split(",")

        # cột 2 dạng string → convert sang int
        col2 = int(parts[1])

        # nếu object_id nằm trong danh sách xoá → bỏ dòng
        if col2 in object_ids_to_remove:
            continue

        # ghi lại dòng
        fout.write(",".join(parts) + "\n")

print("Done! (lines with specified object_ids removed)")
