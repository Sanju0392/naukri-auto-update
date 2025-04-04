from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

# Load credentials from environment
email = os.environ["NAUKRI_EMAIL"]
password = os.environ["NAUKRI_PASSWORD"]

# Set up headless Chrome options for GitHub Actions
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Initialize WebDriver
driver = webdriver.Chrome(options=options)

try:
    print("🔐 Opening Naukri login page...")
    driver.get("https://www.naukri.com/mnjuser/profile/login")

    # Wait for the login form to appear
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "usernameField"))
    )

    print("✅ Login form loaded. Logging in...")
    driver.find_element(By.ID, "usernameField").send_keys(email)
    driver.find_element(By.ID, "passwordField").send_keys(password)
    driver.find_element(By.CLASS_NAME, "waves-effect").click()

    # Wait until login is complete and redirected to profile page
    WebDriverWait(driver, 20).until(
        EC.url_contains("naukri.com/mnjuser")
    )

    print("🚀 Logged in successfully.")

    # Go to profile page (again just to be safe)
    driver.get("https://www.naukri.com/mnjuser/profile")

    # Wait for profile page to load
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "profile-container"))
    )

    # Optional: You can click "Edit" and save to trigger an update
    print("📝 Simulating profile update...")
    time.sleep(2)  # Simulate some edit/save here if needed

    print("✅ Profile update simulated successfully.")

except Exception as e:
    print(f"❌ Error occurred: {e}")
    driver.save_screenshot("error_page.png")
    raise

finally:
    driver.quit()
    print("🧹 Browser closed.")

