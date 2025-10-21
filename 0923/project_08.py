# ev_faq_crawl_to_db.py
# pip install selenium webdriver-manager bs4 pandas pymysql
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import pymysql
import time

URL = "https://www.kia.com/kr/vehicles/kia-ev/guide/faq"

# 1) 크롬 드라이버 준비
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 2) 접속
driver.get(URL)
print("사이트 접속")
time.sleep(2)

# 3) (있으면) '확인' 팝업 닫기
try:
    ok_btn = driver.find_element(By.XPATH, "//button[contains(., '확인')]")
    ok_btn.click()
    time.sleep(1)
except:
    pass

# 4) 화면의 질문 버튼(아코디언 헤더) 찾기
buttons = driver.find_elements(By.CSS_SELECTOR, "button[aria-controls]")
print("질문 버튼 개수:", len(buttons))

# 앞에서 6개만 대상으로
buttons = buttons[:6]

# 5) 펼치기(클릭)
for i, btn in enumerate(buttons, start=1):
    try:
        btn.click()
        time.sleep(0.3)  # 살짝 대기
    except Exception as e:
        print(f"[{i}] 클릭 실패:", e)

# 6) 질문/답변 추출
rows = []
for i, btn in enumerate(buttons, start=1):
    try:
        q = btn.text.strip()
        panel_id = btn.get_attribute("aria-controls")
        ans_el = driver.find_element(By.ID, panel_id)
        a = ans_el.text.strip()
        if q and a:
            rows.append(("Kia", "EV", q, a))
            print(f"[{i}] Q: {q} | A_len: {len(a)}")
    except Exception as e:
        print(f"[{i}] 텍스트 읽기 실패:", e)

print("수집 개수:", len(rows))

# 7) CSV 저장
df = pd.DataFrame(rows, columns=["company", "category", "question", "answer"])
df.to_csv("ev_faq.csv", index=False, encoding="utf-8-sig")
print("CSV 저장 완료: ev_faq.csv")

# 8) MySQL에 적재 (테이블 생성 + INSERT)
try:
    conn = pymysql.connect(
        host="localhost", user="root", password="root1234",
        db="car_db", charset="utf8mb4"
    )
    cur = conn.cursor()
    # 테이블 없으면 생성
    cur.execute("""
    CREATE TABLE IF NOT EXISTS ev_faq (
      id BIGINT AUTO_INCREMENT PRIMARY KEY,
      company   VARCHAR(50)  NOT NULL,
      category  VARCHAR(100) NULL,
      question  TEXT         NOT NULL,
      answer    MEDIUMTEXT   NOT NULL,
      crawled_at TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
      UNIQUE KEY uq_company_q (company(20), question(255))
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)
    # 데이터 삽입 (중복 질문은 무시)
    cur.executemany(
        "INSERT IGNORE INTO ev_faq (category, question, answer) VALUES (%s,%s,%s,%s)",
        rows
    )
    conn.commit()
    cur.close(); conn.close()
    print("MySQL 저장 완료: car_db.ev_faq")
except Exception as e:
    print("MySQL 저장 중 오류:", e)

# 9) 브라우저 종료
time.sleep(1)
driver.quit()
