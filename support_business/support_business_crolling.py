import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re

BIZINFO_URL = "https://www.bizinfo.go.kr/sii/siia/selectSIIA200View.do?rows=100&cpage={}"
HEADERS = {'User-Agent': 'Mozilla/5.0'}
KEYWORDS = ['그린','종자', '농업', '스마트팜', '농식품', '농촌', '귀농', '딸기', '원예', '작물', '청년농', '청년창업', '온실', '재배', '스마트농업', '농기계', '농산물']

def fetch_bizinfo():
    print("기업마당 크롤링 시작 (1~19페이지 탐색)...")
    results = []
    target_date = datetime.now() - timedelta(days=180)
    
    try:
        # 1. 19페이지까지 탐색
        for page in range(1, 20): 
            url = BIZINFO_URL.format(page)
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status() 
            soup = BeautifulSoup(response.text, 'html.parser')
            
            rows = soup.select('tbody tr') 
            
            for row in rows:
                tds = row.find_all('td')
                if len(tds) < 7: # 데이터가 없는 빈 줄은 건너뜀
                    continue
                
                # 2. 제목 추출
                title_tag = tds[2].select_one('a')
                if not title_tag:
                    continue
                title = title_tag.text.strip()
                
                # 3. 주최 기관(소관부처) 및 등록일 추출
                host = tds[4].text.strip()
                date_str = tds[6].text.strip()
                
                post_date = datetime.strptime(date_str, '%Y-%m-%d')
                
                # 기간 및 키워드 필터링
                if post_date < target_date:
                    continue 
                if not any(keyword in title for keyword in KEYWORDS):
                    continue 
                    
                # 중복 수집 방지
                if not any(d['title'] == title for d in results):
                    results.append({
                        "agency": "기업마당", 
                        "host": host,         # 추가됨
                        "title": title, 
                        "date": date_str      # 추가됨
                    })
                    
        print(f"-> 조건에 맞는 {len(results)}개의 공고 수집 완료.\n")
        return results

    except Exception as e:
        print(f"!!! 오류 발생: {e}")
        return []

def make_kakaotalk_msg(news_list):
    today = datetime.now()
    week_number = (today.day - 1) // 7 + 1 
    
    msg = f"{today.strftime('%y년 %m월')} {week_number}주차\n"
    
    if not news_list:
        msg += "- (수집된 관련 소식이 없습니다.)\n"
    else:
        for news in news_list:
            # 출력 포맷 변경: - 소스(주최기관)_제목 [등록일]
            msg += f"- {news['agency']}({news['host']})_{news['title']} [{news['date']}]\n"
            
    return msg

if __name__ == "__main__":
    biz_news = fetch_bizinfo()
    final_msg = make_kakaotalk_msg(biz_news)
    
    print("="*30)
    print("=== 카톡 복사/붙여넣기 용 ===")
    print("="*30 + "\n")
    print(final_msg)
    print("\n" + "="*30)