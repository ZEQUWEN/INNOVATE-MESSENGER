with open("app/src/main/java/com/example/ui/ChatScreen.kt", "r") as f:
    lines = f.readlines()

new_lines = []
skip_next = False
in_sign_dialog = False

for i, line in enumerate(lines):
    if skip_next:
        skip_next = False
        continue
    
    # Remove `var showSignDialog`
    if "var showSignDialog by remember { mutableStateOf(false) }" in line:
        continue
        
    # Remove duplicate attach button
    if "IconButton(onClick = { filePickerLauncher.launch(arrayOf(\"*/*\")) })" in line:
        # skip this and next 2 lines
        continue
    if "Icon(Icons.Filled.AttachFile, contentDescription = \"Attach File\", tint = MaterialTheme.colorScheme.onSurfaceVariant)" in line and "IconButton(onClick = { filePickerLauncher.launch(arrayOf(\"*/*\")) })" in lines[i-1]:
        continue
    if line.strip() == "}" and "Icon(Icons.Filled.AttachFile, contentDescription = \"Attach File\", tint = MaterialTheme.colorScheme.onSurfaceVariant)" in lines[i-1]:
        continue

    # Update DropdownMenuItem
    if "text = { Text(\"Document\") }" in line:
        line = line.replace('Text("Document")', 'Text("File")')
    
    if "attachmentMenuExpanded = false" in line and "showSignDialog = true" in lines[i+1]:
        new_lines.append(line)
        continue
    if "showSignDialog = true" in line:
        new_lines.append('                                    filePickerLauncher.launch(arrayOf("*/*"))\n')
        continue

    # Remove AlertDialog for showSignDialog
    if "if (showSignDialog) {" in line:
        in_sign_dialog = True
        continue
    
    if in_sign_dialog:
        # count braces or just skip until it ends? 
        # let's just find the closing bracket for if(showSignDialog)
        # the dialog code is around lines 388-409. 
        # let's just wait until we see } that closes it. But it might be tricky.
        pass

    # Actually, simpler to just replace using string replace. Let's do that instead of line iteration.
