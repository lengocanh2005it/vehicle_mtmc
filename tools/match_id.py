
mapping = {
    36: 12,
    64: 44,
    92: 38,
    61: 44,
    121: 110,
    171: 136,
    3036: 150,
    218: 175,
    134: 109,
    153: 114,
    247: 231,
    309: 271,
    1422: 1258,
    3009: 1657,
    383: 426,
    618: 600,
    643: 623,
    650: 614,
    682: 653,
    679: 688,
    722: 689,
    775: 761,
    3113: 772,
    3115: 772,
    3121: 806,
    1232: 858,
    927: 895,
    939: 907,
    2749: 921,
    1047: 1016,
    1155: 1123,
    1164: 1153,
    1172: 1151,
    1215: 1199,
    1014: 1201,
    1623: 1201,
    1233: 1208,
    1244: 1230,
    1252: 1234,
    1333: 1308,
    1345: 1322,
    1563: 1442,
    1549: 1509,
    1548: 1509,
    1553: 1512,
    1609: 1587,
    1653: 1629,
}


input_file = "2_mot.txt"
output_file = "mot_out.txt"

with open(input_file, "r") as fin, open(output_file, "w") as fout:
    for line in fin:
        line = line.strip()
        if not line:
            continue

        parts = line.split(",")

        # cột 2 dạng string → convert sang int
        col2 = int(parts[1])

        # nếu có trong mapping thì đổi
        if col2 in mapping:
            parts[1] = str(mapping[col2])

        fout.write(",".join(parts) + "\n")

print("Done! (mapping applied, no sorting)")
