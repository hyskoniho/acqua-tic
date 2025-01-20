# ACQUA-TIC: Aquarium Monitoring and Remote Control

## Project Description

**ACQUA-TIC** is a project designed to monitor and control an 18-liter aquarium, providing an intelligent aquarium experience. Using an ESP32 connected to the home WiFi network, the system captures real-time data such as temperature and light levels, as well as updated images of the aquarium. Users can remotely manage the UV lamp and heater through an Android app, ensuring the aquatic environment is always in optimal conditions.

## Technologies Used

- **Hardware:**
  - ESP32: Microcontroller with WiFi connectivity
  - 5V Relay Module: To control the UV lamp and heater
  - OV7670 Camera: Captures images of the aquarium
  - DS18B20 Temperature Sensor: Monitors water temperature
  - BH1750 Light Sensor: Measures ambient light

- **Software:**
  - **AWS:** Using EC2 to host the server that processes requests.
  - **Flask:** Web framework to create the RESTful API that interacts with the ESP32 and the database.
  - **MongoDB Atlas:** NoSQL database to store collected data and aquarium images.
  - **Kivy:** Python framework for developing the mobile app for Android.

## Project Structure

The project structure is organized into the following folders:

- `database/`: Scripts for database configuration.
- `esp32/`: Code for the ESP32 microcontroller.
- `mobile_app/`: Code for the Android app, including icons and interfaces.
- `server/`: Code for the Flask application that manages the API endpoints.

## Features

1. **Data Capture:**
   - Real-time water temperature measurement.
   - Reading light levels using the BH1750.
   - Capturing images with the camera at regular intervals.

2. **Remote Control:**
   - Enabling/disabling the UV lamp.
   - Controlling the heater to maintain the ideal aquarium temperature.

3. **Data Visualization:**
   - Interface for viewing collected data and images in the Android app.

## Usage Instructions

1. **ESP32 Configuration:**
   - Upload the code provided in the `esp32/` folder to the ESP32 using the Arduino IDE.
   - Ensure the microcontroller is connected to the same WiFi network as the AWS server.

2. **Server Configuration:**
   - Deploy the Flask application on AWS EC2.
   - Configure MongoDB Atlas and connect the application to the database.

3. **Android App:**
   - Install the app developed with Kivy on an Android device.
   - Connect to the Flask application to view data and remotely control the aquarium.
