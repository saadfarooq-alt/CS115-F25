import sys

if len(sys.argv) < 3:
    print("Usage: python3 filter_functions.py output.txt allowed_fn1 allowed_fn2 ...")
    sys.exit(1)

output_file = sys.argv[1]
allowed_functions = set(sys.argv[2:])

results = []

with open(output_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        # Format:  x/a01q1.rkt:   humidex
        try:
            file_part, func_name = line.split(":")
        except ValueError:
            continue

        func_name = func_name.strip()
        student, file_path = file_part.split("/", 1)

        # example file_path = a01q1.rkt
        question = file_path.replace(".rkt", "")

        # check if function is NOT allowed
        if func_name not in allowed_functions:
            results.append(f"{student} {question} {func_name}")

# write output
with open("final_output.txt", "w") as out:
    for r in results:
        out.write(r + "\n")

print("Done. Results saved to final_output.txt")

