# ============ PERFORMANCE SETTINGS ============
CONFIG = {
    # Retry and Timeout
    "MAX_RETRIES": 3,              # Number of retries per number (default: 3)
    "TIMEOUT_SECONDS": 10,         # Timeout limit for each request (default: 10)
    
    # Threading/Concurrency
    "THREAD_POOL_SIZE": 2,         # Number of concurrent threads (default: 2, max: 4)
    
    # Input Limits
    "MAX_NUMBERS": 30,             # Maximum numbers allowed to check (default: 30)
    
    # Rate Limiting
    "DELAY_BETWEEN_REQUESTS": 0.5, # Delay between requests in seconds (default: 0.5)
    
    # Browser
    "USER_AGENT": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
}

# ============ PRESETS ============

# For slow internet connections
SLOW_CONNECTION = {
    "MAX_RETRIES": 4,
    "TIMEOUT_SECONDS": 20,
    "THREAD_POOL_SIZE": 1,
    "DELAY_BETWEEN_REQUESTS": 1.5,
}

# For fast internet connections
FAST_CONNECTION = {
    "MAX_RETRIES": 2,
    "TIMEOUT_SECONDS": 5,
    "THREAD_POOL_SIZE": 4,
    "DELAY_BETWEEN_REQUESTS": 0.2,
}

# Balanced settings for general use
BALANCED = {
    "MAX_RETRIES": 3,
    "TIMEOUT_SECONDS": 10,
    "THREAD_POOL_SIZE": 2,
    "DELAY_BETWEEN_REQUESTS": 0.5,
}

# Safe mode (Less aggressive)
SAFE_MODE = {
    "MAX_RETRIES": 5,
    "TIMEOUT_SECONDS": 15,
    "THREAD_POOL_SIZE": 1,
    "DELAY_BETWEEN_REQUESTS": 2,
}

# ============ HOW TO USE ============
"""
1. Exported by default with CONFIG = ... above

2. Or select from presets below:
   CONFIG = SLOW_CONNECTION    # For slow connection
   CONFIG = FAST_CONNECTION    # For fast connection
   CONFIG = BALANCED           # For regular use
   CONFIG = SAFE_MODE          # For lower aggressive rate on Facebook

3. Import in facebook_checker_v2.py:
   from config import CONFIG
"""

# ============ RECOMMENDATIONS ============
"""
🔧 Choose according to your network connection:

📊 Slow Connection (< 5 Mbps):
   - CONFIG = SLOW_CONNECTION
   - TIMEOUT_SECONDS = 20
   - THREAD_POOL_SIZE = 1

⚡ Fast Connection (> 20 Mbps):
   - CONFIG = FAST_CONNECTION
   - TIMEOUT_SECONDS = 5
   - THREAD_POOL_SIZE = 3-4

⚖️ Medium Connection (5-20 Mbps):
   - CONFIG = BALANCED (default)

🛡️ To reduce block risks:
   - CONFIG = SAFE_MODE
   - Or increase CONFIG["DELAY_BETWEEN_REQUESTS"] (2-3 seconds)

⚠️ Remember:
- More threads = Higher CPU and memory usage
- Lower delay = May flag requests as spam on Facebook
- Find a good balance!
"""

# ============ DEBUG MODE ============
DEBUG = False  # Set to True to enable detailed debug logs

if DEBUG:
    import logging
    logging.basicConfig(level=logging.DEBUG)
