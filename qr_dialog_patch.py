import re

with open('app/src/main/java/com/example/ui/MyProfileScreen.kt', 'r') as f:
    content = f.read()

qr_dialog_regex = re.compile(r'if \(showQrDialog\) \{.*?\n        \}\n        \n        if \(showChangeNumberDialog\)', re.DOTALL)

new_qr_dialog = """if (showQrDialog) {
            ModalBottomSheet(
                onDismissRequest = { showQrDialog = false },
                sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
            ) {
                var selectedThemeIndex by remember { mutableStateOf(0) }
                val themes = listOf(
                    Triple(Color.White, Color(0xFF1E88E5), Color(0xFFE3F2FD)), // Blue
                    Triple(Color(0xFF202020), Color(0xFFFF9800), Color(0xFF3E2723)), // Orange/Dark
                    Triple(Color(0xFF101010), Color(0xFFE91E63), Color(0xFF4A148C)), // Pink/Purple
                    Triple(Color(0xFF002200), Color(0xFF00E676), Color(0xFF1B5E20)), // Green
                    Triple(Color.White, Color(0xFF673AB7), Color(0xFFEDE7F6))  // Purple/Light
                )
                val currentTheme = themes[selectedThemeIndex]
                
                val qrBitmap = remember(activeAccount.username, currentTheme) {
                    com.example.utils.generateQrCode(
                        text = "tg://resolve?domain=${activeAccount.username}",
                        fgColor = android.graphics.Color.argb(
                            (currentTheme.second.alpha * 255).toInt(),
                            (currentTheme.second.red * 255).toInt(),
                            (currentTheme.second.green * 255).toInt(),
                            (currentTheme.second.blue * 255).toInt()
                        ),
                        bgColor = android.graphics.Color.argb(
                            (currentTheme.first.alpha * 255).toInt(),
                            (currentTheme.first.red * 255).toInt(),
                            (currentTheme.first.green * 255).toInt(),
                            (currentTheme.first.blue * 255).toInt()
                        )
                    )
                }
                var showScanner by remember { mutableStateOf(false) }

                androidx.compose.animation.AnimatedContent(
                    targetState = showScanner,
                    label = "qr_scanner_transition"
                ) { isScanner ->
                    if (isScanner) {
                        Column(
                            modifier = Modifier.fillMaxWidth().height(550.dp),
                            horizontalAlignment = Alignment.CenterHorizontally,
                            verticalArrangement = Arrangement.Center
                        ) {
                            Text("Сканировать QR-код", style = MaterialTheme.typography.titleLarge)
                            Spacer(Modifier.height(32.dp))
                            Box(
                                modifier = Modifier
                                    .size(250.dp)
                                    .border(2.dp, MaterialTheme.colorScheme.primary, RoundedCornerShape(16.dp))
                                    .background(Color.Black.copy(alpha = 0.8f), RoundedCornerShape(16.dp)),
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(Icons.Filled.QrCodeScanner, contentDescription = null, modifier = Modifier.size(64.dp), tint = Color.White)
                                // Add scanning line animation?
                            }
                            Spacer(Modifier.height(32.dp))
                            Button(
                                onClick = { showScanner = false },
                                modifier = Modifier.fillMaxWidth(0.8f).height(50.dp)
                            ) {
                                Text("Мой QR-код", fontSize = 16.sp)
                            }
                        }
                    } else {
                        Column(
                            modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp),
                            horizontalAlignment = Alignment.CenterHorizontally
                        ) {
                            // QR Code Card
                            Box(
                                modifier = Modifier
                                    .fillMaxWidth(0.75f)
                                    .aspectRatio(0.65f)
                                    .clip(RoundedCornerShape(24.dp))
                                    .background(currentTheme.third),
                                contentAlignment = Alignment.Center
                            ) {
                                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                                    if (activeAccount.profilePicUrl.isNotEmpty()) {
                                        coil.compose.AsyncImage(
                                            model = activeAccount.profilePicUrl,
                                            contentDescription = null,
                                            modifier = Modifier.size(64.dp).clip(CircleShape).border(2.dp, currentTheme.first, CircleShape),
                                            contentScale = androidx.compose.ui.layout.ContentScale.Crop
                                        )
                                    } else {
                                        Box(
                                            modifier = Modifier.size(64.dp).clip(CircleShape).background(MaterialTheme.colorScheme.primary).border(2.dp, currentTheme.first, CircleShape),
                                            contentAlignment = Alignment.Center
                                        ) {
                                            Text(
                                                activeAccount.displayName.take(1).uppercase(),
                                                color = MaterialTheme.colorScheme.onPrimary,
                                                style = MaterialTheme.typography.headlineMedium
                                            )
                                        }
                                    }
                                    Spacer(Modifier.height(16.dp))
                                    qrBitmap?.let { bmp ->
                                        androidx.compose.foundation.Image(
                                            bitmap = bmp.asImageBitmap(),
                                            contentDescription = "QR Code",
                                            modifier = Modifier
                                                .size(200.dp)
                                                .clip(RoundedCornerShape(16.dp))
                                        )
                                    }
                                    Spacer(Modifier.height(16.dp))
                                    Text(
                                        "@${activeAccount.username}",
                                        style = MaterialTheme.typography.titleLarge,
                                        fontWeight = FontWeight.Bold,
                                        color = currentTheme.second
                                    )
                                }
                            }

                            Spacer(Modifier.height(24.dp))

                            // Controls Row
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Text("QR-код", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                                
                                IconButton(onClick = { showScanner = true }) {
                                    Icon(Icons.Filled.QrCodeScanner, contentDescription = "Scan QR", tint = MaterialTheme.colorScheme.primary)
                                }
                            }

                            Spacer(Modifier.height(16.dp))

                            // Theme selector
                            androidx.compose.foundation.lazy.LazyRow(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.spacedBy(12.dp)
                            ) {
                                items(themes.size) { index ->
                                    val theme = themes[index]
                                    val isSelected = selectedThemeIndex == index
                                    Box(
                                        modifier = Modifier
                                            .size(64.dp, 80.dp)
                                            .clip(RoundedCornerShape(12.dp))
                                            .background(theme.third)
                                            .border(
                                                width = if (isSelected) 2.dp else 1.dp,
                                                color = if (isSelected) MaterialTheme.colorScheme.primary else Color.Gray.copy(alpha = 0.5f),
                                                shape = RoundedCornerShape(12.dp)
                                            )
                                            .clickable { selectedThemeIndex = index },
                                        contentAlignment = Alignment.Center
                                    ) {
                                        Icon(
                                            Icons.Filled.QrCode, 
                                            contentDescription = null, 
                                            tint = theme.second,
                                            modifier = Modifier.size(32.dp)
                                        )
                                    }
                                }
                            }

                            Spacer(Modifier.height(32.dp))

                            Button(
                                onClick = { /* Share QR */ },
                                modifier = Modifier.fillMaxWidth().height(50.dp)
                            ) {
                                Text("Поделиться", fontSize = 16.sp)
                            }
                            
                            Spacer(Modifier.height(16.dp))
                        }
                    }
                }
            }
        }
        
        if (showChangeNumberDialog)"""

content = qr_dialog_regex.sub(new_qr_dialog, content)

with open('app/src/main/java/com/example/ui/MyProfileScreen.kt', 'w') as f:
    f.write(content)
