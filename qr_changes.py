import re

with open('app/src/main/java/com/example/ui/MyProfileScreen.kt', 'r') as f:
    content = f.read()

# Replace the two icons in the top bar with just one
content = re.sub(
    r'IconButton\(onClick = \{ showQrDialog = true \}\) \{\s*Icon\(Icons\.Filled\.QrCode, contentDescription = "QR Code"\)\s*\}\s*IconButton\(onClick = \{ /\* Scan \*/ \}\) \{\s*Icon\(Icons\.Filled\.QrCodeScanner, contentDescription = "Scan QR"\)\s*\}',
    r'IconButton(onClick = { showQrDialog = true }) {\n                        Icon(Icons.Filled.QrCode, contentDescription = "QR Code")\n                    }',
    content
)

# And in the non-top bar section:
content = re.sub(
    r'IconButton\(\s*onClick = \{ showQrDialog = true \},\s*modifier = Modifier\s*\.background\(Color\.Black\.copy\(alpha = 0\.3f\), CircleShape\)\s*\) \{\s*Icon\(Icons\.Filled\.QrCode, contentDescription = "QR Code", tint = Color\.White\)\s*\}\s*Spacer\(Modifier\.width\(8\.dp\)\)\s*IconButton\(\s*onClick = \{ /\* Scan \*/ \},\s*modifier = Modifier\s*\.background\(Color\.Black\.copy\(alpha = 0\.3f\), CircleShape\)\s*\) \{\s*Icon\(Icons\.Filled\.QrCodeScanner, contentDescription = "Scan QR", tint = Color\.White\)\s*\}',
    r'IconButton(\n                        onClick = { showQrDialog = true },\n                        modifier = Modifier\n                            .background(Color.Black.copy(alpha = 0.3f), CircleShape)\n                    ) {\n                        Icon(Icons.Filled.QrCode, contentDescription = "QR Code", tint = Color.White)\n                    }',
    content
)

with open('app/src/main/java/com/example/ui/MyProfileScreen.kt', 'w') as f:
    f.write(content)
