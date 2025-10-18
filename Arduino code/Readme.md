# Smart Plant Incubator System with Automatic Watering and Lighting

## Overview

This project is a **Smart Plant Incubator System** designed to automatically monitor and manage the **watering and lighting** requirements of plants. The system uses an **Arduino UNO** in combination with sensors to maintain optimal plant conditions. It also tracks daily light exposure to ensure plants receive the minimum required light for healthy growth.

The code monitors:

- **Temperature** and **Humidity** using a DHT22 sensor  
- **Soil moisture** using a soil moisture sensor  
- **Ambient light intensity** using an LDR sensor  

Based on these readings, it automatically controls:

- A **water pump** for irrigation  
- Incubator **lights** for artificial lighting  

The system ensures plants are watered only when needed and receive sufficient light while preventing overexposure.

---

## Features

- Automatic **watering** based on soil moisture levels.  
- Automatic **lighting** based on ambient light and minimum/maximum daily light requirements.  
- Tracks **total light duration** per day and resets every 24 hours.  
- Serial monitoring of **temperature, humidity, soil moisture, light intensity**, and device status.  
- Active LOW relays used to control both the **water pump** and **lights**.  

---

## Hardware Requirements

| Component | Description | Connection |
|-----------|-------------|------------|
| Arduino UNO | Microcontroller board | USB connection to PC/Raspberry Pi |
| DHT22 Sensor | Temperature & Humidity sensor | Data Pin → **D2**, VCC → 5V, GND → GND |
| Soil Moisture Sensor | Measures soil moisture | Analog Pin → **A0**, VCC → 5V, GND → GND |
| LDR Sensor | Measures ambient light | Analog Pin → **A1**, voltage divider with resistor, VCC → 5V, GND → GND |
| Water Pump | Pump for irrigation | Relay Module Input → **D8**, Relay VCC → 5V, GND → GND; Pump connected to relay NO/COM terminals |
| Incubator Lights | Artificial light source | Relay Module Input → **D9**, Relay VCC → 5V, GND → GND; Lights connected to relay NO/COM terminals |
| Relay Module | Controls high-power devices | Connected to Arduino digital pins (D8, D9) |

**Notes:**

- Relays are **active LOW** → device turns ON when the pin is LOW.  
- Analog readings from soil moisture and LDR determine thresholds for watering and lighting.  
- Ensure proper power supply to pump and lights; relay isolates high-voltage devices from Arduino.  

---


**High-power devices through Relay:**

- Water Pump → Relay NO/COM  
- Incubator Lights → Relay NO/COM  

---

## Code Functionality

1. **Sensor Readings**:  
   - `DHT22` reads temperature (°C) and humidity (%)  
   - Soil moisture sensor reads analog value (0–1023)  
   - LDR sensor reads ambient light (0–1023)  

2. **Water Pump Control**:  
   - If soil moisture < `SOIL_DRY_THRESHOLD`, pump turns ON  
   - Otherwise, pump remains OFF  

3. **Lighting Control**:  
   - Lights turn ON if ambient light < `LDR_DARK_THRESHOLD` and minimum daily light not met  
   - Lights turn OFF if ambient light > `LDR_BRIGHT_THRESHOLD` and minimum daily light requirement met  
   - Lights are forced OFF if maximum daily light limit is reached  

4. **Daily Light Tracking**:  
   - Tracks total light duration  
   - Resets every 24 hours  

5. **Serial Monitoring**:  
   - Outputs temperature, humidity, soil moisture, LDR value, pump status, light status, and total light time  

---

## Thresholds (Adjustable)

| Sensor / Device | Threshold / Timing |
|-----------------|-----------------|
| Soil Moisture | `SOIL_DRY_THRESHOLD = 500` |
| LDR Dark | `LDR_DARK_THRESHOLD = 300` |
| LDR Bright | `LDR_BRIGHT_THRESHOLD = 400` |
| Minimum Light Time | `MIN_LIGHT_ON_TIME = 8 hours` |
| Maximum Light Time | `MAX_LIGHT_ON_TIME = 16 hours` |

> Thresholds can be calibrated based on your plants and sensor characteristics.

---

## How to Use

1. Connect all hardware components as per the diagram.  
2. Upload the `plant_incubator.c` sketch to Arduino UNO via Arduino IDE.  
3. Open the **Serial Monitor** at 9600 baud to view sensor readings and device status.  
4. Adjust threshold values if necessary for your plant species.  
5. Power the pump and lights through the relays. The system will automatically maintain watering and lighting.

---

## Future Enhancements

- Connect to **Raspberry Pi** for IoT integration and remote monitoring.  
- Add a **Telegram or web-based interface** to monitor and control devices.  
- Use **machine learning** for predictive irrigation and light management based on plant type and growth stage.  


## Connections Summary

