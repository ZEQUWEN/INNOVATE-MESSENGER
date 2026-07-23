import re

# AppViewModel.kt
with open('app/src/main/java/com/example/ui/AppViewModel.kt', 'r') as f:
    avm = f.read()

avm = re.sub(
    r'val account = repository\.getAccount\(accountId\)\n.*if \(account != null\) \{.*repository\.insertAccount\(account\.copy\(encryptedPasscode = encrypted\)\)\n\s*\}',
    """val account = _accounts.value.find { it.id == accountId }
            if (account != null) {
                val encrypted = newPasscode?.let { com.example.data.CryptoManager.encrypt(it) }
                repository.insertAccount(account.copy(encryptedPasscode = encrypted))
                _accounts.value = _accounts.value.map { if (it.id == accountId) it.copy(encryptedPasscode = encrypted) else it }
            }""",
    avm,
    flags=re.DOTALL
)

with open('app/src/main/java/com/example/ui/AppViewModel.kt', 'w') as f:
    f.write(avm)

# MainScreen.kt
with open('app/src/main/java/com/example/ui/MainScreen.kt', 'r') as f:
    ms = f.read()

ms = ms.replace('PasscodeLockScreen(mainNavController)', 'PasscodeLockScreen(viewModel, mainNavController)')

with open('app/src/main/java/com/example/ui/MainScreen.kt', 'w') as f:
    f.write(ms)

# SettingsScreens.kt
with open('app/src/main/java/com/example/ui/SettingsScreens.kt', 'r') as f:
    ss = f.read()

ss = "import androidx.compose.ui.text.font.FontWeight\n" + ss
ss = ss.replace('Icons.AutoMirrored.Filled.Backspace', 'Icons.AutoMirrored.Filled.ArrowBack') # Fallback if Backspace isn't mirrored

with open('app/src/main/java/com/example/ui/SettingsScreens.kt', 'w') as f:
    f.write(ss)

