import os
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

CAPTCHA_WAV = 'GerarSomCaptcha.wav'

def set_chrome(download_dir=None):
    if not download_dir:
        download_dir = os.getcwd()
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : download_dir}
    options.add_experimental_option("prefs", prefs)
    return Chrome(chrome_options=options)
    driver = Chrome()


def load_SIPAC(webdriverwait=5):
    global driver
    WAIT = WebDriverWait(driver, webdriverwait)
    SIPAC = 'https://www.receita.fazenda.gov.br/Aplicacoes/SSL/ATFLA/Sipac.App/'
    driver.get(SIPAC)
    WAIT.until(EC.visibility_of_element_located((By.ID, 'imgcaptcha')))


def check_too_many_requests_error():
    global driver
    TOO_MANY_REQUESTS = ('The remote server returned an error: (429) '
                         'Too Many Requests.')
    return TOO_MANY_REQUESTS in driver.page_source


def load_audio_captcha(webdriverwait=2, wait_too_many_requests=5):
    global driver
    WAIT = WebDriverWait(driver, webdriverwait)
    SOUND = ('https://www.receita.fazenda.gov.br/Aplicacoes/SSL/ATFLA/'
             'Sipac.App/GerarSomCaptcha.aspx?sid=0.2556393534615946')
    driver.get(SOUND)

    try:
        player = WAIT.until(
                     EC.visibility_of_element_located((By.TAG_NAME, 'video')))
        time.sleep(0.25)
    except TimeoutException:
        if check_too_many_requests_error() is True:
            print('Too many requests.')
            time.sleep(wait_too_many_requests)
            # retry
            load_SIPAC()
            player = load_audio_captcha()
        else:
            raise ConnectionError('Erro inesperado.')

    return player


def click_download_audio(player):
    action = webdriver.common.action_chains.ActionChains(driver)
    x, y = 270, -1
    action.move_to_element_with_offset(player, x, -1)
    action.click()
    action.perform()


def check_download_finished(timeout=2):
    print('Waiting Download')
    is_finished = False
    elapsed_time = 0
    start_time = time.time()

    while is_finished is False and elapsed_time <= timeout:
        files = [i for i in os.listdir() if i == 'GerarSomCaptcha.wav']
        is_finished = bool(files)
        elapsed_time = time.time() - start_time

    if is_finished:
        print('Download realizado com sucesso.')
    else:
        print('Erro no Download.')

    return is_finished


def get_captcha(delay=2.85):
    global driver
    load_SIPAC()
    time.sleep(delay)
    player = load_audio_captcha()
    click_download_audio(player)


if __name__ == '__main__':
    try:
        driver = set_chrome()
        for i in range(306, 10001):
            print(f'\n{i}')
            download_finished = False
            while download_finished is False:
                get_captcha()
                download_finished = check_download_finished()

            audio_name = f'captcha_{str(i).zfill(4)}.wav'
            os.rename(CAPTCHA_WAV, audio_name)
    finally:
        driver.quit()
