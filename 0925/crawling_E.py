# ev_faq_crawl_to_db_final.py
# pip install selenium webdriver-manager pandas pymysql

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import pymysql
import time

URL = "https://www.kia.com/kr/vehicles/kia-ev/guide/faq"

# ======================
# 1) 크롤링 (상위 6개)
# ======================
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get(URL)
print("사이트 접속")
time.sleep(2)

# (있으면) '확인' 팝업 닫기
try:
    ok_btn = driver.find_element(By.XPATH, "//button[contains(., '확인')]")
    ok_btn.click()
    time.sleep(1)
except:
    pass

# 질문 버튼(아코디언 헤더) 찾기
buttons = driver.find_elements(By.CSS_SELECTOR, "button[aria-controls]")
print("질문 버튼 개수:", len(buttons))

# 앞에서 6개만
buttons = buttons[:6]

# 펼치기
for i, btn in enumerate(buttons, start=1):
    try:
        btn.click()
        time.sleep(0.3)
    except Exception as e:
        print(f"[{i}] 클릭 실패:", e)

# Q/A 추출
rows = []
for i, btn in enumerate(buttons, start=1):
    try:
        q = btn.text.strip()
        panel_id = btn.get_attribute("aria-controls")
        ans_el = driver.find_element(By.ID, panel_id)
        a = ans_el.text.strip()
        if q and a:
            # company 제거 / category만 유지 (EV로 저장)
            rows.append(("EV", q, a))
            print(f"[{i}] Q: {q} | A_len: {len(a)}")
    except Exception as e:
        print(f"[{i}] 텍스트 읽기 실패:", e)

print("수집 개수:", len(rows))

# CSV 저장(확인용)
df = pd.DataFrame(rows, columns=["category", "question", "answer"])
df.to_csv("ev_faq.csv", index=False, encoding="utf-8-sig")
print("CSV 저장 완료: ev_faq.csv")

# 브라우저 종료
time.sleep(1)
driver.quit()

# ============================================
# 2) MySQL 저장 (company/crawled_at 없이 설계)
#    - 테이블 자동 생성(없으면)
#    - 과거 스키마에 company/crawled_at 있으면 자동 삭제
# ============================================
DB_HOST = "localhost"
DB_USER = "root"
DB_PW   = "root1234"   # <-- 실제 비번으로 바꾸세요
DB_NAME = "car_db"

try:
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PW,
                           db=DB_NAME, charset="utf8mb4")
    cur = conn.cursor()

    # 2-1) ev_faq 테이블(최종 스키마) 생성: id, category, question, answer

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ev_faq (
      id BIGINT AUTO_INCREMENT PRIMARY KEY,
      category  VARCHAR(100) NULL,
      question  TEXT         NOT NULL,
      answer    MEDIUMTEXT   NOT NULL,
      UNIQUE KEY uq_question (question(255))
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # 2-2) 과거에 만들었던 company/crawled_at 컬럼이 남아있다면 드롭
    #      (실패해도 통과하도록 try/except 처리)
    try:
        cur.execute("ALTER TABLE ev_faq DROP COLUMN company;")
        print("기존 company 컬럼 삭제")
    except Exception:
        pass

    try:
        cur.execute("ALTER TABLE ev_faq DROP COLUMN crawled_at;")
        print("기존 crawled_at 컬럼 삭제")
    except Exception:
        pass

    # 2-3) 데이터 삽입 (중복 질문은 무시)
    #      현재 rows: (category, question, answer)
    if rows:
        cur.executemany(
            "INSERT IGNORE INTO ev_faq (category, question, answer) VALUES (%s, %s, %s)",
            rows
        )
        conn.commit()
        print("MySQL 저장 완료: car_db.ev_faq (company/crawled_at 없이)")

    cur.close()
    conn.close()

except Exception as e:
    print("MySQL 처리 중 오류:", e)

print("=== 작업 완료 ===")
