from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import os

# Load credentials from environment variables
USERNAME = os.getenv("NAUKRI_USERNAME")
PASSWORD = os.getenv("NAUKRI_PASSWORD")
RESUME_PATH = os.getenv("RESUME_PATH", "resume.pdf")

def upload_resume():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    try:
        # Open Naukri login page
        driver.get("https://www.naukri.com/nlogin/login")

        # Login
        driver.find_element(By.ID, "usernameField").send_keys(USERNAME)
        driver.find_element(By.ID, "passwordField").send_keys(PASSWORD)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        sleep(5)

        # Go to Profile Page
        driver.get("https://www.naukri.com/mnjuser/profile")

        sleep(5)

        # Upload Resume
        upload_button = driver.find_element(By.XPATH, "//input[@type='file']")
        upload_button.send_keys(os.path.abspath(RESUME_PATH))

        sleep(5)  # Wait for upload to complete

        print("✅ Resume uploaded successfully!")

    except Exception as e:
        print("❌ Error:", e)

    finally:
        driver.quit()

if __name__ == "__main__":
    upload_resume()
