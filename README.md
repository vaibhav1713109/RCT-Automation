# RCT Automation
Developed automation suite to perform basic test cases of RF testing. The purpose of this suite is to configure the radio unit(RU) for transmitting RF power and configure the Vector Analyzer for capturing the transmitting power, ACLR and Constellation of RU. Developed desktop application frontend with PyQt5,QtDesigner and backend with python.


![RCT_setup_dia drawio](https://user-images.githubusercontent.com/96615773/209643547-3c78ccb1-2b50-4301-8be7-5b8779b458a8.png)

## Requirements:
- Python >=3.7
- fpdf2>=2.5.5
- PyVISA>=1.12.0
- PyVISA-py>=0.5.3
- ifcfg>=0.22
- pytest>=7.0.1
- requests>=2.27.1
- tabulate>=0.8.10
- xmltodict>=0.13.0
- pyqt5>=5.15.6
- paramiko>=2.11.0

## Installation
- python -m pip install --upgrade pip
- pip install -r requirements.txt

# Usage:
- Window
  - Run RF_GUI.exe
- Linux
  - Go To Mavu_ru Directory
  - sudo python login_page.py
