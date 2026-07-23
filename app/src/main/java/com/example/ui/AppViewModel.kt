package com.example.ui

import androidx.room.Entity
import androidx.room.PrimaryKey
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.crypto.SignalProtocolManager
import com.example.data.MessengerRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.flow.update
import com.example.utils.MessageSanitizer
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.firstOrNull
import kotlinx.coroutines.launch
import kotlinx.coroutines.Dispatchers

enum class AppTheme {
    DEFAULT,
    NEON_SNOWFLAKES,
    NEON_CHERRY_BLOSSOM,
    NEON_CONFETTI,
    NEON_MOON,
    NEON_ROOM_FOG
}

@Entity(tableName = "accounts")
data class UserAccount(
    @PrimaryKey val id: String,
    val username: String,
    val displayName: String,
    val profilePicUrl: String, // Or gif URL
    val is2FAEnabled: Boolean = false,
    val isActive: Boolean = false,
    val bio: String = "",
    val sessionToken: String? = null,
    val customStatus: String = "",
    val encryptedPasscode: String? = null
)

@Entity(tableName = "contacts")
data class Contact(
    @PrimaryKey val id: String,
    val name: String,
    val phoneNumber: String?,
    val isRegistered: Boolean = true
)

@Entity(    tableName = "messages",
    indices = [androidx.room.Index("chatId"), androidx.room.Index("senderId")]
)
data class Message(
    @PrimaryKey val id: String,
    val chatId: String = "",
    val senderId: String,
    val text: String,
    val audioPath: String? = null,
    val isE2EEncrypted: Boolean = true,
    val timestamp: Long = System.currentTimeMillis(),
    val reaction: String? = null,
    val expiresAt: Long? = null,
    val isDelivered: Boolean = false,
    val isRead: Boolean = false,
    val isPinned: Boolean = false,
    val mediaPath: String? = null,
    val mediaType: String? = null,
    val documentData: String? = null,
    val locationData: String? = null,
    val buttonsData: String? = null
)

@Entity(tableName = "chats")
data class Chat(
    @PrimaryKey val id: String,
    val title: String,
    val isChannel: Boolean = false,
    val isGroup: Boolean = false,
    val isBot: Boolean = false,
    val isSecret: Boolean = false,
    val lastMessage: String,
    val unreadCount: Int = 0,
    val pinnedMessageId: String? = null,
    val isContact: Boolean = false,
    val isBlocked: Boolean = false,
    val isActionMenuDismissed: Boolean = false,
    val isArchived: Boolean = false
)

@Entity(
    tableName = "group_members",
    primaryKeys = ["chatId", "userId"],
    indices = [androidx.room.Index("chatId"), androidx.room.Index("userId")]
)
data class GroupMember(
    val chatId: String,
    val userId: String,
    val userName: String,
    val isAdmin: Boolean = false,
    val canReadMessages: Boolean = true,
    val canSendMessages: Boolean = true
)

@Entity(
    tableName = "drafts",
    indices = [androidx.room.Index("chatId")]
)
data class Draft(
    @PrimaryKey val chatId: String,
    val text: String
)

enum class ConnectionStatus {
    ONLINE, OFFLINE, CONNECTING
}

class AppViewModel(private val repository: MessengerRepository) : ViewModel() {
    private val signalProtocolManager = SignalProtocolManager()

    private val _theme = MutableStateFlow(
        run {
            val savedTheme = repository.getTheme()
            if (savedTheme != null) {
                try {
                    AppTheme.valueOf(savedTheme)
                } catch (e: Exception) {
                    AppTheme.DEFAULT
                }
            } else {
                AppTheme.DEFAULT
            }
        }
    )
    val theme: StateFlow<AppTheme> = _theme.asStateFlow()

    private val _isDarkThemeEnabled = MutableStateFlow(repository.getDarkThemeEnabled())
    val isDarkThemeEnabled: StateFlow<Boolean> = _isDarkThemeEnabled.asStateFlow()

    private val _isAutoThemeEnabled = MutableStateFlow(repository.getAutoThemeSwitcherEnabled())
    val isAutoThemeEnabled: StateFlow<Boolean> = _isAutoThemeEnabled.asStateFlow()

    private val _customPrimaryColor = MutableStateFlow<Long?>(repository.getCustomPrimaryColor())
    val customPrimaryColor: StateFlow<Long?> = _customPrimaryColor.asStateFlow()

    private val _customSecondaryColor = MutableStateFlow<Long?>(repository.getCustomSecondaryColor())
    val customSecondaryColor: StateFlow<Long?> = _customSecondaryColor.asStateFlow()

    private val _favoriteThemes = MutableStateFlow(repository.getFavoriteThemes())
    val favoriteThemes: StateFlow<Set<String>> = _favoriteThemes.asStateFlow()

    private val _batterySaverEnabled = MutableStateFlow(repository.getBatterySaverEnabled())
    val batterySaverEnabled: StateFlow<Boolean> = _batterySaverEnabled.asStateFlow()

    private val _themeOpacity = MutableStateFlow(repository.getThemeOpacity())
    val themeOpacity: StateFlow<Float> = _themeOpacity.asStateFlow()

    private val _connectionStatus = MutableStateFlow(ConnectionStatus.ONLINE)
    val connectionStatus: StateFlow<ConnectionStatus> = _connectionStatus.asStateFlow()

    private val _requires2FA = MutableStateFlow<String?>(null)
    val requires2FA: StateFlow<String?> = _requires2FA.asStateFlow()

    private val _confirmationCode = MutableStateFlow<String?>(null)
    val confirmationCode: StateFlow<String?> = _confirmationCode.asStateFlow()

    private val _pendingEmail = MutableStateFlow<String?>(null)
    val pendingEmail: StateFlow<String?> = _pendingEmail.asStateFlow()

    fun requestEmailConfirmation(email: String) {
        val code = (100000..999999).random().toString()
        _confirmationCode.value = code
        _pendingEmail.value = email
    }

    fun verifyEmailConfirmation(code: String): Boolean {
        val currentCode = _confirmationCode.value
        if (currentCode != null && currentCode == code) {
            val email = _pendingEmail.value
            _confirmationCode.value = null
            _pendingEmail.value = null
            
            // Update the email in active account
            viewModelScope.launch {
                val account = repository.allAccounts.firstOrNull()?.firstOrNull { it.isActive }
                if (account != null && email != null) {
                    repository.insertAccount(account.copy(username = email))
                }
            }
            
            return true
        }
        return false
    }

    private val _isAddingAccount = MutableStateFlow(false)
    val isAddingAccount: StateFlow<Boolean> = _isAddingAccount.asStateFlow()

    fun startAddAccount() {
        _isAddingAccount.value = true
        viewModelScope.launch { repository.logoutAll() }
    }

    fun clearAddingAccount() {
        _isAddingAccount.value = false
    }
    val accounts: StateFlow<List<UserAccount>> = repository.allAccounts
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5000),
            initialValue = emptyList()
        )

    val chats: StateFlow<List<Chat>> = repository.allChats
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5000),
            initialValue = emptyList()
        )

    val contacts: StateFlow<List<Contact>> = repository.allContacts
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5000),
            initialValue = emptyList()
        )

    private val _isE2EEnabled = MutableStateFlow(true)
    val isE2EEnabled: StateFlow<Boolean> = _isE2EEnabled.asStateFlow()

    init {
        viewModelScope.launch {
            // Periodic cleanup of expired messages
            launch {
                while (true) {
                    val now = System.currentTimeMillis()
                    repository.deleteExpiredMessages(now)
                    kotlinx.coroutines.delay(1000) // check every second
                }
            }
            
            // Seed initial data if empty
            val accs = repository.allAccounts.firstOrNull(); if (accs.isNullOrEmpty()) {
                
                    repository.insertAccount(UserAccount("1", "@neo_hacker", "Neo", "https://i.pravatar.cc/150?img=11", true, true))
                    repository.insertAccount(UserAccount("2", "@synth_wave", "Synth Wave", "https://i.pravatar.cc/150?img=33", false, false))
                    repository.insertAccount(UserAccount("3", "@cyber_punk", "Cyber P.", "https://i.pravatar.cc/150?img=55", false, false))
                    
                    repository.insertChat(Chat("c1", "Neon Coders", isGroup = true, lastMessage = "Let's build in Compose! \uD83D\uDD25", unreadCount = 4))
                    repository.insertChat(Chat("botfather", "BotFather", isBot = true, lastMessage = "I am the BotFather. I can help you create and manage your bots.", unreadCount = 0))
                    repository.insertChat(Chat("c2", "Cyberpunk Daily", isChannel = true, lastMessage = "Welcome to the future.", unreadCount = 12))
                    repository.insertChat(Chat("c3", "SynthBot", isBot = true, lastMessage = "Command executed.", unreadCount = 0))
                    repository.insertChat(Chat("c4", "@trinity", isGroup = false, lastMessage = "The matrix has you.", unreadCount = 1))

                    repository.insertGroupMember(GroupMember("c1", "u1", "Sarah Connor", isAdmin = true))
                    repository.insertGroupMember(GroupMember("c1", "u2", "John Doe", isAdmin = false))
                    repository.insertGroupMember(GroupMember("c1", "u3", "Crypto Alpha", isAdmin = false))
                    repository.insertGroupMember(GroupMember("c1", "u4", "Neon Hacker", isAdmin = false))
                }
        }
    }

    fun getMessages(chatId: String) = repository.getMessages(chatId).map { messages ->
        messages.map { msg ->
            msg.copy(text = signalProtocolManager.decryptMessage(msg.text))
        }
    }
    fun getGroupMembers(chatId: String) = repository.getGroupMembers(chatId)
    
    suspend fun getDraft(chatId: String) = repository.getDraft(chatId)

    fun updateAdminStatus(chatId: String, userId: String, isAdmin: Boolean) {
        viewModelScope.launch {
            repository.updateAdminStatus(chatId, userId, isAdmin)
        }
    }

    fun blockUser(chatId: String) {
        viewModelScope.launch {
            repository.updateBlockedStatus(chatId, true)
        }
    }

    fun unblockUser(chatId: String) {
        viewModelScope.launch {
            repository.updateBlockedStatus(chatId, false)
        }
    }

    fun clearHistory(chatId: String) {
        viewModelScope.launch {
            repository.clearHistory(chatId)
        }
    }

    fun deleteChat(chatId: String) {
        viewModelScope.launch {
            repository.deleteChat(chatId)
        }
    }

    fun addToContacts(chatId: String) {
        viewModelScope.launch {
            repository.updateContactStatus(chatId, true)
        }
    }

    fun dismissActionMenu(chatId: String) {
        viewModelScope.launch {
            repository.updateActionMenuDismissed(chatId, true)
        }
    }

    private val _typingChats = MutableStateFlow<Set<String>>(emptySet())
    val typingChats: StateFlow<Set<String>> = _typingChats.asStateFlow()

    fun simulateTyping(chatId: String) {
        viewModelScope.launch {
            _typingChats.update { it + chatId }
            kotlinx.coroutines.delay(3000)
            _typingChats.update { it - chatId }
        }
    }

    fun exportMessageHistory(chatId: String) {
        viewModelScope.launch {
            val messages = repository.getMessages(chatId).firstOrNull() ?: emptyList()
            val text = messages.joinToString("\n") { msg ->
                val decrypted = signalProtocolManager.decryptMessage(msg.text)
                "[${java.util.Date(msg.timestamp)}] ${msg.senderId}: $decrypted"
            }
            val encryptedBackup = signalProtocolManager.encryptMessage(text)
            // Simulating saving to a file. In a real app we'd use FileOutputStream to Context.filesDir.
            println("Exported history for $chatId: \n$encryptedBackup")
        }
    }
    fun updateProfile(id: String, username: String, displayName: String, bio: String, profilePicUrl: String, customStatus: String = "") {
        viewModelScope.launch {
            repository.updateProfile(id, username, displayName, bio, profilePicUrl, customStatus)
        }
    }
    
    fun addGroupMember(chatId: String, userId: String, userName: String, isAdmin: Boolean) {
        viewModelScope.launch {
            repository.insertGroupMember(com.example.ui.GroupMember(chatId, userId, userName, isAdmin))
        }
    }

    fun updateBotPermissions(chatId: String, userId: String, canRead: Boolean, canSend: Boolean) {
        viewModelScope.launch(Dispatchers.IO) {
            val member = repository.getGroupMemberSync(chatId, userId)
            if (member != null) {
                repository.insertGroupMember(member.copy(canReadMessages = canRead, canSendMessages = canSend))
            }
        }
    }

    fun removeGroupMember(chatId: String, userId: String) {
        viewModelScope.launch {
            repository.removeMember(chatId, userId)
        }
    }

    fun sendMessage(chatId: String, senderId: String, text: String, audioPath: String? = null, expiresIn: Long? = null, documentData: String? = null) {
        viewModelScope.launch {
            val sanitizedText = MessageSanitizer.sanitize(text)
            val encryptedMsg = signalProtocolManager.encryptMessage(sanitizedText)
            
            // If offline, message stays locally pending
            val isOnline = _connectionStatus.value == ConnectionStatus.ONLINE
            val msg = Message(
                id = java.util.UUID.randomUUID().toString(),
                chatId = chatId,
                senderId = senderId,
                text = encryptedMsg,
                audioPath = audioPath,
                timestamp = System.currentTimeMillis(),
                expiresAt = if (expiresIn != null) System.currentTimeMillis() + expiresIn else null,
                documentData = documentData,
                isDelivered = isOnline // if offline, it stays pending (not delivered)
            )
            repository.insertMessage(msg)
            
            if (isOnline) {
                // Simulate reply if online
                kotlinx.coroutines.delay(1000)
                simulateTyping(chatId)
                
                val chat = repository.allChats.firstOrNull()?.find { it.id == chatId }
                if (chat != null) {
                    if (chat.isBot || (chat.isGroup && sanitizedText.contains("@"))) {
                        BotService.handleMessage(sanitizedText, chat, repository, signalProtocolManager)
                    } else {
                        kotlinx.coroutines.delay(1500)
                        val reply = Message(
                            id = java.util.UUID.randomUUID().toString(),
                            chatId = chatId,
                            senderId = "other_user",
                            text = signalProtocolManager.encryptMessage("Got it: $sanitizedText"),
                            timestamp = System.currentTimeMillis(),
                            isDelivered = true
                        )
                        repository.insertMessage(reply)
                    }
                }
            }
        }
    }

    fun setConnectionStatus(status: ConnectionStatus) {
        _connectionStatus.value = status
        if (status == ConnectionStatus.ONLINE) {
            processOfflineQueue()
        }
    }
    
    private fun processOfflineQueue() {
        viewModelScope.launch {
            val chats = repository.allChats.firstOrNull() ?: emptyList()
            for (chat in chats) {
                val messages = repository.getMessages(chat.id).firstOrNull() ?: emptyList()
                val pendingMessages = messages.filter { !it.isDelivered && it.senderId != "other_user" }
                for (msg in pendingMessages) {
                    // Mark as delivered
                    repository.updateMessageDelivery(msg.id, true)
                    
                    // Simulate reply
                    kotlinx.coroutines.delay(1000)
                    simulateTyping(chat.id)
                    kotlinx.coroutines.delay(1500)
                    val reply = Message(
                        id = java.util.UUID.randomUUID().toString(),
                        chatId = chat.id,
                        senderId = "other_user",
                        text = signalProtocolManager.encryptMessage("Offline msg received: ${msg.text}"),
                        timestamp = System.currentTimeMillis(),
                        isDelivered = true
                    )
                    repository.insertMessage(reply)
                }
            }
        }
    }

    fun toggle2FA(accountId: String, currentEnabled: Boolean) {
        viewModelScope.launch {
            repository.update2FA(accountId, !currentEnabled)
        }
    }

    fun deleteMessage(messageId: String) {
        viewModelScope.launch {
            repository.deleteMessage(messageId)
        }
    }

    fun deleteAccount(accountId: String, onDeleted: () -> Unit) {
        viewModelScope.launch {
            repository.deleteAccount(accountId)
            onDeleted()
        }
    }

    // --- Search functionality context ---

    fun markMessagesAsRead(chatId: String, myUserId: String) {
        viewModelScope.launch {
            repository.markAsRead(chatId, myUserId)
        }
    }
    fun saveDraft(chatId: String, text: String?) {
        viewModelScope.launch {
            repository.updateDraft(chatId, text)
        }
    }
    fun addReaction(messageId: String, reaction: String) {
        viewModelScope.launch {
            repository.updateReaction(messageId, reaction)
        }
    }
    fun pinMessage(chatId: String, messageId: String) {
        viewModelScope.launch {
            repository.updatePinStatus(messageId, true)
        }
    }
    fun unpinMessage(chatId: String, messageId: String) {
        viewModelScope.launch {
            repository.updatePinStatus(messageId, false)
        }
    }
    fun switchAccount(accountId: String) {
        viewModelScope.launch {
            repository.switchActiveAccount(accountId)
        }
    }
    fun createAccount(username: String, displayName: String, bio: String = "", profilePicUrl: String = "", customStatus: String = "") {
        viewModelScope.launch {
            val account = UserAccount(
                id = java.util.UUID.randomUUID().toString(),
                username = username,
                displayName = displayName,
                bio = bio,
                profilePicUrl = profilePicUrl,
                customStatus = customStatus,
                isActive = true
            )
            repository.logoutAll()
            repository.insertAccount(account)
        }
    }
    fun addAccountAction() {
        _isAddingAccount.value = true
    }
    fun verify2FA(code: String) {
        _requires2FA.value = null
    }
    fun cancel2FA() {
        _requires2FA.value = null
    }
    fun createSecretChat(contactId: String) {
        viewModelScope.launch {
            val chat = Chat(id = java.util.UUID.randomUUID().toString(), title = "Secret Chat", isGroup = false, isSecret = true, lastMessage = "")
            repository.insertChat(chat)
        }
    }
    fun createChat(name: String, desc: String, photo: String, isPrivate: Boolean, linkOrUsername: String, isGroup: Boolean = false, isChannel: Boolean = false) {
        viewModelScope.launch {
            val chat = Chat(id = java.util.UUID.randomUUID().toString(), title = name, isGroup = isGroup, isSecret = false, isChannel = isChannel, lastMessage = "")
            repository.insertChat(chat)
        }
    }
    fun toggleArchive(chatId: String, isArchived: Boolean) {
        viewModelScope.launch {
            val chat = repository.allChats.firstOrNull()?.find { it.id == chatId }
            if (chat != null) {
                repository.updateArchiveStatus(chatId, !chat.isArchived)
            }
        }
    }
    fun setAutoThemeEnabled(enabled: Boolean) {
        _isAutoThemeEnabled.value = enabled
        repository.saveAutoThemeSwitcherEnabled(enabled)
    }
    fun setDarkThemeEnabled(enabled: Boolean) {
        _isDarkThemeEnabled.value = enabled
        repository.saveDarkThemeEnabled(enabled)
    }
    fun setBatterySaverEnabled(enabled: Boolean) {
        _batterySaverEnabled.value = enabled
        repository.saveBatterySaverEnabled(enabled)
    }
    fun setThemeOpacity(opacity: Float) {
        _themeOpacity.value = opacity
        repository.saveThemeOpacity(opacity)
    }
    fun setCustomPrimaryColor(color: Long?) {
        _customPrimaryColor.value = color
        if (color != null) repository.saveCustomPrimaryColor(color)
    }
    fun setCustomSecondaryColor(color: Long?) {
        _customSecondaryColor.value = color
        if (color != null) repository.saveCustomSecondaryColor(color)
    }
    fun switchTheme(theme: AppTheme) {
        _theme.value = theme
        repository.saveTheme(theme.name)
    }
    fun toggleFavoriteTheme(themeName: String) {
        val current = _favoriteThemes.value.toMutableSet()
        if (current.contains(themeName)) current.remove(themeName) else current.add(themeName)
        _favoriteThemes.value = current
        repository.saveFavoriteThemes(current)
    }
    fun importTheme(themeCode: String) {
        try {
            val parts = themeCode.substringAfter("Neon Messenger Theme Code: ").split("-")
            if (parts.size >= 3) {
                val themeName = parts[0]
                val primaryStr = parts[1]
                val secondaryStr = parts[2]
                switchTheme(AppTheme.valueOf(themeName))
                setCustomPrimaryColor(if (primaryStr != "def") primaryStr.toLongOrNull() else null)
                setCustomSecondaryColor(if (secondaryStr != "def") secondaryStr.toLongOrNull() else null)
                setAutoThemeEnabled(false)
            }
        } catch (e: Exception) {}
    }
    fun resetTheme() {
        switchTheme(AppTheme.DEFAULT)
        setCustomPrimaryColor(null)
        setCustomSecondaryColor(null)
        setAutoThemeEnabled(false)
    }
    fun logout() {
        viewModelScope.launch {
            repository.logoutAll()
        }
    }
    fun checkAutoTheme() {}
    fun addBot(chat: Chat) { viewModelScope.launch { repository.insertChat(chat) } }

    fun updatePasscode(accountId: String, newPasscode: String?) {
        viewModelScope.launch(kotlinx.coroutines.Dispatchers.IO) {
            val account = accounts.value.find { it.id == accountId }
            if (account != null) {
                val encrypted = newPasscode?.let { com.example.data.CryptoManager.encrypt(it) }
                repository.insertAccount(account.copy(encryptedPasscode = encrypted, is2FAEnabled = if (encrypted != null) false else account.is2FAEnabled))
            }
        }
    }
}
