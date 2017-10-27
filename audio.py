import re
from subprocess import Popen, PIPE
import os


def file_info(filepath):
    get_info = ['sox', '--info', filepath]
    process = Popen(get_info, stdout=PIPE, encoding='utf-8')
    info, err = process.communicate()
    return info.splitlines()


def split_letters(audio_file, output, duration='0.03', threshold='9.5%', verbosity=2):
    cmd = f'sox -V{verbosity} {audio_file} {output} silence 1 {duration} {threshold} 1 {duration} {threshold} : newfile : restart'
    os.system(cmd)


def count_letters(letter_audio_file):
    name, extension = letter_audio_file.split('.')
    count = len([i for i in os.listdir() if i.startswith(name)])
    print(f'{count} letras')
    return count


def validate_results(letter_audio_file):
    LETTER_COUNT = 6
    return count_letters(letter_audio_file) == LETTER_COUNT


def clean_up(letter_audio_file):
    name, extension = letter_audio_file.split('.')
    letters = [i for i in os.listdir() if i.startswith(name)]
    for i in letters:
        filepath = os.path.join(os.getcwd(), i)
        os.remove(filepath)

def get_captchas():
    pattern = '^captcha_\d{4}\.wav$'
    cwd = os.getcwd()
    captchas = [os.path.join(cwd, i) for i in os.listdir() if re.match(pattern, i)]
    return captchas


if __name__ == '__main__':
    print(get_captchas())
    CAPTCHA_AUDIO_FILE = 'captcha_0000.wav'
    LETTER_AUDIO_FILE = 'letter.wav'
    DURATION = 0.025
    THRESHOLD = '10.5%'

    split_letters(CAPTCHA_AUDIO_FILE, LETTER_AUDIO_FILE, duration=DURATION,
                  threshold=THRESHOLD)
    is_valid = validate_results(LETTER_AUDIO_FILE)
    print('Validação:', is_valid)
    clean_up(LETTER_AUDIO_FILE)
