with open("app/src/main/java/com/example/ui/ChatScreen.kt", "r") as f:
    content = f.read()

replacement = """                if (message.documentData != null) {
                    val documentData = message.documentData
                    var name = "File"
                    var size = 0L
                    var mime = ""
                    try {
                        val json = org.json.JSONObject(documentData)
                        name = json.optString("name", "File")
                        size = json.optLong("size", 0L)
                        mime = json.optString("mimeType", "")
                    } catch(e: Exception) {
                    }
                    
                    val icon = if (mime.startsWith("image/")) Icons.Filled.Image
                        else if (mime.startsWith("video/")) Icons.Filled.VideoFile
                        else if (mime.startsWith("audio/")) Icons.Filled.AudioFile
                        else Icons.Filled.InsertDriveFile

                    Column {
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            modifier = Modifier
                                .background(MaterialTheme.colorScheme.surface.copy(alpha = 0.2f), RoundedCornerShape(8.dp))
                                .padding(8.dp)
                        ) {
                            Icon(icon, contentDescription = "File", tint = if (isMe) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant)
                            Spacer(Modifier.width(8.dp))
                            Column {
                                Text(name, color = if (isMe) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant, fontWeight = androidx.compose.ui.text.font.FontWeight.Bold, style = MaterialTheme.typography.bodyMedium)
                                Text("${size / 1024} KB", color = if (isMe) MaterialTheme.colorScheme.onPrimary.copy(alpha = 0.8f) else MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.8f), style = MaterialTheme.typography.bodySmall)
                            }
                        }
                        if (message.text.isNotBlank()) {
                            Spacer(Modifier.height(4.dp))
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                if (message.isE2EEncrypted) {
                                    Icon(Icons.Filled.Lock, contentDescription = "Encrypted", modifier = Modifier.size(12.dp), tint = if (isMe) MaterialTheme.colorScheme.onPrimary.copy(alpha=0.6f) else MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha=0.6f))
                                    Spacer(Modifier.width(4.dp))
                                }
                                Text(message.text, color = if (isMe) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant)
                            }
                        }
                    }
                } else if (message.audioPath != null) {"""

import re
pattern = r'                if \(message\.documentData != null\) \{.*?                \} else if \(message\.audioPath != null\) \{'
content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open("app/src/main/java/com/example/ui/ChatScreen.kt", "w") as f:
    f.write(content)

