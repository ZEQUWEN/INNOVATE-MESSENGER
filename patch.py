with open("app/src/main/java/com/example/ui/AppViewModel.kt", "r") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "fun sendMessage(chatId: String, senderId: String, text: String, audioPath: String? = null, expiresIn: Long? = null)" in line:
        lines[i] = "    fun sendMessage(chatId: String, senderId: String, text: String, audioPath: String? = null, expiresIn: Long? = null, documentData: String? = null) {\n"
    if "expiresAt = if (expiresIn != null) System.currentTimeMillis() + expiresIn else null" in line:
        lines[i] = line + "                , documentData = documentData\n"

with open("app/src/main/java/com/example/ui/AppViewModel.kt", "w") as f:
    f.writelines(lines)
