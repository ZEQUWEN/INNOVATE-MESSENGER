with open('app/src/main/java/com/example/ui/SettingsScreens.kt', 'r') as f:
    ss = f.read()

if ss.startswith('import androidx.compose.ui.text.font.FontWeight\npackage com.example.ui\n'):
    ss = ss.replace('import androidx.compose.ui.text.font.FontWeight\npackage com.example.ui\n', 'package com.example.ui\nimport androidx.compose.ui.text.font.FontWeight\n')
elif ss.startswith('import androidx.compose.ui.text.font.FontWeight\n'):
    ss = ss.replace('import androidx.compose.ui.text.font.FontWeight\n', '')
    ss = ss.replace('package com.example.ui\n', 'package com.example.ui\nimport androidx.compose.ui.text.font.FontWeight\n')

with open('app/src/main/java/com/example/ui/SettingsScreens.kt', 'w') as f:
    f.write(ss)

