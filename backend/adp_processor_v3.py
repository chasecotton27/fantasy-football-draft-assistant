import ssl
import urllib3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Disable SSL verification
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context

# Set up Chrome options
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": "../tests",  # Change to your preferred directory
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    # Navigate to the webpage
    driver.get("https://www.fantasypros.com/nfl/adp/overall.php")

    # Wait for the page to load
    time.sleep(5)  # Adjust the wait time as needed

    # Find and click the download button
    download_button = driver.find_element(By.CSS_SELECTOR, ".export")
    download_button.click()

    # Wait for the download to complete
    time.sleep(10)  # Adjust the wait time as needed

finally:
    # Close the WebDriver
    driver.quit()

# Re-enable SSL verification
ssl._create_default_https_context = ssl.create_default_context
