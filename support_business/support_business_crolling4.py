import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
import urllib3
import time # ★ 서버 차단 방지를 위한 시간 지연 모듈 추가

# 보안 경고 숨김
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- 1. 기본 설정 ---
# ★ 헤더를 더 사람(브라우저)처럼 보이게 변경
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
}

KEYWORDS = ['자연','농', '농업', '스마트팜', '농식품', '농촌', '귀농', '딸기', '원예', '작물', '청년농', '청년창업', '온실', '재배', '스마트농업', '농기계', '농산물']
EXCLUDE_HOSTS = ['구제역방역과', '축산경영과', '조류인플루엔자방역과', '반려산업동물의료과'] 

BIZINFO_URL = "https://www.bizinfo.go.kr/sii/siia/selectSIIA200View.do?rows=100&cpage={}"
MAFRA_URL = "https://www.mafra.go.kr/home/5108/subview.do?page={}"
KOAT_URL = "https://www.koat.or.kr/board/business/list.do"
SMARTFARM_URL = "https://www.smartfarmkorea.net/board/list.do?menuId=M010705" # 스마트팜코리아 공고게시판

# --- 2. 기업마당 크롤링 ---
def fetch_bizinfo(target_date):
    print("1. 기업마당 크롤링 시작 (1~10페이지)...")
    results = []
    try:
        for page in range(1, 11): 
            url = BIZINFO_URL.format(page)
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status() 
            soup = BeautifulSoup(response.text, 'html.parser')
            
            rows = soup.select('tbody tr') 
            for row in rows:
                tds = row.find_all('td')
                if len(tds) < 7: continue
                
                title_tag = tds[2].select_one('a')
                if not title_tag: continue
                title = title_tag.text.strip()
                
                host = tds[4].text.strip()
                date_str = tds[6].text.strip()
                
                post_date = datetime.strptime(date_str, '%Y-%m-%d')
                
                if post_date < target_date: continue 
                if not any(keyword in title for keyword in KEYWORDS): continue 
                    
                if not any(d['title'] == title for d in results):
                    results.append({"agency": "기업마당", "host": host, "title": title, "date": date_str})
            
            # 페이지 넘길 때 1초 대기
            time.sleep(1)
                    
        print(f"   -> 완료: {len(results)}건 수집됨.\n")
        return results
    except Exception as e:
        print(f"!!! 기업마당 오류: {e}\n")
        return []

# --- 3. 농식품부 크롤링 ---
def fetch_mafra(target_date):
    print("2. 농식품부 크롤링 시작 (1~5페이지)...")
    results = []
    
    try:
        for page in range(1, 6): 
            url = f"https://www.mafra.go.kr/home/5108/subview.do?page={page}&pageIndex={page}"
            response = requests.get(url, headers=HEADERS, timeout=10, verify=False) 
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            rows = soup.select('tbody tr')
            
            for row in rows:
                title_tag = row.select_one('a')
                if not title_tag: continue
                
                title = title_tag.text.strip()
                if not title: continue 
                
                host_tag = row.select_one('.name')
                host = host_tag.text.strip() if host_tag else "농식품부"
                if host in EXCLUDE_HOSTS: continue
                
                date_match = re.search(r'\d{4}[-./]\d{2}[-./]\d{2}', row.text)
                if not date_match: continue
                
                date_clean = date_match.group().replace('.', '-').replace('/', '-')
                post_date = datetime.strptime(date_clean, '%Y-%m-%d')
                
                if post_date < target_date: continue
                if not any(keyword in title for keyword in KEYWORDS): continue
                
                if not any(d['title'] == title for d in results):
                    results.append({"agency": "농식품부", "host": host, "title": title, "date": date_clean})
            
            # ★ 농식품부 서버 차단 방지를 위해 2초 대기
            time.sleep(2)
            
        print(f"   -> 완료: {len(results)}건 수집됨.\n")
        return results
    except Exception as e:
        print(f"!!! 농식품부 오류: {e}\n")
        return []

# --- 4. 한국농업기술진흥원(KOAT) 크롤링 ---
def fetch_koat(target_date):
    print("3. 농업기술진흥원 크롤링 시작 (1페이지)...")
    results = []
    
    try:
        response = requests.get(KOAT_URL, headers=HEADERS, timeout=10, verify=False)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        rows = soup.select('tbody tr')
        for row in rows:
            title_td = row.find('td', class_='textCut')
            if not title_td: continue
            
            title_tag = title_td.find('a')
            if not title_tag: continue
            title = title_tag.text.strip()
            
            tds = row.find_all('td')
            if len(tds) < 5: continue
            
            date_str = tds[4].text.strip()
            date_match = re.search(r'\d{4}[-./]\d{2}[-./]\d{2}', date_str)
            if not date_match: continue
            
            date_clean = date_match.group().replace('.', '-').replace('/', '-')
            post_date = datetime.strptime(date_clean, '%Y-%m-%d')
            
            if post_date < target_date: continue
            if not any(keyword in title for keyword in KEYWORDS): continue
            
            if not any(d['title'] == title for d in results):
                results.append({"agency": "농진원", "host": "사업공고", "title": title, "date": date_clean})
                
        print(f"   -> 완료: {len(results)}건 수집됨.\n")
        return results
    except Exception as e:
        print(f"!!! 농업기술진흥원 오류: {e}\n")
        return []

# --- 5. 스마트팜 코리아 크롤링 ---
def fetch_smartfarm(target_date):
    print("4. 스마트팜 코리아 크롤링 시작 (1페이지)...")
    results = []
    
    try:
        response = requests.get(SMARTFARM_URL, headers=HEADERS, timeout=10, verify=False)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        rows = soup.select('tbody tr')
        for row in rows:
            # 날짜 추출
            date_match = re.search(r'\d{4}[-./]\d{2}[-./]\d{2}', row.text)
            if not date_match: continue
            
            date_clean = date_match.group().replace('.', '-').replace('/', '-')
            post_date = datetime.strptime(date_clean, '%Y-%m-%d')
            
            # 제목 추출
            title_tag = row.select_one('a')
            if title_tag:
                title = title_tag.text.strip()
            else:
                tds = row.find_all('td')
                if len(tds) < 3: continue
                title = tds[1].text.strip() # 보통 2번째 열이 제목
                
            # 쓸데없는 공백 텍스트 제거
            title = re.sub(r'\s+', ' ', title)
            if not title: continue
            
            if post_date < target_date: continue
            if not any(keyword in title for keyword in KEYWORDS): continue
            
            if not any(d['title'] == title for d in results):
                results.append({"agency": "스마트팜코리아", "host": "공고확인", "title": title, "date": date_clean})
                
        print(f"   -> 완료: {len(results)}건 수집됨.\n")
        return results
    except Exception as e:
        print(f"!!! 스마트팜 코리아 오류: {e}\n")
        return []

# --- 6. 카톡 메시지 생성 ---
def make_kakaotalk_msg(news_list):
    today = datetime.now()
    week_number = (today.day - 1) // 7 + 1 
    
    msg = f"{today.strftime('%y년 %m월')} {week_number}주차\n"
    
    if not news_list:
        msg += "- (수집된 관련 소식이 없습니다.)\n"
    else:
        for news in news_list:
            msg += f"- {news['agency']}({news['host']})_{news['title']} [{news['date']}]\n"
            
    return msg

# --- 메인 실행 ---
if __name__ == "__main__":
    # 20일 전 날짜 기준
    target_date = datetime.now() - timedelta(days=20)
    
    # 4개 사이트 데이터 수집 및 병합
    all_news = fetch_bizinfo(target_date) + fetch_mafra(target_date) + fetch_koat(target_date) + fetch_smartfarm(target_date)
    
    # 카톡 포맷 출력
    final_msg = make_kakaotalk_msg(all_news)
    
    print("="*40)
    print("=== 카톡 복사/붙여넣기 용 ===")
    print("="*40 + "\n")
    print(final_msg)
    print("\n" + "="*40)