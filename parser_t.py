import requests
from bs4 import BeautifulSoup as bss4
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from TikTokApi import TikTokApi

try:
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    dr = webdriver.Chrome(options=options)
except:
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    dr = webdriver.Firefox(options = options)

id_out = []


def parser(link, domen, min_videos, min_watches, min_total_watch):
    try:
        global dr, id_out
        if len(link) < 20:
            link = 'https://www.tiktok.com/'+link+'?lang=uk-UA'
        dr.get(link)
        dom = dr.find_element_by_class_name('share-links').text
        us_id = dr.find_element_by_class_name('share-sub-title').text
        if us_id in id_out:
            return 'Акаунт уже был сдан!'
        if dom not in domen:
            return 'Домен не такой'
        dr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(2)

        videos = dr.find_elements_by_class_name('jsx-2261688415.video-feed-item.three-column-item')
        watches = dr.find_elements_by_class_name('jsx-1036923518.video-count')
        total_watch = 0
        if len(list(videos)) >= min_videos:
            for i in watches:
                if 'K' in i.text:
                    total_watch += 10000
                    continue
                if 'M' in i.text:
                    total_watch += 10000000
                    continue
                if int(i.text) < min_watches:
                    return f'Недостаточно просмотров на каждом видео (мин. {min_watches})'
                total_watch += int(i.text)
            if total_watch < min_total_watch:
                return f'Недостаточно просмотров в сумме (мин. {min_total_watch})'
        else:
            return f'Недостаточно видео (мин. {min_videos})'
        id_out.append(us_id)
        return '✅Ссылка успешно добавлена✅'
    except:
        return 'Неверная ссылка или ник (Ссылка вида: https://www.tiktok.com/@username)'
#print(parser('http://tiktok.com/@lolly8822', 'staemcammunily.ru',15,13,1500))

def parser_test(link, domen, min_videos, min_watches, min_total_watch):
    try:
        global dr
        if len(link) < 20:
            link = 'https://www.tiktok.com/'+link+'?lang=uk-UA'
        dr.get(link)
        dom = dr.find_element_by_class_name('share-links').text
        needed_domen = 'Домен правильный'
        if dom not in domen:
            needed_domen = 'Домен не такой'
        dr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(2)
        videos = dr.find_elements_by_class_name('jsx-2261688415.video-feed-item.three-column-item')
        watches = dr.find_elements_by_class_name('jsx-1036923518.video-count')
        count_videos = 'Достаточно видео'
        total_watch = 0
        enaugh_total_watc = 'Достаточно просмотров в суме'
        enaugh_watc = 'Достаточно просмотров на каждом видео'
        if len(list(videos)) < min_videos:
            count_videos = f'Недостаточно видео, всего {len(list(videos))} (мин. {min_videos})'
        for i in watches:
            if 'K' in i.text:
                total_watch += 10000
                continue
            if 'M' in i.text:
                total_watch += 10000000
                continue
            if int(i.text) < min_watches:
                enaugh_watc = f'Недостаточно просмотров на каждом видео (мин. {min_watches})'
            total_watch += int(i.text)
        if total_watch < min_total_watch:
            enaugh_total_watc = f'Недостаточно просмотров в сумме, всего {total_watch} (мин. {min_total_watch})'
        return needed_domen + '\n' + count_videos + '\n' + enaugh_total_watc + '\n' + enaugh_watc
    except:
        return 'Неверная ссылка или ник (Ссылка вида: https://www.tiktok.com/@username)'