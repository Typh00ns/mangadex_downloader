import os
import requests
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def set_up_chrome():
    """Set up Chrome options and return a webdriver instance."""
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--enable-logging")
    options.add_argument("--v=1")
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")  # comment if you want headless mode

    # Enable network logging
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL', 'browser': 'ALL'})

    # Set up ChromeDriver path
    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=options)
    return driver

def capture_network_logs(driver):
    """Capture network logs and return matching URLs."""
    try:
        performance_logs = driver.get_log("performance")
        browser_logs = driver.get_log("browser")
        
        matching_urls = []
        
        for entry in performance_logs:
            if 'message' in entry:
                try:
                    message_data = json.loads(entry['message'])
                    if 'url' in message_data['message']['params']['response']:
                        url = message_data['message']['params']['response']['url']
                        if url.startswith("https://cmdxd"):
                            matching_urls.append(url)
                            print(f"Matching URL: {url}")
                
                except (json.JSONDecodeError, KeyError) as e:
                    print(f"Error parsing entry: {e}")
    except Exception as e:
        print(f"Error capturing logs: {e}")
    
    return matching_urls

def extract_manga_info(chapter_url):
    """Extract manga info from the API."""
    if "://mangadex.org" in chapter_url:
        url = chapter_url.replace("://mangadex.org", "://api.mangadex.org")
        print(url)
    else:
        raise ValueError("The URL does not match the expected format.")

    response = requests.get(url)
    data = response.json()
    
    attributes = data['data']['attributes']
    volume = attributes['volume']
    chapter = attributes['chapter']
    title = attributes['title']
    language = attributes['translatedLanguage']
    pages = attributes['pages']
    
    return volume, chapter, title, language, pages

def download_images(matching_urls, save_directory):
    """Download images from the provided URLs."""
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    for index, url in enumerate(matching_urls, start=1):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            file_name = f"page_{index}.jpg"
            file_path = os.path.join(save_directory, file_name)

            with open(file_path, "wb") as file:
                for chunk in response.iter_content(8192):
                    file.write(chunk)

            print(f"Downloaded {file_name} from {url}")
        except Exception as e:
            print(f"Failed to download {url}: {e}")

    print(f"All images saved in {os.path.abspath(save_directory)}")

def main(chapter_url, manga_name):
    """Main function to handle the complete process."""
    print(f"Starting process for manga: {manga_name}, Chapter URL: {chapter_url}")

    # Set up the browser and capture network logs
    print("Setting up the browser...")
    driver = set_up_chrome()
    print("Browser setup complete.")
    
    print(f"Navigating to chapter URL: {chapter_url}")
    driver.get(chapter_url)
    
    print("Waiting for the page to load...")
    time.sleep(20)  # Allow time for page to load
    
    print("Capturing network logs...")
    matching_urls = capture_network_logs(driver)
    print(f"Captured {len(matching_urls)} matching URLs.")
    
    driver.quit()
    print("Browser closed.")

    # Extract manga information
    print(f"Extracting manga information from chapter URL: {chapter_url}")
    volume, chapter, title, language, pages = extract_manga_info(chapter_url)
    print(f"Extracted info - Volume: {volume}, Chapter: {chapter}, Title: {title}, Language: {language}, Pages: {pages}")

    # Create save directory
    save_directory = f"C:\\{manga_name}\\Volume {volume}\\Chapter {chapter}\\{title}"
    print(f"Save directory will be: {save_directory}")
    
    # Download images
    print(f"Starting image download for chapter {chapter}...")
    download_images(matching_urls, save_directory)
    print(f"Image download for chapter {chapter} complete.")


if __name__ == "__main__":
    # Provide your target URL and manga name here
    chapter_url = input("your_target_url: ")
    manga_name = input("your_manga_name: ")
    main(chapter_url, manga_name)
