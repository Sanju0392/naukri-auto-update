# update_naukri.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

email = "your_email_here"
password = "your_password_here"

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)

driver.get("https://www.naukri.com/mnjuser/profile/login")
time.sleep(2)

# Log in
driver.find_element(By.ID, "usernameField").send_keys(email)
driver.find_element(By.ID, "passwordField").send_keys(password)
driver.find_element(By.CLASS_NAME, "waves-effect").click()
time.sleep(5)

# Do a dummy update (open profile edit and save)
driver.get("https://www.naukri.com/mnjuser/profile")
time.sleep(5)

print("Profile update simulated.")
driver.quit()
