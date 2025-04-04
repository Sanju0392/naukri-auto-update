from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# Load credentials from environment variables
email = os.environ["NAUKRI_EMAIL"]
password = os.environ["NAUKRI_PASSWORD"]

# Set up Chrome options
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-gpu")

# Initialize the driver
driver = webdriver.Chrome(options=options)

try:
    print("🔐 Opening Naukri login page...")
    driver.get("https://www.naukri.com/mnjuser/profile/login")

    # Wait for the page to load
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Check for iframes and switch if necessary
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    if iframes:
        print(f"Found {len(iframes)} iframe(s). Switching to first iframe.")
        driver.switch_to.frame(iframes[0])

    # Locate and fill username field
    username_field = wait.until(EC.presence_of_element_located((By.ID, "usernameField")))
    username_field.send_keys(email)

    # Locate and fill password field
    password_field = wait.until(EC.presence_of_element_located((By.ID, "passwordField")))
    password_field.send_keys(password)

    # Click login button (adjust locator as needed)
    login_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "waves-effect")))
    login_button.click()

    # Verify login success
    wait.until(EC.url_contains("naukri.com/mnjuser"))
    print("✅ Logged in successfully.")

except Exception as e:
    print("❌ An error occurred:", e)
    # Save debug info
    driver.save_screenshot("error_page.png")
    with open("error_dump.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    raise

finally:
    driver.quit()
    print("🧹 Browser closed.")
