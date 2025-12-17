
mapping = {
   12: 3,
   3084: 4,
   348: 136,
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
