from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# Retrieve credentials
email = os.environ.get("NAUKRI_EMAIL")
password = os.environ.get("NAUKRI_PASSWORD")
if not email or not password:
    raise ValueError("NAUKRI_EMAIL or NAUKRI_PASSWORD not set in environment variables")

# Configure Chrome options
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")  # Set a standard window size

# Initialize WebDriver
driver = webdriver.Chrome(options=options)

try:
    print("🔐 Opening Naukri login page...")
    driver.get("https://www.naukri.com/mnjuser/profile/login")

    print(f"🌐 Current URL: {driver.current_url}")
    print(f"📄 Page title: {driver.title}")

    # Save initial page for debugging
    with open("page_dump.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    driver.save_screenshot("naukri_login_page.png")

    # Wait for page to load
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    # Check for iframes
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    if iframes:
        print(f"Found {len(iframes)} iframe(s). Switching to first iframe.")
        driver.switch_to.frame(iframes[0])
    else:
        print("No iframes detected.")

    # Locate and fill username field
    try:
        username_field = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "usernameField"))
        )
    except:
        print("ID 'usernameField' not found. Trying alternative locator.")
        username_field = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.NAME, "username"))  # Fallback
        )
    print("✅ Username field found.")
    username_field.send_keys(email)

    # Locate and fill password field
    try:
        password_field = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "passwordField"))
        )
    except:
        print("ID 'passwordField' not found. Trying alternative locator.")
        password_field = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.NAME, "password"))  # Fallback
        )
    print("✅ Password field found.")
    password_field.send_keys(password)

    # Locate and click login button
    try:
        login_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "waves-effect"))
        )
    except:
        print("Class 'waves-effect' not found. Trying alternative locator.")
        login_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))  # Fallback
        )
    print("✅ Login button found.")
    login_button.click()

    # Wait for successful login
    WebDriverWait(driver, 30).until(
        EC.url_contains("naukri.com/mnjuser")
    )
    print("✅ Logged in successfully.")

except Exception as e:
    print("❌ An error occurred:")
    print(e)
    driver.save_screenshot("error_page.png")
    with open("error_dump.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    raise

finally:
    driver.quit()
    print("🧹 Browser closed.")
