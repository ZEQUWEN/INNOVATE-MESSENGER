with open("app/src/main/java/com/example/ui/MainScreen.kt", "r") as f:
    lines = f.readlines()

import re

alert_logic = """
    var showStorageAlert by remember { mutableStateOf(false) }
    var storageAlertMessage by remember { mutableStateOf("") }
    
    LaunchedEffect(Unit) {
        kotlinx.coroutines.Dispatchers.IO.invoke {
            try {
                fun getFolderSize(file: java.io.File): Long {
                    var size: Long = 0
                    if (file.isDirectory) {
                        file.listFiles()?.forEach {
                            size += getFolderSize(it)
                        }
                    } else {
                        size = file.length()
                    }
                    return size
                }
                
                val dbSize = getFolderSize(context.getDatabasePath("messenger_db").parentFile ?: context.filesDir)
                val cacheSize = getFolderSize(context.cacheDir)
                val totalAppSize = dbSize + cacheSize
                
                val stat = android.os.StatFs(context.filesDir.path)
                val availableBytes = stat.availableBytes
                
                // If less than 500 MB remaining, alert the user
                if (availableBytes < 500L * 1024 * 1024 || totalAppSize > 1024L * 1024 * 1024) { 
                    storageAlertMessage = "Storage Warning: Device has ${availableBytes / (1024 * 1024)} MB free. App encrypted database and cache are currently using ${totalAppSize / (1024 * 1024)} MB. Please free up space."
                    showStorageAlert = true
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }
    
    if (showStorageAlert) {
        AlertDialog(
            onDismissRequest = { showStorageAlert = false },
            title = { Text("Storage Limit Warning") },
            text = { Text(storageAlertMessage) },
            confirmButton = {
                TextButton(onClick = { showStorageAlert = false }) { Text("OK") }
            }
        )
    }
"""

for i, line in enumerate(lines):
    if "val context = androidx.compose.ui.platform.LocalContext.current" in line:
        lines.insert(i + 1, alert_logic)
        break

with open("app/src/main/java/com/example/ui/MainScreen.kt", "w") as f:
    f.writelines(lines)

