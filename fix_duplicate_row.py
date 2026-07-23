with open("app/src/main/java/com/example/ui/ChatScreen.kt", "r") as f:
    lines = f.readlines()

for i in range(len(lines)):
    if "verticalAlignment = Alignment.CenterVertically," in lines[i]:
        if "verticalAlignment = Alignment.CenterVertically," in lines[i+6]:
            # Delete lines i+6 to i+10
            del lines[i+6:i+11]
            break

with open("app/src/main/java/com/example/ui/ChatScreen.kt", "w") as f:
    f.writelines(lines)
