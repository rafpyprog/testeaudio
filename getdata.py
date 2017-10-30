import os

from audio import save_captcha_audio
from browser import set_chrome
from image import save_captcha_image

DATA_FOLDER = os.path.join(os.getcwd(), 'data')

driver = set_chrome(download_dir=DATA_FOLDER)
