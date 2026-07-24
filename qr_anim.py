import re

with open('app/src/main/java/com/example/ui/MyProfileScreen.kt', 'r') as f:
    content = f.read()

# Add animation imports
if "import androidx.compose.animation.core.animateFloat" not in content:
    content = content.replace("import androidx.compose.animation.AnimatedContent", "import androidx.compose.animation.AnimatedContent\nimport androidx.compose.animation.core.*\nimport androidx.compose.ui.geometry.Offset\nimport androidx.compose.ui.graphics.Brush")

scanner_regex = re.compile(r'Box\(\s*modifier = Modifier\s*\.size\(250\.dp\)\s*\.border\(2\.dp, MaterialTheme\.colorScheme\.primary, RoundedCornerShape\(16\.dp\)\)\s*\.background\(Color\.Black\.copy\(alpha = 0\.8f\), RoundedCornerShape\(16\.dp\)\),\s*contentAlignment = Alignment\.Center\s*\) \{\s*Icon\(Icons\.Filled\.QrCodeScanner, contentDescription = null, modifier = Modifier\.size\(64\.dp\), tint = Color\.White\)\s*// Add scanning line animation\?\s*\}')

new_scanner = """val infiniteTransition = rememberInfiniteTransition()
                            val scanAnim by infiniteTransition.animateFloat(
                                initialValue = 0f,
                                targetValue = 250f,
                                animationSpec = infiniteRepeatable(
                                    animation = tween(2000, easing = LinearEasing),
                                    repeatMode = RepeatMode.Reverse
                                )
                            )
                            
                            Box(
                                modifier = Modifier
                                    .size(250.dp)
                                    .border(2.dp, MaterialTheme.colorScheme.primary, RoundedCornerShape(16.dp))
                                    .background(Color.Black.copy(alpha = 0.8f), RoundedCornerShape(16.dp)),
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(Icons.Filled.QrCodeScanner, contentDescription = null, modifier = Modifier.size(64.dp), tint = Color.White.copy(alpha = 0.3f))
                                
                                androidx.compose.foundation.Canvas(modifier = Modifier.fillMaxSize()) {
                                    val y = scanAnim.dp.toPx()
                                    drawLine(
                                        color = androidx.compose.ui.graphics.Color(0xFF00E676),
                                        start = Offset(0f, y),
                                        end = Offset(size.width, y),
                                        strokeWidth = 4.dp.toPx()
                                    )
                                    drawRect(
                                        brush = Brush.verticalGradient(
                                            colors = listOf(Color.Transparent, androidx.compose.ui.graphics.Color(0xFF00E676).copy(alpha = 0.3f)),
                                            startY = y - 40.dp.toPx(),
                                            endY = y
                                        ),
                                        topLeft = Offset(0f, y - 40.dp.toPx()),
                                        size = androidx.compose.ui.geometry.Size(size.width, 40.dp.toPx())
                                    )
                                }
                            }"""

content = scanner_regex.sub(new_scanner, content)

with open('app/src/main/java/com/example/ui/MyProfileScreen.kt', 'w') as f:
    f.write(content)
