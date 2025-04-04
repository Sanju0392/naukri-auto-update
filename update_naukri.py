from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

email = os.environ["NAUKRI_EMAIL"]
password = os.environ["NAUKRI_PASSWORD"]

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

try:
    print("🔐 Opening Naukri login page...")
    driver.get("https://www.naukri.com/mnjuser/profile/login")

    print(f"🌐 Current URL: {driver.current_url}")
    print(f"📄 Page title: {driver.title}")

    # Dump HTML for debugging
    with open("page_dump.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    # Take screenshot
    driver.save_screenshot("naukri_login_page.png")

    # Wait until the field is present (max 20s)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "usernameField"))
    )

    print("✅ Login form found, logging in...")
    driver.find_element(By.ID, "usernameField").send_keys(email)
    driver.find_element(By.ID, "passwordField").send_keys(password)
    driver.find_element(By.CLASS_NAME, "waves-effect").click()

    WebDriverWait(driver, 20).until(
        EC.url_contains("naukri.com/mnjuser")
    )

    print("✅ Logged in successfully.")

except Exception as e:
    print("❌ An error occurred.")
    print(e)
    driver.save_screenshot("error_page.png")
    with open("error_dump.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    raise

finally:
    driver.quit()
    print("🧹 Browser closed.")


