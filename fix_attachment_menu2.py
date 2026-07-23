import re

with open("app/src/main/java/com/example/ui/ChatScreen.kt", "r") as f:
    content = f.read()

# 1. Remove `var showSignDialog...`
content = re.sub(r'\s*var showSignDialog by remember \{ mutableStateOf\(false\) \}', '', content)

# 2. Update DropdownMenuItem
old_menu_item = """                            DropdownMenuItem(
                                text = { Text("Document") },
                                onClick = { 
                                    attachmentMenuExpanded = false
                                    showSignDialog = true
                                },
                                leadingIcon = { Icon(Icons.Filled.Description, contentDescription = null) }
                            )"""
new_menu_item = """                            DropdownMenuItem(
                                text = { Text("File") },
                                onClick = { 
                                    attachmentMenuExpanded = false
                                    filePickerLauncher.launch(arrayOf("*/*"))
                                },
                                leadingIcon = { Icon(Icons.Filled.Description, contentDescription = null) }
                            )"""
content = content.replace(old_menu_item, new_menu_item)

# 3. Remove duplicate attach button
duplicate_button = """                    IconButton(onClick = { filePickerLauncher.launch(arrayOf("*/*")) }) {
                        Icon(Icons.Filled.AttachFile, contentDescription = "Attach File", tint = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
"""
content = content.replace(duplicate_button, '')

# 4. Remove AlertDialog block
dialog_block_regex = r'\s*if \(showSignDialog\) \{\s*AlertDialog\([\s\S]*?dismissButton = \{\s*TextButton\(onClick = \{[\s\S]*?showSignDialog = false\s*\}\) \{\s*Text\("Send As Is"\)\s*\}\s*\}\s*\)\s*\}'
content = re.sub(dialog_block_regex, '', content)

with open("app/src/main/java/com/example/ui/ChatScreen.kt", "w") as f:
    f.write(content)

