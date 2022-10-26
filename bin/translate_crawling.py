import sys
sys.path.append('./')
from selenium import webdriver
from selenium.webdriver.common.by import By
from util.time_utils import clock
from tqdm import tqdm
import time
import random
import chromedriver_autoinstaller
import util.file_util as ft
import argparse


# Todo 문장이 100개 이상으로 많아짐에 따라 문장이 서로 합쳐지는 오류가 발생함.
# 50개씩 리스트를 따로 나누어 하나씩 append 하는식으로 교체

def translate_crawl(site_info:dict, text_list):
    chrome_filename = chromedriver_autoinstaller.utils.get_chromedriver_filename()
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    try:
        driver = webdriver.Chrome(f'./{chrome_ver}/{chrome_filename}')
    except:
        chromedriver_autoinstaller.install(True)
        driver = webdriver.Chrome(f'./{chrome_ver}/{chrome_filename}')
    driver.implicitly_wait(2)

    driver.get(site_info['url'])

    selected_tag_a = driver.find_element(By.CSS_SELECTOR, site_info['src_text'])
    # test = text_list[:20]
    trans_result = []

    for i in tqdm(range(0, len(text_list), 5)):
        sublist = '\n'.join(text_list[i:i + 5])
        selected_tag_a.send_keys(sublist)
        time.sleep(5)
        result = driver.find_element(By.CSS_SELECTOR,site_info['tgt_text']).text
        trans_result.append(result)
        time.sleep(3)
        selected_tag_a.clear()
    driver.quit()
    return trans_result

@clock
def papago_trans(words, src_lang, tgt_lang):
    info_dict = {
        'url': f'https://papago.naver.com/?sk={src_lang}&tk={tgt_lang}&hn=0',
        'src_text': 'textarea#txtSource',
        'tgt_text': '#txtTarget'
    }
    return translate_crawl(info_dict, words)

@clock
def google_trans(words, src_lang, tgt_lang):
    info_dict = {
        'url': f'https://translate.google.co.kr/?hl=ko&sl={src_lang}&tl={tgt_lang}&op=translate',
        'src_text': 'textarea.er8xn',
        'tgt_text': 'span.HwtZe'
    }
    res = translate_crawl(info_dict, words)
    return res


def papago_apitrans(text, src_lang, tgt_lang):
    client_id = "D6MyhofTVhSS2id_DrGH"  # 개발자센터에서 발급받은 Client ID 값
    client_secret = "PvT06SvA5G"  # 개발자센터에서 발급받은 Client Secret 값

    data = {'text': text,
            'source': src_lang,
            'target': tgt_lang}

    url = "https://openapi.naver.com/v1/papago/n2mt"

    header = {"X-Naver-Client-Id": client_id,
              "X-Naver-Client-Secret": client_secret}

    response = requests.post(url, headers=header, data=data)
    rescode = response.status_code

    if (rescode == 200):
        t_data = response.json()
        return t_data['message']['result']['translatedText']
    else:
        print("Error Code:", rescode)
        return None


def args():
    parser = argparse.ArgumentParser(usage='usage', description='Usage of parameters ')
    parser.add_argument('--lp', required=False, default='zh-CNko')
    parser.add_argument('--crawler', required=False, default='papago')

    parser.add_argument('--input', required=False, default='../data/zhko.txt')
    parser.add_argument('--output', required=False,default='../data/trans')
    return parser.parse_args()


def main():
    result = None

    config = args()
    if len(config.lp) > 10:
        # print(config.lp[:-2])
        print('Check your lp ---')

    else:
        txt_list = ft.get_all_lines(config.input)
        print(f'Input file length : {len(txt_list)}')
        src, tgt = config.lp[:-2], config.lp[-2:]
        print(src)

        if config.crawler == 'papago':
            result = papago_trans(txt_list, src, tgt)
            ft.write_list_file(result, f'{config.output}/papago_{config.lp}.txt')
        elif config.crawler == 'google':
            result = google_trans(txt_list, src, tgt)
            ft.write_list_file(result, f'{config.output}/google_{config.lp}.txt')
        else:
            print('Check your parameters ---')
        print(f'output file length : {len(result)}')
        print(result)

    return result


if __name__ == '__main__':
    main()