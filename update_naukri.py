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
    options.add_argument("--headless=new")  # New headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    try:
        print("🔁 Opening Naukri login page...")
        driver.get("https://www.naukri.com/nlogin/login")

        # Wait and enter username
        email_input = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//input[@placeholder="Enter your active Email ID / Username"]')
        ))
        email_input.send_keys(USERNAME)

        # Enter password
        password_input = driver.find_element(By.XPATH, '//input[@placeholder="Enter your password"]')
        password_input.send_keys(PASSWORD)

        # Click login
        login_button = driver.find_element(By.XPATH, '//button[.="Login"]')
        login_button.click()

        print("✅ Logged in. Navigating to profile...")

        # Wait for redirection or go directly
        time.sleep(5)
        driver.get("https://www.naukri.com/mnjuser/profile")

        # Wait for upload input
        upload_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="file"]')))
        upload_input.send_keys(os.path.abspath(RESUME_PATH))

        time.sleep(5)  # Let upload complete
        print("✅ Resume uploaded successfully!")

    except Exception as e:
        print("❌ Error occurred:", e)
        driver.save_screenshot("error_screenshot.png")  # 🔍 screenshot for debugging
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

    finally:
        driver.quit()

if __name__ == "__main__":
    upload_resume()
