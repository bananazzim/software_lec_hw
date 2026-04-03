import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
import urllib3

# 보안 경고 숨김
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- 1. 기본 설정 ---
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
KEYWORDS = ['자연','농', '농업', '스마트팜', '농식품', '농촌', '귀농', '딸기', '원예', '작물', '청년농', '청년창업', '온실', '재배', '스마트농업', '농기계', '농산물']
# 제외할 부서 목록
EXCLUDE_HOSTS = ['구제역방역과', '축산경영과', '조류인플루엔자방역과', '반려산업동물의료과'] 

BIZINFO_URL = "https://www.bizinfo.go.kr/sii/siia/selectSIIA200View.do?rows=100&cpage={}"
MAFRA_URL = "https://www.mafra.go.kr/home/5108/subview.do?page={}"

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
                
                # 필터링
                if post_date < target_date: continue 
                if not any(keyword in title for keyword in KEYWORDS): continue 
                    
                if not any(d['title'] == title for d in results):
                    results.append({"agency": "기업마당", "host": host, "title": title, "date": date_str})
                    
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
            # 공공기관에서 자주 쓰는 페이지 파라미터 모두 투입
            url = f"https://www.mafra.go.kr/home/5108/subview.do?page={page}&pageIndex={page}"
            response = requests.get(url, headers=HEADERS, timeout=10, verify=False) 
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            rows = soup.select('tbody tr')
            
            # --- [진단용 출력] ---
            if page == 1:
                print(f"  -> 1페이지에서 {len(rows)}개의 게시글(tr)을 찾았습니다.")
                if len(rows) == 0:
                    print("  !!! [경고] 게시글을 0개 찾았습니다. 사이트가 로봇을 차단했거나, 게시판 구조가 완전히 다릅니다.")
            # --------------------
            
            for row in rows:
                # 조건 완화: 복잡한 태그 말고 일단 아무 a 태그나 무조건 찾기
                title_tag = row.select_one('a')
                if not title_tag: continue
                
                title = title_tag.text.strip()
                if not title: continue # 제목이 빈칸이면 패스
                
                # 주최기관 유연하게 추출 (.name 이라는 클래스를 가진 어떤 태그든)
                host_tag = row.select_one('.name')
                host = host_tag.text.strip() if host_tag else "농식품부"
                if host in EXCLUDE_HOSTS: continue
                
                # ★가장 핵심★ 날짜 태그를 찾지 않고, 텍스트 전체에서 '0000-00-00' 형태를 억지로 뜯어냄
                date_match = re.search(r'\d{4}[-./]\d{2}[-./]\d{2}', row.text)
                if not date_match: continue
                
                # '.' 이나 '/' 가 들어있어도 '-'로 통일
                date_clean = date_match.group().replace('.', '-').replace('/', '-')
                
                post_date = datetime.strptime(date_clean, '%Y-%m-%d')
                
                # 필터링
                if post_date < target_date: continue
                if not any(keyword in title for keyword in KEYWORDS): continue
                
                if not any(d['title'] == title for d in results):
                    results.append({"agency": "농식품부", "host": host, "title": title, "date": date_clean})
                    
        print(f"   -> 완료: {len(results)}건 수집됨.\n")
        return results
    except Exception as e:
        print(f"!!! 농식품부 오류: {e}\n")
        return []

# --- 4. 카톡 메시지 생성 ---
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
    # 180일 전 날짜 기준
    target_date = datetime.now() - timedelta(days=20)
    
    # 두 사이트 데이터 수집 및 병합
    all_news = fetch_bizinfo(target_date) + fetch_mafra(target_date)
    
    # 카톡 포맷 출력
    final_msg = make_kakaotalk_msg(all_news)
    
    print("="*40)
    print("=== 카톡 복사/붙여넣기 용 ===")
    print("="*40 + "\n")
    print(final_msg)
    print("\n" + "="*40)