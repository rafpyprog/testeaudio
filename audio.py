from subprocess import Popen, PIPE
import os


def create_noise_profile(audio_sample, outfile='noise.prof'):
    os.system(f'sox {audio_sample} -n noiseprof {outfile}')

def clean_noise(audio_file, noise_profile, output=None, sensivity=0.21):
    if not output:
        output = audio_file
    os.system(f'sox {audio_file} {output} noisered {noise_profile} {sensivity}')

def file_info(filepath):
    get_info = ['sox', '--info', filepath]
    process = Popen(get_info, stdout=PIPE, encoding='utf-8')
    info, err = process.communicate()
    return info.splitlines()

def remove_silence(audio_file, output, duration='0.03', threshold='9.5%'):
    cmd = f'sox -V3 {audio_file} {output} silence 1 {duration} {threshold} 1 {duration} {threshold} : newfile : restart'
    os.system(cmd)

create_noise_profile('ruido_fala.wav', outfile='noise_fala.prof')
clean_noise('captcha.wav', 'noise_fala.prof', output='captcha1_clean.wav', sensivity=.1)

DURATION = 0.025
THRESHOLD = '10.5%'
remove_silence('captcha1.wav', output='silence.wav', duration=DURATION,
               threshold=THRESHOLD)

















AUDIO_FILE = 'captcha.wav'
DURATION = 4
CUT = 0.31

file_info('captcha1.wav')


trim_start = f'sox {audio_file} clean.wav trim {CUT} {4 - 0.09}'
os.system(trim_start)

file_info('clean.wav')


split_audio = f'sox clean.wav out.wav trim 0 0.6 : newfile : restart'
os.system(split_audio)
