from googleapiclient.discovery import build
from google.oauth2 import service_account

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re

def WebsiteLogin():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--start-maximized')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--log-level=1')
    options.add_argument("–disable-extensions")
    options.add_argument('--user-data-dir= ') # directory of chrome driver
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
    global driver
    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = options)
    driver.get("https://www.tradingview.com/")
    print(driver)
    time.sleep(5)
    try:
        driver.find_element(By.XPATH, r"//img[@aria-hidden='true'][@class='tv-header__user-menu-button-userpic js-userpic-mid'][@src]")
        return "Aleardy logged in!"
    except:
        pass
    driver.find_element(By.XPATH, "//button[@aria-haspopup='true'][@aria-label='Open user menu'][@class='tv-header__user-menu-button tv-header__user-menu-button--anonymous js-header-user-menu-button']").click()
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@data-name='header-user-menu-sign-in'][@role='menuitem'][@class='item-RhC5uhZw item-TZ2SJ2fG']"))
        ).click()
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@class = 'tv-signin-dialog__social tv-signin-dialog__toggle-email js-show-email']"))
            ).click()
    except:
        pass
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@id=\"overlap-manager-root\"]/div/div[2]/div/div"))
        )
    driver.find_element(By.NAME, "password").send_keys("") #insert password
    driver.find_element(By.NAME, "username").send_keys("") #insert username
    driver.find_element(By.XPATH, "//span[@class='tv-button__loader']").click()
    return "Logged in Success!"


def DataCollect():
    try:
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.widgetbar-pages"))
            )
    except:
        driver.find_element(By.XPATH, "//div[@class='button-ocTuaBGx apply-common-tooltip common-tooltip-vertical'][@data-name='base']").click()
    menu = driver.find_element(By.XPATH, "//div[@class='tableHeader-L_zaemu9']").text.splitlines()
    elements = driver.find_element(By.XPATH, "//div[@class='listContainer-zol_jClG']").text.splitlines()
    array = []
    array.append(menu)
    for item in elements:
        if re.search('[a-zA-Z]+',item):
            try:
                array.append(row)
            except:
                pass
            row = []
        row.append(item)
    DataInsertSheet(array)

def DataInsertSheet(lst):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = r"=keys.json"
    creds = None
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes = SCOPES)
    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = 'SPREADSHEET KEY'
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    # Updating values from the spreadsheets
    request = sheet.values().clear(spreadsheetId = SAMPLE_SPREADSHEET_ID, range = "Foaie1!A:Z").execute()
    print(request)
    request = sheet.values().update(spreadsheetId = SAMPLE_SPREADSHEET_ID, range = "Foaie1!A:Z", valueInputOption = "USER_ENTERED", body = {"values": lst}).execute()

if __name__ == "__main__":
    print(WebsiteLogin())
    DataCollect()