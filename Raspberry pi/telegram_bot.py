# telegram_bot.py
# -*- coding: utf-8 -*-
"""
Enhanced Telegram Bot for Smart Plant Monitoring & Disease Detection System
Features:
- Interactive menu with bot commands
- Send sensor status updates
- Control water pump and UV lights
- Send disease reports (PDF with annotated images)
- Send prediction CSV and detection charts
- Send full frames report
- Trigger PC-based disease detection
"""

import telegram
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio
import os
from datetime import datetime

# ====== Configuration ======
BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'   # Replace with your bot token
CHAT_ID = 'YOUR_TELEGRAM_CHAT_ID'       # Replace with your chat ID

# File paths
DISEASE_REPORT_PDF = 'disease_report.pdf'
PREDICTIONS_CSV = 'disease_predictions.csv'
CONFIDENCE_CHART = 'confidence_chart.png'
DETECTION_CHART = 'detection_chart.png'
FULL_FRAMES_PDF = 'full_frames_report.pdf'

# Global variables for sensor data and control
latest_sensor_data = {}
pump_status = "OFF"
uv_light_status = "OFF"

# Initialize bot
bot = telegram.Bot(token=BOT_TOKEN)

# ====== Keyboard Layouts ======
def get_main_keyboard():
    """Create the main menu keyboard"""
    keyboard = [
        [KeyboardButton("🌿 Status"), KeyboardButton("💧 Water Now")],
        [KeyboardButton("☀️ Toggle UV"), KeyboardButton("📄 Send Report")],
        [KeyboardButton("📊 Send Chart"), KeyboardButton("📸 Send Full Frames")],
        [KeyboardButton("🖥️ Trigger PC Detection")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# ====== Bot Command Handlers ======
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    welcome_message = (
        "🌿 *Welcome to Smart Plant Bot!* 🌿\n\n"
        "I can help you monitor your plants and detect diseases.\n\n"
        "*Available Commands:*\n"
        "🌿 /status - Get current sensor readings\n"
        "💧 /water - Water the plant manually\n"
        "☀️ /toggle_uv - Toggle UV/grow lights\n"
        "📄 /report - Get disease detection report\n"
        "📊 /chart - Get detection charts\n"
        "📸 /frames - Get full frames report\n"
        "🖥️ /detect - Trigger disease detection\n\n"
        "Use the buttons below for quick access!"
    )
    await update.message.reply_text(
        welcome_message,
        parse_mode='Markdown',
        reply_markup=get_main_keyboard()
    )

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command - show current sensor readings"""
    temp = latest_sensor_data.get('temp', 'N/A')
    humidity = latest_sensor_data.get('humidity', 'N/A')
    soil = latest_sensor_data.get('soil', 'N/A')
    ldr = latest_sensor_data.get('ldr', 'N/A')
    
    # Determine soil status
    try:
        soil_value = int(soil)
        if soil_value > 500:
            soil_status = "🌵 Dry"
        else:
            soil_status = "💧 Wet"
    except (ValueError, TypeError):
        soil_status = "❓ Unknown"
    
    # Determine temperature status
    try:
        temp_value = float(temp)
        if temp_value < 15:
            temp_status = "❄️ Cold"
        elif temp_value > 30:
            temp_status = "🔥 Hot"
        else:
            temp_status = "✅ Normal"
    except (ValueError, TypeError):
        temp_status = "❓ Unknown"
    
    # Determine humidity status
    try:
        humidity_value = float(humidity)
        if humidity_value < 40:
            humidity_status = "🌵 Low"
        elif humidity_value > 70:
            humidity_status = "💦 High"
        else:
            humidity_status = "✅ Normal"
    except (ValueError, TypeError):
        humidity_status = "❓ Unknown"
    
    status_message = (
        "🌱 *Smart Plant Status*\n\n"
        f"🌡 *Temp:* {temp}°C — {temp_status} Temperature\n"
        f"💧 *Humidity:* {humidity}% — {humidity_status} Humidity\n"
        f"🌱 *Soil:* {soil} — {soil_status}\n"
        f"💡 *Light:* {ldr}\n"
        f"💦 *Pump:* {pump_status}\n"
        f"☀️ *UV:* {uv_light_status}\n\n"
        f"_Last updated: {datetime.now().strftime('%I:%M %p')}_"
    )
    
    await update.message.reply_text(
        status_message,
        parse_mode='Markdown',
        reply_markup=get_main_keyboard()
    )

async def water_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /water command - manually trigger watering"""
    global pump_status
    pump_status = "ON"
    
    message = (
        "💧 *Watering Plant*\n\n"
        "Water pump activated for 5 seconds...\n"
        "Please wait..."
    )
    await update.message.reply_text(message, parse_mode='Markdown')
    
    # TODO: Send command to Arduino/Raspberry Pi to activate pump
    # This would typically be done via serial communication or GPIO
    
    await asyncio.sleep(5)
    pump_status = "OFF"
    
    await update.message.reply_text(
        "✅ Watering complete!",
        reply_markup=get_main_keyboard()
    )

async def toggle_uv_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /toggle_uv command - toggle UV/grow lights"""
    global uv_light_status
    
    if uv_light_status == "OFF":
        uv_light_status = "ON"
        message = "☀️ *UV Lights:* ON\n\nGrow lights activated!"
    else:
        uv_light_status = "OFF"
        message = "🌙 *UV Lights:* OFF\n\nGrow lights deactivated!"
    
    # TODO: Send command to Arduino to toggle lights
    
    await update.message.reply_text(
        message,
        parse_mode='Markdown',
        reply_markup=get_main_keyboard()
    )

async def report_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /report command - send disease detection report"""
    await update.message.reply_text("📄 Generating disease report... Please wait.")
    
    # Send disease report PDF
    if os.path.exists(DISEASE_REPORT_PDF):
        with open(DISEASE_REPORT_PDF, 'rb') as pdf:
            await update.message.reply_document(
                document=pdf,
                filename="disease_report.pdf",
                caption="🔬 Plant Disease Detection Report"
            )
    else:
        await update.message.reply_text("❌ Disease report not found. Run detection first.")
    
    # Send predictions CSV
    if os.path.exists(PREDICTIONS_CSV):
        with open(PREDICTIONS_CSV, 'rb') as csv:
            await update.message.reply_document(
                document=csv,
                filename="disease_predictions.csv",
                caption="📊 Disease Prediction Data (CSV)"
            )
    else:
        await update.message.reply_text("❌ Predictions CSV not found.")
    
    await update.message.reply_text("✅ Report sent!", reply_markup=get_main_keyboard())

async def chart_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /chart command - send detection charts"""
    await update.message.reply_text("📊 Generating charts... Please wait.")
    
    charts_sent = 0
    
    # Send confidence chart
    if os.path.exists(CONFIDENCE_CHART):
        with open(CONFIDENCE_CHART, 'rb') as chart:
            await update.message.reply_photo(
                photo=chart,
                caption="📊 Average Disease Confidence\n\n"
                        "Shows confidence levels for:\n"
                        "• Healthy Leaf Rose\n"
                        "• Rose Rust\n"
                        "• Rose Sawfly Slug"
            )
        charts_sent += 1
    
    # Send detection chart
    if os.path.exists(DETECTION_CHART):
        with open(DETECTION_CHART, 'rb') as chart:
            await update.message.reply_photo(
                photo=chart,
                caption="📊 Total Disease Detections\n\n"
                        "Shows total number of detections for each disease type"
            )
        charts_sent += 1
    
    if charts_sent == 0:
        await update.message.reply_text(
            "❌ No charts found. Run detection first.",
            reply_markup=get_main_keyboard()
        )
    else:
        await update.message.reply_text(
            f"✅ {charts_sent} chart(s) sent!",
            reply_markup=get_main_keyboard()
        )

async def frames_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /frames command - send full frames report"""
    await update.message.reply_text("📸 Generating full frames report... Please wait.")
    
    if os.path.exists(FULL_FRAMES_PDF):
        with open(FULL_FRAMES_PDF, 'rb') as pdf:
            await update.message.reply_document(
                document=pdf,
                filename="full_frames_report.pdf",
                caption="📸 Full Frames Report\n\nComplete collection of captured plant images"
            )
        await update.message.reply_text("✅ Full frames report sent!", reply_markup=get_main_keyboard())
    else:
        await update.message.reply_text(
            "❌ Full frames report not found.",
            reply_markup=get_main_keyboard()
        )

async def detect_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /detect command - trigger PC-based disease detection"""
    message = (
        "🖥️ *Triggering Disease Detection*\n\n"
        "Starting analysis...\n"
        "• Capturing plant images 📸\n"
        "• Running AI detection model 🤖\n"
        "• Generating reports 📊\n\n"
        "This may take 1-2 minutes. Please wait..."
    )
    await update.message.reply_text(message, parse_mode='Markdown')
    
    # TODO: Trigger detection script on PC/Raspberry Pi
    # This would typically call your disease detection pipeline
    
    await asyncio.sleep(3)  # Simulate processing time
    
    await update.message.reply_text(
        "✅ Detection complete!\n\n"
        "Use /report to view the disease report\n"
        "Use /chart to view detection charts",
        reply_markup=get_main_keyboard()
    )

# ====== Direct Send Functions (for automated updates) ======
async def send_message(text: str):
    """Send a text message to the configured Telegram chat"""
    try:
        await bot.send_message(chat_id=CHAT_ID, text=text)
    except Exception as e:
        print(f"Failed to send message: {e}")

async def send_photo(photo_path: str, caption: str = None):
    """Send a photo with optional caption to Telegram"""
    if not os.path.exists(photo_path):
        print(f"Photo not found: {photo_path}")
        return
    
    try:
        with open(photo_path, 'rb') as photo:
            await bot.send_photo(chat_id=CHAT_ID, photo=photo, caption=caption)
    except Exception as e:
        print(f"Failed to send photo: {e}")

async def send_sensor_update(sensor_data: dict, image_path: str = None):
    """
    Send a formatted sensor update along with optional plant image
    This can be called from main_pi.py for automated updates
    """
    global latest_sensor_data
    latest_sensor_data = sensor_data
    
    # Build sensor message
    soil_value = sensor_data.get('soil')
    try:
        soil_level = int(soil_value)
        if soil_level > 500:
            water_msg = "🌵 Soil is dry. Watering activated."
        else:
            water_msg = "💧 Soil is wet. No watering needed."
    except (ValueError, TypeError):
        water_msg = "❓ Soil moisture data unavailable."
    
    message = (
        "🌿 *Smart Plant Monitor Update* 🌿\n\n"
        f"🌡 *Temperature:* {sensor_data.get('temp', 'N/A')} °C\n"
        f"💧 *Humidity:* {sensor_data.get('humidity', 'N/A')} %\n"
        f"🌱 *Soil Moisture:* {sensor_data.get('soil', 'N/A')}\n"
        f"🔆 *Light Level (LDR):* {sensor_data.get('ldr', 'N/A')}\n"
        f"💦 *Pump Status:* {sensor_data.get('pump', 'N/A')}\n"
        f"☀️ *UV Lights:* {sensor_data.get('lights', 'N/A')}\n\n"
        f"{water_msg}\n\n"
        f"_Updated: {datetime.now().strftime('%I:%M %p, %b %d')}_"
    )
    
    # Send text message
    await send_message(message)
    
    # Send photo if provided
    if image_path:
        await send_photo(image_path, caption="📸 Current Plant Image")

async def send_disease_report_auto():
    """
    Automatically send disease report after detection completes
    Call this from your detection script
    """
    message = "🔬 *Disease Detection Complete!*\n\nSending reports..."
    await send_message(message)
    
    # Send disease report PDF
    if os.path.exists(DISEASE_REPORT_PDF):
        with open(DISEASE_REPORT_PDF, 'rb') as pdf:
            await bot.send_document(
                chat_id=CHAT_ID,
                document=pdf,
                filename="disease_report.pdf",
                caption="🔬 Plant Disease Detection Report"
            )
    
    # Send predictions CSV
    if os.path.exists(PREDICTIONS_CSV):
        with open(PREDICTIONS_CSV, 'rb') as csv:
            await bot.send_document(
                chat_id=CHAT_ID,
                document=csv,
                filename="disease_predictions.csv",
                caption="📊 Disease Prediction Data (CSV)"
            )
    
    # Send charts
    if os.path.exists(CONFIDENCE_CHART):
        with open(CONFIDENCE_CHART, 'rb') as chart:
            await bot.send_photo(
                chat_id=CHAT_ID,
                photo=chart,
                caption="📊 Average Disease Confidence Chart"
            )
    
    if os.path.exists(DETECTION_CHART):
        with open(DETECTION_CHART, 'rb') as chart:
            await bot.send_photo(
                chat_id=CHAT_ID,
                photo=chart,
                caption="📊 Total Disease Detections Chart"
            )
    
    await send_message("✅ All reports sent successfully!")

# ====== Main Bot Application ======
def main():
    """Start the bot"""
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("water", water_command))
    application.add_handler(CommandHandler("toggle_uv", toggle_uv_command))
    application.add_handler(CommandHandler("report", report_command))
    application.add_handler(CommandHandler("chart", chart_command))
    application.add_handler(CommandHandler("frames", frames_command))
    application.add_handler(CommandHandler("detect", detect_command))
    
    print("🤖 Telegram bot started!")
    print("Waiting for commands...")
    
    # Start polling
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
