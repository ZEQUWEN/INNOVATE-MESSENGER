with open("app/src/main/java/com/example/ui/ChatScreen.kt", "r") as f:
    lines = f.readlines()

for i in range(len(lines)):
    if "OutlinedTextField(" in lines[i]:
        if "OutlinedTextField(" in lines[i+1]:
            del lines[i]
            break

with open("app/src/main/java/com/example/ui/ChatScreen.kt", "w") as f:
    f.writelines(lines)
