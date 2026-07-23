with open('app/src/main/java/com/example/ui/AppViewModel.kt', 'r') as f:
    avm = f.read()

import re
avm = re.sub(
    r'val account = _accounts\.value\.find \{ it\.id == accountId \}\n.*?_accounts\.value = _accounts\.value\.map \{ if \(it\.id == accountId\) it\.copy\(encryptedPasscode = encrypted\) else it \}\n\s*\}',
    """val account = accounts.value.find { it.id == accountId }
            if (account != null) {
                val encrypted = newPasscode?.let { com.example.data.CryptoManager.encrypt(it) }
                repository.insertAccount(account.copy(encryptedPasscode = encrypted))
            }""",
    avm,
    flags=re.DOTALL
)

with open('app/src/main/java/com/example/ui/AppViewModel.kt', 'w') as f:
    f.write(avm)

