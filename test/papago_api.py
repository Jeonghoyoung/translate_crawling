import os, sys
import requests


'''
id : D6MyhofTVhSS2id_DrGH
secret :  PvT06SvA5G
'''
def get_translate(text, lan):
    client_id = "D6MyhofTVhSS2id_DrGH"  # 개발자센터에서 발급받은 Client ID 값
    client_secret = "PvT06SvA5G"  # 개발자센터에서 발급받은 Client Secret 값

    data = {'text' : text,
            'source' : 'ko',
            'target': lan}

    url = "https://openapi.naver.com/v1/papago/n2mt"

    header = {"X-Naver-Client-Id":client_id,
              "X-Naver-Client-Secret":client_secret}

    response = requests.post(url, headers=header, data= data)
    rescode = response.status_code

    if(rescode==200):
        t_data = response.json()
        return t_data['message']['result']['translatedText']
    else:
        print("Error Code:" , rescode)
        return None


a = get_translate('반가워요', 'en')
print(a)
