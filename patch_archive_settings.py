import sys

with open("app/src/main/java/com/example/ui/MainScreen.kt", "r") as f:
    content = f.read()

# Add archive_settings to NavHost
navhost_target = """                            composable("archived_chats") { ArchivedChatsScreen(viewModel, mainNavController) }"""
navhost_replace = """                            composable("archived_chats") { ArchivedChatsScreen(viewModel, mainNavController) }
                            composable("archive_settings") { ArchiveSettingsScreen(mainNavController) }"""
content = content.replace(navhost_target, navhost_replace)

# Modify ArchivedChatsScreen DropdownMenuItem
dropdown_target = """                            DropdownMenuItem(
                                text = { Text("Archive Settings") },
                                onClick = { showMenu = false }
                            )"""
dropdown_replace = """                            DropdownMenuItem(
                                text = { Text("Archive Settings") },
                                onClick = { 
                                    showMenu = false
                                    navController.navigate("archive_settings")
                                },
                                leadingIcon = {
                                    Icon(Icons.Filled.Settings, contentDescription = null)
                                }
                            )"""
content = content.replace(dropdown_target, dropdown_replace)

with open("app/src/main/java/com/example/ui/MainScreen.kt", "w") as f:
    f.write(content)
print("Patched MainScreen.kt")

