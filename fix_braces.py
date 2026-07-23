with open("app/src/main/java/com/example/ui/AppViewModel.kt", "r") as f:
    lines = f.readlines()

out = []
for line in lines:
    if line.strip() == "}":
        # Check if previous line was also }
        if len(out) > 0 and out[-1].strip() == "}":
            # Possible double brace
            pass
    out.append(line)

