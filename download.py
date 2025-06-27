"""Automate Zaim login and data download process using Selenium.

Required Environment variables:
- ZAIM_ID: Your Zaim account ID
- ZAIM_PASSWORD: Your Zaim account password
"""

import argparse
import datetime
import logging
import os
import shutil
import tempfile
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Check for environment variables for Zaim credentials
ZAIM_ID = os.getenv("ZAIM_ID")
ZAIM_PASSWORD = os.getenv("ZAIM_PASSWORD")
if not ZAIM_ID or not ZAIM_PASSWORD:
    logger.error("Environment variables ZAIM_ID and ZAIM_PASSWORD must be set.")
    raise ValueError("Environment variables ZAIM_ID and ZAIM_PASSWORD must be set.")

# Process command-line arguments
parser = argparse.ArgumentParser(
    description="Automate Zaim login and data download process using Selenium. Required environment variables: ZAIM_ID, ZAIM_PASSWORD"
)
parser.add_argument("start_year", help="Start year. Example: 2020")
parser.add_argument("start_month", help="Start month. Example: 01")
parser.add_argument("start_day", help="Start day. Example: 01")
parser.add_argument("end_year", help="End year. Example: 2021")
parser.add_argument("end_month", help="End month. Example: 12")
parser.add_argument("end_day", help="End day. Example: 31")
parser.add_argument("-t", "--totp", help="Two-Factor Authentication code. Required if TOTP is enabled")
parser.add_argument(
    "-c",
    "--charset",
    help="Character set for the output file. Available charsets: utf8, sjis. Default: utf8.",
    default="utf8",
)
parser.add_argument(
    "-o",
    "--outputdir",
    help="Output directory under ~/Downloads. Default: 'selenium_downloads'",
    default="selenium_downloads",
)
parser.add_argument("--prompt_for_download", help="Enable prompt for download confirmation", action="store_true")
parser.add_argument("-v", "--verbose", help="Enable verbose logging", action="store_true")
args = parser.parse_args()

if args.verbose:
    logger.setLevel(logging.DEBUG)

# Download directory setup
download_dir = os.path.join(os.path.expanduser("~"), "Downloads", args.outputdir)
if not os.path.exists(download_dir):
    logger.debug(f"Creating download directory: {download_dir}")
    os.makedirs(download_dir)

temp_dir = tempfile.mkdtemp()
logger.debug(f"Temporary directory created: {temp_dir}")

driver = None

try:
    # Configure Chrome options
    options = Options()
    prefs = {
        "download.default_directory": temp_dir,
        "download.prompt_for_download": args.prompt_for_download,
        "download.directory_upgrade": False,
        "safebrowsing.enabled": True,
    }
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--headless=new")  # Run in headless mode
    driver = webdriver.Chrome(options=options)

    # Start the login process
    driver.get("https://zaim.net/user_session/new")
    driver.find_element(By.ID, "email").send_keys(ZAIM_ID)
    driver.find_element(By.ID, "password").send_keys(ZAIM_PASSWORD)
    driver.find_element(By.CLASS_NAME, "id-zaim-button__subtext").click()

    try:
        wait = WebDriverWait(driver, 10)
        element = wait.until(expected_conditions.visibility_of_element_located((By.ID, "passcode")))
    except Exception as e:
        logger.error(f"Timeout: Expected field not found: {e}")
        raise ValueError(f"Timeout: Expected field not found: {e}") from e

    TOTP = args.totp if args.totp else ""
    if TOTP:
        driver.find_element(By.ID, "passcode").send_keys(TOTP)
        driver.find_element(By.XPATH, "/html/body/div/main/div/div[1]/div[2]/div[2]/form/input[3]").click()

    # Wait for the page to load after login
    time.sleep(3)
    driver.get("https://content.zaim.net/home/money")

    try:
        wait = WebDriverWait(driver, 10)
        element = wait.until(
            expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "[href='#collapseDownload']"))
        )
    except Exception as e:
        logger.error(f"Timeout: Expected field not found: {e}")
        raise ValueError(f"Timeout: Expected field not found: {e}") from e

    # Start the download process
    driver.find_element(By.CSS_SELECTOR, "[href='#collapseDownload']").click()

    try:
        wait = WebDriverWait(driver, 10)
        element = wait.until(expected_conditions.visibility_of_element_located((By.NAME, "start_year")))
    except Exception as e:
        logger.error(f"Timeout: Expected field not found: {e}")
        raise ValueError(f"Timeout: Expected field not found: {e}") from e

    select_element = driver.find_element(By.NAME, "start_year")
    option_to_select = select_element.find_element(By.CSS_SELECTOR, f"option[value='{args.start_year}']")
    option_to_select.click()
    select_element = driver.find_element(By.NAME, "start_month")
    option_to_select = select_element.find_element(By.CSS_SELECTOR, f"option[value='{args.start_month}']")
    option_to_select.click()
    select_element = driver.find_element(By.NAME, "start_day")
    option_to_select = select_element.find_element(By.CSS_SELECTOR, f"option[value='{args.start_day}']")
    option_to_select.click()
    select_element = driver.find_element(By.NAME, "end_year")
    option_to_select = select_element.find_element(By.CSS_SELECTOR, f"option[value='{args.end_year}']")
    option_to_select.click()
    select_element = driver.find_element(By.NAME, "end_month")
    option_to_select = select_element.find_element(By.CSS_SELECTOR, f"option[value='{args.end_month}']")
    option_to_select.click()
    select_element = driver.find_element(By.NAME, "end_day")
    option_to_select = select_element.find_element(By.CSS_SELECTOR, f"option[value='{args.end_day}']")
    option_to_select.click()
    select_element = driver.find_element(By.ID, "MoneyCharset")
    option_to_select = select_element.find_element(By.CSS_SELECTOR, f"option[value='{args.charset}']")
    option_to_select.click()
    download_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'].btn.btn-success")
    download_button.click()

    logger.info("Download started. Waiting for the file to be downloaded...")
    start_time = time.time()
    while True:
        files = [f for f in os.listdir(temp_dir) if f.endswith(".csv") and not f.endswith(".crdownload")]
        if files:
            logger.debug(f"Files found in temp directory: {files}")
            downloaded_file = os.path.join(temp_dir, files[0])
            break
        if time.time() - start_time > 30:
            logger.error("Download timed out after 30 seconds.")
            raise ValueError("Download timed out after 30 seconds.")
        time.sleep(1)

    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S%f")[:14]
    new_file_name = os.path.join(
        download_dir,
        f"zaim_data_{args.start_year}{args.start_month}{args.start_day}_{args.end_year}{args.end_month}{args.end_day}_{timestamp}.csv",
    )

    try:
        shutil.move(downloaded_file, new_file_name)
        logger.info(f"File downloaded to: {new_file_name}")
    except Exception as e:
        logger.error(f"Failed to rename or move file: {e}")
finally:
    if driver is not None:
        driver.quit()

    # Clean up temporary directory
    try:
        shutil.rmtree(temp_dir)
        logger.debug(f"Removed temporary directory {temp_dir}")
    except Exception as e:
        logger.error(f"Failed to remove temporary directory {temp_dir}: {e}")
