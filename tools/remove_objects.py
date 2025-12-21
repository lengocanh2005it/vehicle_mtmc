# file: remove_objects.py

input_file = "0_mot.txt"
output_file = "mot_out.txt"

# danh sách object_id cần xoá
object_ids_to_remove = [
42, 51, 72, 200, 208, 214, 218, 
212, 254, 264, 266, 294, 315, 334, 340, 343, 
422, 423, 429, 431, 508, 509, 540, 542, 562, 
638, 639, 614,643,642, 652,76,94,95,89,100,104,114,124,127,142,155,163,
167,171,172,197,201,216,247,279,359,370,374,379,381,391,393,412,413,418,426,430,476,483,
497,571,576,578,580,591,593,595,597,617,630,648,19,29,30,52,59,74,99,158,160,
168,170,174,177,181,166,193,217,230,241,243,250,251,252,258,261,281,313,321,329,
341,342,371,378,409,416,566,575,592,616,655,659,662,33,34,36,137,175,202,271,373,
428,434,437,445,448,491,492,507,551,558,107,270,436
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
