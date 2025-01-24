# MangaDex Downloader

A Python script for downloading manga chapters from MangaDex. This script uses Selenium to capture network requests and download manga images directly to your local machine in an organized structure.

---

## Features
- Extracts manga chapter details (volume, chapter, title, language, and pages).
- Captures and processes network logs for downloading image URLs.
- Organizes manga chapters into structured directories.
- Uses Selenium for browser automation and WebDriver Manager for setup.

---

## Requirements
- Python 3.12 or higher
- Google Chrome browser

### Libraries
- `selenium==4.27.1`
- `requests==2.32.2`
- `webdriver-manager==4.0.2`

---

## Installation
### 1. Clone the Repository
```bash
git clone https://github.com/Typh00ns/mangadex_downloader.git
cd mangadex_downloader
```


### 2. Create and Activate a Virtual Environment
Anaconda:
```bash
conda create --name mangadex_downloader_env python=3.12
conda activate mangadex_downloader_env
```
For none conda users:
```bash
python -m venv mangadex_downloader_env
source mangadex_downloader_env/bin/activate  # On Linux/Mac
mangadex_downloader_env\Scripts\activate     # On Windows
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
## Usage
### 1. Run the Script
```bash
python mangadex_downloader.py
```
### 2. Input Information
Enter the chapter URL of the manga you wish to download(after you click on read).
Enter the name of the manga to save it with an organized directory structure.

### 3. Directory Structure

The downloaded files are saved in:

C:\{manga_name}\Volume {volume}\Chapter {chapter}\{title}

## Acknowledgments

MangaDex for providing amazing manga content.
Selenium for browser automation.
WebDriver Manager for simplifying WebDriver setup.
