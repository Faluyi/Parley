#!/bin/bash

echo "Installing the required components..."

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python is not installed. Please install Python and add it to the PATH."
    exit
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null
then
    echo "Pip is not installed. Please install pip."
    exit
fi

# Install required Python packages
echo "Installing required Python packages..."
pip3 install selenium

# Download ChromeDriver
echo "Downloading ChromeDriver..."
chromedriver_version=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)
curl -O https://chromedriver.storage.googleapis.com/${chromedriver_version}/chromedriver_mac64.zip

# Unzip ChromeDriver
echo "Unzipping ChromeDriver..."
unzip chromedriver_mac64.zip -d .
rm chromedriver_mac64.zip

# Add ChromeDriver to PATH
echo "Adding ChromeDriver to PATH..."
chmod +x chromedriver
mv chromedriver /usr/local/bin/

echo "Setup is complete."
