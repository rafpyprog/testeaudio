import os
import time

from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.common.exceptions import NoSuchElementException


def set_chrome():
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : os.getcwd()}
    options.add_experimental_option("prefs", prefs)
    return Chrome(chrome_options=options)
    driver = Chrome()


def click_download_audio(player):
    action = webdriver.common.action_chains.ActionChains(driver)
    x, y = 270, -1
    action.move_to_element_with_offset(player, x, -1)
    action.click()
    action.perform()


def get_captcha():
    global driver
    driver.get(SIPAC)
    driver.get(SOUND)
    player = driver.find_element_by_tag_name('video')
    click_download_audio(player)


SIPAC = 'https://www.receita.fazenda.gov.br/Aplicacoes/SSL/ATFLA/Sipac.App/'
SOUND = ('https://www.receita.fazenda.gov.br/Aplicacoes/SSL/ATFLA/Sipac.App/'
         'GerarSomCaptcha.aspx?sid=0.2556393534615946')
WAIT = 2

driver = set_chrome()

for i in range(0, 100):
    while True:
        try:
            get_captcha()
        except NoSuchElementException:  # Server error: Too many requests
            time.sleep(WAIT)
        else:
            break


driver.quit()
