def split_mot_file(input_path, output_small_path, output_large_path, threshold=3000):
    with open(input_path, "r") as f:
        lines = f.readlines()

    small = []
    large = []

    for line in lines:
        parts = line.strip().split(",")
        if len(parts) < 2:
            continue

        frame_id = int(parts[0])

        if frame_id < threshold:
            small.append(line)
        else:
            large.append(line)

    with open(output_small_path, "w") as f:
        f.writelines(small)

    with open(output_large_path, "w") as f:
        f.writelines(large)

    print("Done.")
    print(f"Frames < {threshold}: {len(small)} lines -> {output_small_path}")
    print(f"Frames >= {threshold}: {len(large)} lines -> {output_large_path}")


split_mot_file(
    "0_mot.txt",
    "mot_part1.txt",
    "mot_part2.txt",
    threshold=3000
)
