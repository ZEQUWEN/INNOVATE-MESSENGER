import re

with open('app/src/main/java/com/example/ui/MyProfileScreen.kt', 'r') as f:
    content = f.read()

# Fix isActive
content = content.replace('while (kotlinx.coroutines.isActive) {', 'while (kotlinx.coroutines.isActive) {') # already coroutines

# Syntax error
lines = content.split('\n')
for i, line in enumerate(lines):
    if i == 743:
        print(f"Line 743: {line}")
    if i == 139:
        print(f"Line 139: {line}")

