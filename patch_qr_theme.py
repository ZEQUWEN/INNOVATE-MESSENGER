import re

with open('app/src/main/java/com/example/ui/MyProfileScreen.kt', 'r') as f:
    content = f.read()

content = content.replace("val activeAccount = LocalActiveAccount.current ?: return", 
"""val activeAccount = LocalActiveAccount.current ?: return
    val isQrSnowflakesEnabled by viewModel.isQrSnowflakesEnabled.collectAsState()""")

# We need to wrap the contents of the ModalBottomSheet in a Box with the gradient and snowflakes.
# The ModalBottomSheet content starts at `var selectedThemeIndex`
sheet_content_regex = re.compile(r'(ModalBottomSheet\(\n\s*onDismissRequest = \{ showQrDialog = false \},\n\s*sheetState = rememberModalBottomSheetState\(skipPartiallyExpanded = true\)\n\s*\) \{)(.*?)\n\s*if \(showChangeNumberDialog\)', re.DOTALL)

def replacer(match):
    start_tag = match.group(1)
    body = match.group(2)
    
    new_body = """
                Box(modifier = Modifier.fillMaxWidth().fillMaxHeight(0.85f)) {
                    // Iridescent Gradient
                    val infiniteTransition = rememberInfiniteTransition()
                    val gradientOffset by infiniteTransition.animateFloat(
                        initialValue = 0f,
                        targetValue = 1000f,
                        animationSpec = infiniteRepeatable(
                            animation = tween(10000, easing = LinearEasing),
                            repeatMode = RepeatMode.Reverse
                        )
                    )
                    Box(
                        modifier = Modifier.fillMaxSize().background(
                            Brush.linearGradient(
                                colors = listOf(
                                    Color(0xFFE0C3FC).copy(alpha = 0.5f),
                                    Color(0xFF8EC5FC).copy(alpha = 0.5f),
                                    Color(0xFFE0C3FC).copy(alpha = 0.5f)
                                ),
                                start = Offset(gradientOffset, gradientOffset),
                                end = Offset(gradientOffset + 500f, gradientOffset + 500f)
                            )
                        )
                    )
                    
                    if (isQrSnowflakesEnabled) {
                        val snowflakes = remember { List(30) { com.example.ui.Snowflake() } }
                        var dt by remember { mutableStateOf(0f) }
                        var lastTime by remember { mutableStateOf(0L) }
                        LaunchedEffect(Unit) {
                            while (kotlinx.coroutines.isActive) {
                                androidx.compose.runtime.withFrameNanos { time ->
                                    if (lastTime != 0L) {
                                        dt = (time - lastTime) / 1_000_000_000f
                                    }
                                    lastTime = time
                                }
                            }
                        }
                        androidx.compose.foundation.Canvas(modifier = Modifier.fillMaxSize()) {
                            val currentDt = dt
                            snowflakes.forEach { flake ->
                                flake.update(size.width, size.height, currentDt)
                                drawCircle(
                                    color = Color.White.copy(alpha = flake.alpha),
                                    center = Offset(flake.x, flake.y),
                                    radius = flake.radius
                                )
                            }
                        }
                    }
                    
                    Column(modifier = Modifier.fillMaxSize()) {
""" + body + """
                    }
                }
        }
"""
    return start_tag + new_body

content = sheet_content_regex.sub(replacer, content)

with open('app/src/main/java/com/example/ui/MyProfileScreen.kt', 'w') as f:
    f.write(content)
