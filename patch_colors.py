import re

with open('app/src/main/java/com/example/ui/SettingsScreens.kt', 'r') as f:
    content = f.read()

colors_regex = re.compile(r'(val isDarkThemeEnabled by viewModel\.isDarkThemeEnabled\.collectAsState\(\))')
content = colors_regex.sub(r'\1\n    val isQrSnowflakesEnabled by viewModel.isQrSnowflakesEnabled.collectAsState()', content)

dark_theme_regex = re.compile(r'(Text\("Global Dark Theme", style = MaterialTheme\.typography\.bodyLarge\)\n\s*Switch\(\n\s*checked = isDarkThemeEnabled,\n\s*onCheckedChange = \{ viewModel\.setDarkThemeEnabled\(it\) \}\n\s*\)\n\s*\})')
content = dark_theme_regex.sub(r'\1\n            Row(\n                modifier = Modifier.fillMaxWidth().padding(16.dp),\n                horizontalArrangement = Arrangement.SpaceBetween,\n                verticalAlignment = Alignment.CenterVertically\n            ) {\n                Text("QR Code Snowflakes", style = MaterialTheme.typography.bodyLarge)\n                Switch(\n                    checked = isQrSnowflakesEnabled,\n                    onCheckedChange = { viewModel.setQrSnowflakesEnabled(it) }\n                )\n            }', content)

with open('app/src/main/java/com/example/ui/SettingsScreens.kt', 'w') as f:
    f.write(content)
