# 🌿 Smart Plant Monitoring and Disease Detection System

```The ECE Final year project;

**An IoT-based Intelligent Agricultural System Using Machine Learning**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Arduino](https://img.shields.io/badge/Arduino-C%2FC%2B%2B-00979D.svg)](https://www.arduino.cc/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.0+-FF6F00.svg)](https://www.tensorflow.org/)
[![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-3B%2B-C51A4A.svg)](https://www.raspberrypi.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Final Year Project - Bachelor of Engineering in Electronics and Communication Engineering**  
> Apollo Engineering College, Tamil Nadu (Affiliated to Anna University, Chennai)  
> May 2025

---

## 📖 Abstract

This project implements an **IoT-based plant health management system** combining CNN machine learning, multi-sensor data fusion, and automated irrigation. The Arduino UNO microcontroller interfaces with environmental sensors (DHT22, LDR, soil moisture) to monitor plant conditions, while a Raspberry Pi 3B+ executes Python programming for image processing AI via a TensorFlow Lite CNN model.

### Key Achievements
- ✅ **92.3% accuracy** in plant disease detection
- ✅ **35% water savings** through intelligent irrigation
- ✅ **Real-time alerts** via Telegram bot
- ✅ **Edge computing** for minimal latency
- ✅ Validated across **50+ plant specimens**

---

## 📋 Table of Contents

- [Introduction](#-introduction)
- [System Overview](#-system-overview)
- [Features](#-features)
- [Hardware Components](#️-hardware-components)
- [Software Architecture](#-software-architecture)
- [System Design](#-system-design)
- [Installation Guide](#-installation-guide)
- [Usage Instructions](#-usage-instructions)
- [Disease Detection](#-disease-detection)
- [Telegram Bot Interface](#-telegram-bot-interface)
- [Results & Performance](#-results--performance)
- [Applications](#-applications)
- [Future Enhancements](#-future-enhancements)
- [Team](#-team)
- [Acknowledgments](#-acknowledgments)
- [References](#-references)

---

## 🎯 Introduction

### Problem Statement

The agriculture sector faces critical challenges:
- 🌡️ **Unpredictable weather patterns** due to climate change
- 💧 **Water scarcity** and inefficient irrigation practices
- 🦠 **Plant diseases** causing significant crop yield losses
- 👨‍🌾 **Manual monitoring** requiring extensive labor and time
- 📉 **Delayed disease detection** leading to crop damage

### Our Solution

A smart, integrated system leveraging **IoT sensors** and **Machine Learning** to:
- Monitor environmental parameters in real-time (temperature, humidity, soil moisture, light)
- Automatically control irrigation based on soil conditions
- Detect plant diseases early using CNN image classification
- Provide remote monitoring and control via Telegram bot
- Enable data-driven agricultural decision-making

### Scope

- **Continuous monitoring** of vital plant growth parameters
- **Automated irrigation** during soil moisture deficits
- **Early disease detection** using trained ML models
- **Instant notifications** through Telegram integration
- **Reduced manual labor** and improved resource efficiency
- **Scalable design** for various crops and farm sizes

---

## 🏗️ System Overview

### Architecture Diagram
```
┌─────────────────────────────────────────────────────────────────┐
│                    SYSTEM ARCHITECTURE                          │
└─────────────────────────────────────────────────────────────────┘

    ┌─────────────────┐              ┌─────────────────┐
    │   SENSORS       │              │   ACTUATORS     │
    │                 │              │                 │
    │  • DHT22        │              │  • Water Pump   │
    │  • Soil Sensor  │◄────────────►│  • UV Light     │
    │  • LDR          │              │  • Relay Module │
    │  • Camera       │              │                 │
    └────────┬────────┘              └────────▲────────┘
             │                                 │
             │ Digital/Analog Signals          │ Relay Control
             │                                 │
             ▼                                 │
    ┌──────────────────────────────────────────┴──────────┐
    │         ARDUINO UNO (ATmega328P)                    │
    │  ┌──────────────────────────────────────────────┐  │
    │  │  • C/C++ Embedded Programming                │  │
    │  │  • Sensor Data Acquisition                   │  │
    │  │  • Real-time Actuator Control                │  │
    │  │  • Serial Communication Protocol             │  │
    │  └──────────────────────────────────────────────┘  │
    └───────────────────────┬─────────────────────────────┘
                            │
                            │ USB Serial (9600 baud)
                            │
                            ▼
    ┌───────────────────────────────────────────────────────┐
    │      RASPBERRY PI 3B+ (Raspbian OS - Debian Linux)   │
    │  ┌───────────────────────────────────────────────┐   │
    │  │  Python Application Layer                     │   │
    │  │  • Serial Data Processing (PySerial)          │   │
    │  │  • Image Capture (PiCamera2)                  │   │
    │  │  • CNN Model Inference (TensorFlow Lite)      │   │
    │  │  • Disease Classification                      │   │
    │  │  • Flask Web Server (Camera Stream)           │   │
    │  │  • Report Generation (PDF, CSV, Charts)       │   │
    │  │  • Telegram Bot Integration                   │   │
    │  └───────────────────────────────────────────────┘   │
    └───────────────────────┬───────────────────────────────┘
                            │
                            │ HTTPS Telegram Bot API
                            │
                            ▼
    ┌───────────────────────────────────────────────────────┐
    │              TELEGRAM BOT INTERFACE                   │
    │  ┌───────────────────────────────────────────────┐   │
    │  │  • Real-time Sensor Updates                   │   │
    │  │  • Disease Detection Alerts                   │   │
    │  │  • Remote Hardware Control                    │   │
    │  │  • Report Distribution (PDF/CSV)              │   │
    │  │  • Interactive Command Menu                   │   │
    │  └───────────────────────────────────────────────┘   │
    └───────────────────────┬───────────────────────────────┘
                            │
                            │ Mobile/Desktop App
                            │
                            ▼
                    ┌───────────────┐
                    │   END USER    │
                    │  👨‍🌾 Farmer    │
                    └───────────────┘
```

### Data Flow
