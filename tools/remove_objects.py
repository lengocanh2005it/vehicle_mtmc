# file: remove_objects.py

input_file = "0_mot.txt"
output_file = "mot_filtered.txt"

# danh sách object_id cần xoá
object_ids_to_remove = [
 20, 36, 61, 64, 92, 134, 153, 171, 216, 218 ,247, 300, 369, 426, 383,
    618, 643, 650, 679, 722, 740, 741, 788, 927, 939, 993,
    1112, 1164, 1194, 1213, 1244, 1252, 1281, 1333, 1345,
    1549, 1553, 1542, 1637, 1653
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
