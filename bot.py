import sys
import time
import json
import logging
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from collections import defaultdict

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    WebDriverException,
    ConnectionError as SeleniumConnectionError
)

# ============ CONFIGURATION ============
CHROMEDRIVER_PATHS = [
    "/data/data/com.termux/files/usr/bin/chromedriver",  # Termux default
    "/usr/bin/chromedriver",                              # Linux default
    "/usr/local/bin/chromedriver",                        # macOS
    "./chromedriver"                                      # Current directory
]

CONFIG = {
    "MAX_RETRIES": 3,
    "TIMEOUT_SECONDS": 10,
    "THREAD_POOL_SIZE": 2,
    "MAX_NUMBERS": 30,
    "DELAY_BETWEEN_REQUESTS": 0.5,  # seconds
    "USER_AGENT": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
}

# ============ LOGGING SETUP ============
def setup_logging():
    """Setup logging configuration"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / f"fb_checker_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)

logger = setup_logging()

# ============ RESULT TRACKER ============
class ResultTracker:
    """Track and manage results"""
    
    def __init__(self):
        self.results = []
        self.stats = defaultdict(int)
        self.lock = Lock()
    
    def add_result(self, number, status, message=""):
        """Add result to tracker"""
        with self.lock:
            result = {
                "number": number,
                "status": status,
                "message": message,
                "timestamp": datetime.now().isoformat()
            }
            self.results.append(result)
            self.stats[status] += 1
            logger.info(f"{number} - {status} ({message})")
    
    def save_to_file(self):
        """Save results to files"""
        output_dir = Path("outputs")
        output_dir.mkdir(exist_ok=True)
        
        # JSON format
        json_file = output_dir / f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                "summary": dict(self.stats),
                "results": self.results,
                "total": len(self.results),
                "generated_at": datetime.now().isoformat()
            }, f, indent=2, ensure_ascii=False)
        
        # CSV format
        csv_file = output_dir / f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(csv_file, 'w', encoding='utf-8') as f:
            f.write("Number,Status,Message,Timestamp\n")
            for result in self.results:
                f.write(f"{result['number']},{result['status']},\"{result['message']}\",{result['timestamp']}\n")
        
        logger.info(f"📁 Results saved: {json_file} and {csv_file}")
        return json_file, csv_file
    
    def print_summary(self):
        """Print summary statistics"""
        print("\n" + "="*50)
        print("📊 SUMMARY")
        print("="*50)
        print(f"Total Numbers Checked: {len(self.results)}")
        for status, count in self.stats.items():
            print(f"  {status}: {count}")
        print("="*50 + "\n")

# ============ CHROMEDRIVER FINDER ============
def find_chromedriver():
    """Find available ChromeDriver path"""
    for path in CHROMEDRIVER_PATHS:
        try:
            if Path(path).exists():
                logger.info(f"✅ ChromeDriver found: {path}")
                return path
        except:
            pass
    
    logger.error("❌ ChromeDriver not found!")
    return None

# ============ CHROME OPTIONS ============
def get_chrome_options():
    """Setup Chrome options"""
    options = Options()
    
    # Performance options
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--single-process")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-sync")
    
    # User agent
    options.add_argument(f"user-agent={CONFIG['USER_AGENT']}")
    
    # Window size
    options.add_argument("--window-size=375,667")
    
    # Disable images/css/fonts to improve speed
    prefs = {
        "profile.managed_default_content_settings.images": 2,
        "profile.managed_default_content_settings.stylesheets": 2,
        "profile.managed_default_content_settings.fonts": 2,
        "profile.managed_default_content_settings.media": 2
    }
    options.add_experimental_option("prefs", prefs)
    
    return options

# ============ FACEBOOK CHECKER ============
def check_facebook_number(driver, number, tracker):
    """Check number on Facebook with retry logic"""
    
    for attempt in range(1, CONFIG["MAX_RETRIES"] + 1):
        try:
            logger.debug(f"Checking {number} (Attempt {attempt}/{CONFIG['MAX_RETRIES']})")
            
            # Navigate to Facebook identify page
            driver.get("https://limited.facebook.com/login/identify/")
            time.sleep(0.5)
            
            # Find input box with extended wait
            try:
                input_box = WebDriverWait(driver, CONFIG["TIMEOUT_SECONDS"]).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='email'], input[type='text']"))
                )
            except TimeoutException:
                tracker.add_result(number, "❌ NOT FOUND", "Input box timeout")
                return
            
            # Clear and enter number
            input_box.click()
            time.sleep(0.2)
            input_box.clear()
            time.sleep(0.1)
            input_box.send_keys(number)
            time.sleep(0.3)
            
            # Submit form
            try:
                submit_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'], button")
                submit_button.click()
            except NoSuchElementException:
                # Try sending Enter key if button not found
                input_box.send_keys("\n")
            
            # Wait for response
            time.sleep(CONFIG["DELAY_BETWEEN_REQUESTS"])
            
            # Check page content
            page_content = driver.page_source.lower()
            current_url = driver.current_url
            
            # Detection logic
            account_found_keywords = [
                "choose a way",
                "try entering your password",
                "try another way",
                "password",
                "reset"
            ]
            
            is_account_present = any(keyword in page_content for keyword in account_found_keywords) or "identify" not in current_url
            
            if is_account_present:
                tracker.add_result(number, "✅ FOUND", "Account detected")
            else:
                tracker.add_result(number, "❌ NOT FOUND", "No account")
            
            return
        
        except WebDriverException as e:
            error_msg = str(e)
            if attempt < CONFIG["MAX_RETRIES"]:
                logger.warning(f"{number} - WebDriver error (Attempt {attempt}): {error_msg}. Retrying...")
                time.sleep(2)  # Wait before retry
            else:
                tracker.add_result(number, "⚠️ ERROR", f"WebDriver: {error_msg[:50]}")
        
        except SeleniumConnectionError as e:
            if attempt < CONFIG["MAX_RETRIES"]:
                logger.warning(f"{number} - Connection error (Attempt {attempt}). Retrying...")
                time.sleep(2)
            else:
                tracker.add_result(number, "⚠️ ERROR", "Connection timeout")
        
        except Exception as e:
            error_type = type(e).__name__
            if attempt < CONFIG["MAX_RETRIES"]:
                logger.warning(f"{number} - {error_type} (Attempt {attempt}): {str(e)[:50]}. Retrying...")
                time.sleep(1)
            else:
                tracker.add_result(number, "⚠️ ERROR", f"{error_type}")
    
    logger.error(f"❌ {number} - Failed after {CONFIG['MAX_RETRIES']} attempts")

# ============ WORKER THREAD ============
def worker_thread(numbers_chunk, chromedriver_path, tracker):
    """Worker function for each thread"""
    
    try:
        # Create Chrome session per thread
        options = get_chrome_options()
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=options)
        
        # Check each number
        for number in numbers_chunk:
            check_facebook_number(driver, number, tracker)
            time.sleep(0.5)  # Rate limiting
        
        driver.quit()
        
    except Exception as e:
        logger.error(f"Worker thread error: {e}")

# ============ MAIN PROGRAM ============
def main():
    """Main program execution"""
    
    print("\n" + "="*60)
    print("🔍 FACEBOOK NUMBER CHECKER - PRODUCTION VERSION")
    print("="*60 + "\n")
    
    # Find ChromeDriver
    chromedriver_path = find_chromedriver()
    if not chromedriver_path:
        print("❌ ChromeDriver not found!")
        print("Run: pkg install -y chromium (in Termux)")
        sys.exit(1)
    
    # Input numbers
    print(f"📱 Enter numbers (Max {CONFIG['MAX_NUMBERS']}, blank line to finish):")
    print("Type 'exit' to cancel\n")
    
    numbers_to_check = []
    while True:
        try:
            user_input = input(f"[{len(numbers_to_check)}/{CONFIG['MAX_NUMBERS']}] > ").strip()
            
            if user_input.lower() == 'exit':
                if numbers_to_check:
                    print("\nCancelling...")
                    sys.exit(0)
                else:
                    print("No numbers entered. Exiting...")
                    sys.exit(0)
            
            if len(numbers_to_check) >= CONFIG['MAX_NUMBERS']:
                print(f"⚠️ Maximum {CONFIG['MAX_NUMBERS']} numbers reached!")
                break
            
            if user_input:
                # Validate number format (basic)
                if len(user_input) >= 5:  # Minimum 5 characters
                    numbers_to_check.append(user_input)
                    print(f"✅ Added: {user_input}")
                else:
                    print("❌ Number too short (min 5 characters)")
            else:
                if numbers_to_check:
                    break
        
        except KeyboardInterrupt:
            print("\n\n⚠️ Interrupted by user")
            sys.exit(0)
    
    if not numbers_to_check:
        print("❌ No numbers to check!")
        sys.exit(1)
    
    # Initialize tracker
    tracker = ResultTracker()
    
    # Start checking
    print(f"\n⏳ Starting to check {len(numbers_to_check)} numbers with {CONFIG['THREAD_POOL_SIZE']} threads...\n")
    print("="*60 + "\n")
    
    start_time = time.time()
    
    try:
        # Divide numbers into chunks for threads
        chunk_size = max(1, len(numbers_to_check) // CONFIG['THREAD_POOL_SIZE'])
        chunks = [numbers_to_check[i:i + chunk_size] for i in range(0, len(numbers_to_check), chunk_size)]
        
        # Use ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=CONFIG['THREAD_POOL_SIZE']) as executor:
            futures = [
                executor.submit(worker_thread, chunk, chromedriver_path, tracker)
                for chunk in chunks
            ]
            
            # Wait for all tasks
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logger.error(f"Thread error: {e}")
    
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    
    # Calculate time
    elapsed_time = time.time() - start_time
    
    # Print results
    print("\n" + "="*60)
    print("📋 FINAL RESULTS")
    print("="*60 + "\n")
    
    for result in tracker.results:
        emoji = result['status'].split()[0]
        print(f"{emoji} {result['number']:<20} {result['status']:<15} {result['message']}")
    
    # Print summary
    tracker.print_summary()
    
    print(f"⏱️  Time taken: {elapsed_time:.2f} seconds")
    print(f"⚡ Speed: {len(tracker.results) / elapsed_time:.2f} numbers/second\n")
    
    # Save results
    json_file, csv_file = tracker.save_to_file()
    print(f"\n✅ Results saved successfully!")
    print(f"   JSON: {json_file}")
    print(f"   CSV:  {csv_file}\n")

if __name__ == "__main__":
    main()
