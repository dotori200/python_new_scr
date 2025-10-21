# pip install selenium webdriver-manager bs4 pandas
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time

url = "https://www.kia.com/kr/customer-service/center/faq"

# 1) 크롬 드라이버 준비
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 2) 사이트 접속
driver.get(url)
print("사이트 접속했습니다.")
time.sleep(2)

# 3) (있으면) '확인' 팝업 닫기
try:
    # 버튼 텍스트가 '확인'인 경우
    ok_btn = driver.find_element(By.XPATH, "//button[contains(., '확인')]")
    ok_btn.click()
    time.sleep(1)
except:
    pass  # 없으면 그냥 진행

# 4) 화면에 보이는 질문 버튼들 찾기 (아코디언 헤더)
#    aria-controls 속성이 붙은 버튼이 "답변 패널"을 가리킵니다.
buttons = driver.find_elements(By.CSS_SELECTOR, "button[aria-controls]")
print("질문 버튼 개수:", len(buttons))

# 5) 앞에서 10개만 클릭해서 펼치기
buttons = buttons[:10]
for i, btn in enumerate(buttons, start=1):
    try:
        btn.click()
        time.sleep(0.3)  # 펼쳐질 시간 약간 주기
    except:
        pass

# 6) 질문/답변 텍스트 뽑기
#    - 질문: 버튼의 .text
#    - 답변: 버튼의 aria-controls 값(=패널 id)을 이용해서 해당 요소 찾은 뒤 .text
rows = []
for i, btn in enumerate(buttons, start=1):
    try:
        q = btn.text.strip()
        panel_id = btn.get_attribute("aria-controls")
        ans_el = driver.find_element(By.ID, panel_id)
        a = ans_el.text.strip()
        if q and a:
            rows.append(("Kia", "TOP10", q, a))
            print(f"[{i}] Q: {q} | A_len: {len(a)}")
    except Exception as e:
        print(f"[{i}] 읽기 실패:", e)

print("TOP10 수집 개수:", len(rows))

# 7) CSV 저장
df = pd.DataFrame(rows, columns=["company", "category", "question", "answer"])
df.to_csv("kia_faq_top10.csv", index=False, encoding="utf-8-sig")
print("CSV 저장 완료: kia_faq_top10.csv")

# 8) 브라우저 종료
time.sleep(1)
driver.quit()