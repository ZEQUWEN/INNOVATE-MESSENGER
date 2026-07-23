import sys

with open("app/src/main/java/com/example/ui/MainScreen.kt", "r") as f:
    content = f.read()

# 1. Add "archived_chats" route to NavHost
navhost_target = """                            composable("chat_list") { ChatListScreen(viewModel, mainNavController, isStoryExpanded) { isStoryExpanded = it } }"""
navhost_replace = """                            composable("chat_list") { ChatListScreen(viewModel, mainNavController, isStoryExpanded) { isStoryExpanded = it } }
                            composable("archived_chats") { ArchivedChatsScreen(viewModel, mainNavController) }"""
content = content.replace(navhost_target, navhost_replace)


# 2. Modify ChatListScreen
chatlist_target = """    var isArchivedSection by remember { mutableStateOf(false) }
    
    val filteredChats = chats.filter { 
        !it.isBlocked &&
        it.isArchived == isArchivedSection &&
        (it.title.contains(searchQuery, ignoreCase = true) || 
        it.lastMessage.contains(searchQuery, ignoreCase = true)) &&
        when (selectedTabIndex) {
            1 -> !it.isGroup && !it.isChannel && !it.isBot // Personal
            2 -> it.isGroup
            3 -> it.isChannel
            4 -> it.isBot
            else -> true // All
        }
    }"""
chatlist_replace = """    val filteredChats = chats.filter { 
        !it.isBlocked &&
        !it.isArchived &&
        (it.title.contains(searchQuery, ignoreCase = true) || 
        it.lastMessage.contains(searchQuery, ignoreCase = true)) &&
        when (selectedTabIndex) {
            1 -> !it.isGroup && !it.isChannel && !it.isBot // Personal
            2 -> it.isGroup
            3 -> it.isChannel
            4 -> it.isBot
            else -> true // All
        }
    }"""
content = content.replace(chatlist_target, chatlist_replace)

search_bar_target = """                placeholder = { Text(if (isArchivedSection) "Search archived..." else "Search chats...", color = MaterialTheme.colorScheme.onSurfaceVariant) },"""
search_bar_replace = """                placeholder = { Text("Search chats...", color = MaterialTheme.colorScheme.onSurfaceVariant) },"""
content = content.replace(search_bar_target, search_bar_replace)

icon_target = """            Spacer(Modifier.width(8.dp))
            IconButton(
                onClick = { isArchivedSection = !isArchivedSection },
                modifier = Modifier.background(if (isArchivedSection) MaterialTheme.colorScheme.primary.copy(alpha = 0.2f) else Color.Transparent, CircleShape)
            ) {
                Icon(
                    Icons.Filled.Archive,
                    contentDescription = "Archived Chats",
                    tint = if (isArchivedSection) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant
                )
            }"""
icon_replace = """"""
content = content.replace(icon_target, icon_replace)

archive_item_target = """            item {
                Card(
                    modifier = Modifier.fillMaxWidth().padding(8.dp),"""
archive_item_replace = """            if (searchQuery.isBlank() && selectedTabIndex == 0) {
                item {
                    val archivedCount = chats.count { it.isArchived && !it.isBlocked }
                    if (archivedCount > 0) {
                        ListItem(
                            headlineContent = { Text("Archived Chats", fontWeight = FontWeight.Bold) },
                            supportingContent = { Text("$archivedCount chat${if(archivedCount>1)"s" else ""}") },
                            leadingContent = {
                                Box(
                                    modifier = Modifier
                                        .size(48.dp)
                                        .background(MaterialTheme.colorScheme.surfaceVariant, CircleShape),
                                    contentAlignment = Alignment.Center
                                ) {
                                    Icon(Icons.Filled.Archive, contentDescription = null, tint = MaterialTheme.colorScheme.onSurfaceVariant)
                                }
                            },
                            modifier = Modifier.clickable { navController.navigate("archived_chats") }
                        )
                    }
                }
            }

            item {
                Card(
                    modifier = Modifier.fillMaxWidth().padding(8.dp),"""
content = content.replace(archive_item_target, archive_item_replace)

with open("app/src/main/java/com/example/ui/MainScreen.kt", "w") as f:
    f.write(content)
print("Patched MainScreen.kt")
