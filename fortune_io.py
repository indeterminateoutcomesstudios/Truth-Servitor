from os import listdir
from os.path import isfile, join
import random

FORTUNE_DIR = './fortunes/'

files = [f for f in listdir(FORTUNE_DIR) if isfile(join(FORTUNE_DIR, f))]

fortunes = {}

for file_name in files:
    file_path = FORTUNE_DIR + file_name
    with open(file_path) as file:
        # Get list of strings using \n%\n as delimiter, filter empty ones out
        fortune_list = list(filter(lambda x: x, file.read().split('\n%\n')))
        fortunes[file_name] = fortune_list

def get_fortune(fn):
    list = fortunes.get(fn, None)

    if list:
        return random.choice(list)
    else:
        return None
