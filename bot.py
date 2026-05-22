import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

def check_facebook_number(driver, number):
    try:
        driver.get("https://limited.facebook.com/login/identify/")
        time.sleep(0.1)

        try:
            input_box = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='email'], input[type='text']"))
            )
        except:
            return f"{number} - 🖕"
        
        input_box.click()
        input_box.clear()
        input_box.send_keys(number)
        input_box.send_keys("\n")
        
        try:
            submit_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'], button")
            submit_button.click()
        except:
            pass

        time.sleep(0.8)

        page_content = driver.page_source.lower()
        current_url = driver.current_url
        
        is_account_present = (
            "choose a way" in page_content or 
            "try entering your password" in page_content or 
            "try another way" in page_content or 
            "password" in page_content or
            "identify" not in current_url
        )

        if is_account_present:
            return f"{number} - ✅"
        else:
            return f"{number} - 🖕"

    except Exception as e:
        return f"{number} - 🖕"

print("--- Facebook Number Checker ---\n")

numbers_to_check = []

while True:
    try:
        user_input = input().strip()
        
        if user_input.lower() == 'exit':
            if numbers_to_check:
                break
            else:
                print("No numbers entered. Exiting...")
                sys.exit()
        
        if user_input:
            numbers_to_check.append(user_input)
        else:
            if numbers_to_check:
                break
        
    except KeyboardInterrupt:
        print("\nProgram stopped by user.")
        sys.exit()

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--single-process")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-sync")
chrome_options.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1")
chrome_options.add_argument("--window-size=375,667")

prefs = {
    "profile.managed_default_content_settings.images": 2,
    "profile.managed_default_content_settings.stylesheets": 2,
    "profile.managed_default_content_settings.fonts": 2,
    "profile.managed_default_content_settings.media": 2
}
chrome_options.add_experimental_option("prefs", prefs)

print("Checking Started\n")

results = []

try:
    service = Service("/data/data/com.termux/files/usr/bin/chromedriver")
    driver1 = webdriver.Chrome(service=service, options=chrome_options)
    driver2 = webdriver.Chrome(service=service, options=chrome_options)
    
    for i, number in enumerate(numbers_to_check):
        current_driver = driver1 if i % 2 == 0 else driver2
        result = check_facebook_number(current_driver, number)
        results.append(result)
        print(result)
    
    print("\n" + "="*40)
    print("FINAL RESULTS")
    print("="*40 + "\n")
    for result in results:
        print(result)
    
    driver1.quit()
    driver2.quit()

except Exception as e:
    print(f"Error: {e}")
    try:
        driver1.quit()
    except:
        pass
    try:
        driver2.quit()
    except:
        pass
