package com.example.ui

import androidx.compose.animation.core.*
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.RadioButtonUnchecked
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.drawscope.clipRect
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import kotlin.math.sin

data class CacheCategory(
    val name: String,
    val sizeMb: Float,
    val color: Color,
    val isSelected: Boolean = true
)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsStorageScreen(viewModel: AppViewModel, navController: NavController) {
    var categories by remember {
        mutableStateOf(
            listOf(
                CacheCategory("Photos", 15.2f, Color(0xFF4CAF50)),
                CacheCategory("Videos", 45.8f, Color(0xFF2196F3)),
                CacheCategory("Music", 8.4f, Color(0xFF9C27B0)),
                CacheCategory("Other files", 2.1f, Color(0xFFFFC107))
            )
        )
    }

    var isClearing by remember { mutableStateOf(false) }
    var clearProgress by remember { mutableStateOf(0f) }
    val scope = rememberCoroutineScope()

    val totalSelectedSize = categories.filter { it.isSelected }.sumOf { it.sizeMb.toDouble() }.toFloat()
    val totalSize = categories.sumOf { it.sizeMb.toDouble() }.toFloat()

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Data and Storage") },
                navigationIcon = { 
                    IconButton(onClick = { navController.popBackStack() }) { 
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, "Back") 
                    } 
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .padding(padding)
                .fillMaxSize()
        ) {

            // Usage overview
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(32.dp),
                contentAlignment = Alignment.Center
            ) {
                Canvas(modifier = Modifier.size(200.dp)) {
                    var startAngle = -90f
                    val strokeWidth = 32.dp.toPx()
                    
                    if (totalSize > 0) {
                        for (category in categories) {
                            val sweepAngle = (category.sizeMb / totalSize) * 360f
                            drawArc(
                                color = category.color,
                                startAngle = startAngle,
                                sweepAngle = sweepAngle,
                                useCenter = false,
                                style = androidx.compose.ui.graphics.drawscope.Stroke(width = strokeWidth)
                            )
                            startAngle += sweepAngle
                        }
                    } else {
                        drawArc(
                            color = Color.DarkGray,
                            startAngle = 0f,
                            sweepAngle = 360f,
                            useCenter = false,
                            style = androidx.compose.ui.graphics.drawscope.Stroke(width = strokeWidth)
                        )
                    }
                }
                
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Text(String.format("%.1f", totalSize), style = MaterialTheme.typography.displayMedium)
                    Text("MB", style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }

            // Categories list
            LazyColumn(
                modifier = Modifier.weight(1f)
            ) {
                items(categories) { category ->
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clickable {
                                categories = categories.map {
                                    if (it.name == category.name) it.copy(isSelected = !it.isSelected) else it
                                }
                            }
                            .padding(16.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Box(
                            modifier = Modifier
                                .size(16.dp)
                                .background(category.color, shape = androidx.compose.foundation.shape.CircleShape)
                        )
                        Spacer(modifier = Modifier.width(16.dp))
                        Text(category.name, modifier = Modifier.weight(1f), style = MaterialTheme.typography.bodyLarge)
                        Text(String.format("%.1f MB", category.sizeMb), style = MaterialTheme.typography.bodyMedium)
                        Spacer(modifier = Modifier.width(16.dp))
                        Icon(
                            imageVector = if (category.isSelected) Icons.Filled.CheckCircle else Icons.Filled.RadioButtonUnchecked,
                            contentDescription = null,
                            tint = if (category.isSelected) MaterialTheme.colorScheme.primary else Color.Gray
                        )
                    }
                }
            }

            // Clear Cache Animation Area
            if (isClearing) {
                CacheClearAnimation(
                    progress = clearProgress,
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(60.dp)
                        .padding(horizontal = 16.dp)
                )
            } else {
                Button(
                    onClick = {
                        if (totalSelectedSize > 0) {
                            isClearing = true
                            clearProgress = 0f
                            scope.launch {
                                // Animate clearing progress
                                val steps = 100
                                for (i in 0..steps) {
                                    clearProgress = i / steps.toFloat()
                                    delay(20) // 2s total animation
                                }
                                delay(500)
                                // Update categories sizes (set cleared ones to 0)
                                categories = categories.map {
                                    if (it.isSelected) it.copy(sizeMb = 0f) else it
                                }
                                isClearing = false
                            }
                        }
                    },
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp),
                    enabled = totalSelectedSize > 0
                ) {
                    Text("Clear Cache (${String.format("%.1f MB", totalSelectedSize)})")
                }
            }
            Spacer(modifier = Modifier.height(16.dp))
        }
    }
}

@Composable
fun CacheClearAnimation(progress: Float, modifier: Modifier = Modifier) {
    val infiniteTransition = rememberInfiniteTransition(label = "flame")
    val time by infiniteTransition.animateFloat(
        initialValue = 0f,
        targetValue = 10f,
        animationSpec = infiniteRepeatable(tween(2000, easing = LinearEasing)),
        label = "time"
    )

    Canvas(modifier = modifier) {
        val w = size.width
        val h = size.height
        val corner = CornerRadius(h / 2, h / 2)
        
        // Background track (trash to be cleared)
        drawRoundRect(
            color = Color.DarkGray,
            size = Size(w, h),
            cornerRadius = corner
        )

        val clearWidth = w * progress

        // Draw cleared portion (green or primary color)
        clipRect(right = clearWidth) {
            drawRoundRect(
                color = Color(0xFF4CAF50),
                size = Size(w, h),
                cornerRadius = corner
            )
        }

        // Draw flame at the front line of clearing progress
        if (progress > 0f && progress < 1f) {
            val flameX = clearWidth
            val flameYOffset = sin(time * 10f) * (h * 0.2f)
            
            // Flame Path (simple animated triangle/drop)
            val flamePath = Path().apply {
                moveTo(flameX, h * 0.9f)
                quadraticBezierTo(
                    flameX + h * 0.5f + sin(time * 15f) * h * 0.2f, h * 0.5f,
                    flameX, -h * 0.2f + flameYOffset
                )
                quadraticBezierTo(
                    flameX - h * 0.5f + sin(time * 12f) * h * 0.2f, h * 0.5f,
                    flameX, h * 0.9f
                )
                close()
            }
            
            // Inner flame
            val innerFlamePath = Path().apply {
                moveTo(flameX, h * 0.8f)
                quadraticBezierTo(
                    flameX + h * 0.3f + sin(time * 20f) * h * 0.1f, h * 0.6f,
                    flameX, h * 0.1f + flameYOffset * 0.5f
                )
                quadraticBezierTo(
                    flameX - h * 0.3f + sin(time * 18f) * h * 0.1f, h * 0.6f,
                    flameX, h * 0.8f
                )
                close()
            }

            drawPath(flamePath, color = Color(0xFFFF5722)) // Outer Orange Red
            drawPath(innerFlamePath, color = Color(0xFFFFEB3B)) // Inner Yellow
        }
    }
}
