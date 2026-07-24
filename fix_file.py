with open('app/src/main/java/com/example/ui/MyProfileScreen.kt', 'r') as f:
    text = f.read()

# Let's count open and close braces
open_b = text.count('{')
close_b = text.count('}')
print(f"Open: {open_b}, Close: {close_b}")

