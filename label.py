import os
import re
import time

import matplotlib as
from PIL import Image
DATA_FOLDER = os.path.join(os.getcwd(), 'data')

def get_images(path, select_labeled=False):
    pattern = '^captcha_\d{1,4}\.png$'
    if select_labeled:
        pattern = '^captcha_\d{1,4}\_([a-z]|[0-9]){6}.png$'
    images = filter(lambda x: re.match(pattern, x), os.listdir(DATA_FOLDER))
    return [os.path.join(path, i) for i in sorted(list(images))]


from IPython import display
for i in range(0, 10):
    time.sleep(1)
    display.clear_output()
    display.display(Image.open(images[i]))
