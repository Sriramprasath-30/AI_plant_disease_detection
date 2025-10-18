# -*- coding: utf-8 -*-

"""
Smart Plant Monitoring System - Raspberry Pi Script
- Reads sensors from Arduino UNO via serial
- Captures plant image via Pi Camera
- Sends updates and images to Telegram bot
- Can forward images to a CNN server for disease detection
"""

import asyncio
import serial
from datetime import datetime
from picamera2 import Picamera2
import telegram
import requests
import os

# ====== Configuration ======
BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
CHAT_ID = 'YOUR_TELEGRAM_CHAT_ID'

SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600

IMAGE_FOLDER = '/home/pi/smartplant_images'
CNN_SERVER_URL = 'http://your_cnn_server/upload'  # Optional

# Create image folder if not exists
os.makedirs(IMAGE_FOLDER, exist_ok=True)

# Initialize Telegram bot
bot = telegram.Bot(token=BOT_TOKEN)

# Initialize Serial connection to Arduino
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

# Initialize Pi Camera
picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration())
picam2.start()
asyncio.sleep(2)  # Camera warm-up

# ====== Helper Functions ======
def parse_sensor_data(lines):
    """
    Parse Arduino serial output into dictionary
    """
    data = {}
    for line in lines:
        line = line.strip()
        if line.startswith("Temperature:"):
            data['temp'] = line.split(":")[1].strip().split()[0]
        elif line.startswith("Humidity:"):
            data['humidity'] = line.split(":")[1].strip().split()[0]
        elif line.startswith("Soil Moisture:"):
            data['soil'] = line.split(":")[1].strip()
        elif line.startswith("LDR Value:"):
            data['ldr'] = line.split(":")[1].strip()
        elif "Pump ON" in line:
            data['pump'] = "ON"
        elif "Pump OFF" in line:
            data['pump'] = "OFF"
    return data

def read_serial_data(timeout=3):
    """
    Read sensor data from Arduino for a few seconds
    """
    start_time = datetime.now()
    lines = []
    while (datetime.now() - start_time).seconds < timeout:
        if ser.in_waiting:
            line = ser.readline().decode('utf-8', errors='ignore')
            if line.strip():
                lines.append(line)
    return parse_sensor_data(lines)

def capture_image():
    """
    Capture image using Pi Camera and save with timestamp
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = os.path.join(IMAGE_FOLDER, f"plant_{timestamp}.jpg")
    picam2.capture_file(image_path)
    return image_path

async def send_telegram(sensor_data, image_path):
    """
    Send sensor data and plant image to Telegram
    """
    soil_value = sensor_data.get('soil')
    try:
        soil_level = int(soil_value)
        if soil_level > 500:
            water_msg = "Soil is dry. Please water the plant."
        else:
            water_msg = "Soil is wet. No watering needed."
    except (ValueError, TypeError):
        water_msg = "Soil moisture data unavailable."

    message = (
        "🌿 Smart Plant Monitor Update 🌿\n\n"
        f"🌡 Temperature: {sensor_data.get('temp', 'N/A')} °C\n"
        f"💧 Humidity: {sensor_data.get('humidity', 'N/A')} %\n"
        f"🌱 Soil Moisture: {sensor_data.get('soil', 'N/A')}\n"
        f"🔆 Light Level (LDR): {sensor_data.get('ldr', 'N/A')}\n"
        f"💦 Pump Status: {sensor_data.get('pump', 'N/A')}\n\n"
        f"{water_msg}\n\n"
        f"📸 Plant Image attached."
    )

    await bot.send_message(chat_id=CHAT_ID, text=message)

    with open(image_path, 'rb') as photo:
        await bot.send_photo(chat_id=CHAT_ID, photo=photo)

def send_to_cnn_server(image_path):
    """
    Optionally send captured image to external CNN server
    """
    try:
        with open(image_path, 'rb') as img_file:
            files = {'file': img_file}
            response = requests.post(CNN_SERVER_URL, files=files, timeout=10)
        return response.json()  # Expect JSON with disease info
    except Exception as e:
        print(f"CNN Server Error: {e}")
        return None

# ====== Main Loop ======
async def main():
    while True:
        # Read sensor data from Arduino
        sensor_data = read_serial_data()

        # Capture image
        image_path = capture_image()

        # Optionally send to CNN server
        cnn_result = send_to_cnn_server(image_path)
        if cnn_result:
            print("CNN Server Result:", cnn_result)

        # Send update to Telegram
        await send_telegram(sensor_data, image_path)

        print("Update sent! Waiting for next cycle...")
        await asyncio.sleep(300)  # Wait 5 minutes before next update

if __name__ == "__main__":
    asyncio.run(main())
