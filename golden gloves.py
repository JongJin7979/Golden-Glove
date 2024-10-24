import time
import random
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
# Selenium WebDriver 설정
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
# 날짜 범위 설정
start_date = datetime(2022, 11, 8)
end_date = datetime(2022, 12, 8)
current_date = start_date
# 기사 제목 리스트
all_title_list = []
# 날짜 범위 반복
while current_date <= end_date:
    page_num = 1
    # 최대 페이지 수 찾기
    while True:
        url = f'https://sports.news.naver.com/kbaseball/news/index?date={current_date.strftime("%Y%m%d")}&isphoto=N&page={page_num}'
        driver.get(url)
        time.sleep(2)  # 랜덤 지연 추가
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        # 'next' 버튼이 있는지 확인
        next_button = soup.find(class_='paginate')
        if next_button and next_button.find(class_='next'):
            page_num += 10  # 다음 페이지로 이동
        else:
            max_pages = int(next_button.find('strong').text.strip()) # 최대 페이지 수 결정
            if max_pages == page_num:
                page_num +=10
            else:
                break  # 더 이상 다음 페이지가 없으면 종료
    print('최대 페이지: ',max_pages)
    # 페이지 반복
    page_num = 1  # 페이지 수 초기화
    while page_num <= max_pages:
        url = f'https://sports.news.naver.com/kbaseball/news/index?date={current_date.strftime("%Y%m%d")}&isphoto=N&page={page_num}'
        driver.get(url)
        time.sleep(random.uniform(2, 4))  # 랜덤 지연 추가
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        # 'content' 클래스에서 'text' 클래스 추출
        content_div = soup.find('div', {'class': 'content'})
        if content_div:
            news = content_div.findAll('div', {'class': 'text'})
            if not news:  # 기사가 더 이상 없으면 종료
                break
            for item in news:
                title = item.find('span')  # 제목이 있는 span 태그 찾기
                if title:
                    title_text = title.text.strip()
                    all_title_list.append(title_text)
            print(f"{page_num} 페이지 완료")
            page_num += 1  # 다음 페이지로 이동
        else:
            break  # 'content'가 없으면 종료
    # 다음 날짜로 이동
    current_date += timedelta(days=1)
# DataFrame 생성 및 CSV 파일로 저장
df = pd.DataFrame(all_title_list, columns=["Title"])
df.to_csv('golden_glove_articles.csv', index=False, encoding='utf-8-sig')
# 드라이버 종료
driver.quit()