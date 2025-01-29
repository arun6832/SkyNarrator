# Weather Advisory for Farmers

This project generates a weather advisory report for farmers based on weather data. It provides a summary in English, with a translation into Malayalam, and generates a PDF report containing weather data and advisory details.

## Features

- Weather data table for the next five days, including:
  - Rainfall
  - Wind Speed
  - Temperature
  - Humidity
  - Relative Humidity (Max and Min)

- Advisory summary in **English** and **Malayalam** for farmers, including:
  - Irrigation recommendations
  - Crop management tips
  - Weather preparedness advice

- PDF generation with:
  - Weather data in a tabular format
  - Advisory content in English and Malayalam

## Prerequisites

Before running this project, ensure you have the following dependencies installed:

- Python 3.6 or higher
- `reportlab` for PDF generation
- `googletrans` for language translation
- A font supporting Malayalam (e.g., `NotoSansMalayalam`)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/weather-advisory-for-farmers.git
   cd weather-advisory-for-farmers
