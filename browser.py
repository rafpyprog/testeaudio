import os

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def set_chrome(download_dir=None):
    if not download_dir:
        download_dir = os.getcwd()
    options = ChromeOptions()
    prefs = {"download.default_directory" : download_dir}
    options.add_experimental_option("prefs", prefs)
    return Chrome(chrome_options=options)
    driver = Chrome()


def load_SIPAC(driver, webdriverwait=5):    
    WAIT = WebDriverWait(driver, webdriverwait)
    SIPAC = 'https://www.receita.fazenda.gov.br/Aplicacoes/SSL/ATFLA/Sipac.App/'
    driver.get(SIPAC)
    WAIT.until(EC.visibility_of_element_located((By.ID, 'imgcaptcha')))
