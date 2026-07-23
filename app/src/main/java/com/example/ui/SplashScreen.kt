package com.example.ui

import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import kotlinx.coroutines.delay

@Composable
fun SplashScreen(onSplashFinished: () -> Unit) {
    var startAnimation by remember { mutableStateOf(false) }

    LaunchedEffect(Unit) {
        startAnimation = true
        delay(2000)
        onSplashFinished()
    }

    val icebergYOffset by animateFloatAsState(
        targetValue = if (startAnimation) 0f else 1f,
        animationSpec = tween(durationMillis = 1500, easing = FastOutSlowInEasing),
        label = "icebergYOffset"
    )
    
    val alphaAnim by animateFloatAsState(
        targetValue = if (startAnimation) 1f else 0f,
        animationSpec = tween(durationMillis = 1000),
        label = "alphaAnim"
    )

    Canvas(modifier = Modifier.fillMaxSize().background(Color(0xFF0A1B2A))) {
        val w = size.width
        val h = size.height
        val waterLevel = h * 0.65f
        
        // Background ice mountains (Antarctica)
        val bgMountains = Path().apply {
            moveTo(0f, waterLevel)
            lineTo(w * 0.15f, waterLevel - h * 0.1f)
            lineTo(w * 0.35f, waterLevel)
            lineTo(w * 0.65f, waterLevel - h * 0.15f)
            lineTo(w * 0.85f, waterLevel - h * 0.05f)
            lineTo(w, waterLevel)
            lineTo(w, h)
            lineTo(0f, h)
            close()
        }
        drawPath(bgMountains, Color(0xFF162A40).copy(alpha = alphaAnim))

        // Emerging Iceberg
        val icebergHeight = h * 0.35f
        val currentY = waterLevel + (icebergHeight * icebergYOffset)
        
        val iceberg = Path().apply {
            moveTo(w * 0.2f, waterLevel)
            lineTo(w * 0.35f, currentY - icebergHeight * 0.5f)
            lineTo(w * 0.5f, currentY - icebergHeight)
            lineTo(w * 0.65f, currentY - icebergHeight * 0.7f)
            lineTo(w * 0.8f, waterLevel)
            close()
        }
        
        // Iceberg shading
        val icebergShadow = Path().apply {
            moveTo(w * 0.5f, currentY - icebergHeight)
            lineTo(w * 0.65f, currentY - icebergHeight * 0.7f)
            lineTo(w * 0.8f, waterLevel)
            lineTo(w * 0.5f, waterLevel)
            close()
        }

        drawPath(iceberg, Color(0xFFD9F1FF).copy(alpha = alphaAnim))
        drawPath(icebergShadow, Color(0xFFA6D8FF).copy(alpha = alphaAnim))

        // Water
        val water = Path().apply {
            moveTo(0f, waterLevel)
            lineTo(w, waterLevel)
            lineTo(w, h)
            lineTo(0f, h)
            close()
        }
        drawPath(water, Color(0xFF00447A).copy(alpha = 0.9f * alphaAnim))
        
        // Water reflections
        drawRect(
            color = Color(0xFFD9F1FF).copy(alpha = 0.2f * alphaAnim),
            topLeft = Offset(w * 0.25f, waterLevel),
            size = Size(w * 0.5f, h * 0.1f)
        )
    }
}
