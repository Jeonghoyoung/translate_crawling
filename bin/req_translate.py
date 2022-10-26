import sys
sys.path.append('./')
import util.file_util as ft
import requests
from bs4 import BeautifulSoup
from util.time_utils import clock
from tqdm import tqdm

def translage(info, text):
    return


src_lang = 'ko'
tgt_lang = 'en'

text = '안녕하세요.'
url = f'https://papago.naver.com/?sk={src_lang}&tk={tgt_lang}&hn=0&st={text}'
req = requests.get(url)
html = req.text

soup = BeautifulSoup(html, 'html.parser')
print(soup)
e = soup.select('txtTarget > span')
print(e)
