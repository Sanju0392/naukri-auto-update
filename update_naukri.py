from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

USERNAME = os.getenv("NAUKRI_USERNAME")
PASSWORD = os.getenv("NAUKRI_PASSWORD")
RESUME_PATH = os.getenv("RESUME_PATH", "resume.pdf")

def upload_resume():
    options = Options()
    options.add_argument("--headless=new")  # ✅ new headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")  # 👈 important for rendering


    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    try:
        driver.get("https://www.naukri.com/nlogin/login")

        # Wait for and enter username
        wait.until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Enter your active Email ID / Username"]'))).send_keys(USERNAME)

        # Enter password
        driver.find_element(By.XPATH, '//input[@placeholder="Enter your password"]').send_keys(PASSWORD)

        # Click login
        driver.find_element(By.XPATH, '//button[text()="Login"]').click()

        # Wait for profile page redirect (or do it manually)
        time.sleep(5)
        driver.get("https://www.naukri.com/mnjuser/profile")

        # Wait for resume upload field
        upload_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="file"]')))
        upload_input.send_keys(os.path.abspath(RESUME_PATH))

        time.sleep(5)  # Wait for upload to complete
        print("✅ Resume uploaded successfully!")

    except Exception as e:
        print("❌ Error:", e)

    finally:
        driver.quit()

if __name__ == "__main__":
    upload_resume()
