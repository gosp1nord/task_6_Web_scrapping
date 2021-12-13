import bs4
import re
import requests
import time


KEYWORDS = ['дизайн', 'фото', 'web', 'python']

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
    'sec-ch-ua-platform': "Windows",
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}

def get_requests(link):
    answer = requests.get(link, headers=headers)
    answer.raise_for_status()
    soup = bs4.BeautifulSoup(answer.text, 'html.parser')
    return soup

def scrap():
    link = "https://habr.com/ru/all/"
    answer = get_requests(link)
    articles = answer.find_all('article')
    flag = True
    for article in articles:
        href_ = article.find('a', class_="tm-article-snippet__title-link")['href']
        link = f"https://habr.com{href_}"
        full_article = get_requests(link)
        full_text = full_article.find('div', class_="tm-article-body").get_text()

        for i in KEYWORDS:
            pattern = f'(^|\\s){i}[^A-Za-zА-Яа-яЁё0-9]'
            res = re.search(pattern, full_text.lower())
            if res:
                title = full_article.find('h1', class_="tm-article-snippet__title tm-article-snippet__title_h1").get_text()
                date_time = article.find('span', class_="tm-article-snippet__datetime-published").find("time")['title']
                date_time = str(date_time).split(',')
                date = date_time[0]
                print(f"<{date}> - <{title}> - <{link}>")
                flag = False
                break
        time.sleep(1)
    if flag:
        print("Новых статей со словами из списка не опубликовано")


if __name__ == "__main__":
    scrap()
