# pip install selenium webdriver-manager pandas
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time, pandas as pd

URL = "https://www.kia.com/kr/customer-service/center/faq"

def make_driver(headless=False):
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--start-maximized")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_argument("user-agent=Mozilla/5.0")
    svc = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=svc, options=opts)

def wait_body(driver, t=15):
    WebDriverWait(driver, t).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

def click_confirm_if_any(driver):
    for xp in [
        "//button[normalize-space()='확인']",
        "//*[@role='button' and contains(., '확인')]",
        "//button[contains(., '확인')]",
    ]:
        try:
            el = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, xp)))
            driver.execute_script("arguments[0].click();", el)
            time.sleep(0.4)
            return True
        except: pass
    return False

def find_header_buttons(driver):
    # 질문(아코디언 헤더) 후보들: aria-controls가 가장 신뢰도 높음
    candidates = [
        "button[aria-controls]",                 # 가장 선호
        "button[aria-expanded]",                 # 보조
        "button.accordion-header",               # 관용 클래스
        ".faq button", ".accordion button"       # 최후 보정
    ]
    for css in candidates:
        btns = driver.find_elements(By.CSS_SELECTOR, css)
        # 의미 있는 버튼만 필터(텍스트가 있는 것 위주)
        btns = [b for b in btns if (b.text or b.get_attribute("aria-controls"))]
        if len(btns) >= 1:
            return btns
    return []

def get_panel_text(driver, btn):
    """
    1) aria-controls 로 패널 id 찾기
    2) 없으면 형제/부모 기준으로 패널 추정
    3) .text 가 비면 innerText로 보정 (동적 렌더링 대응)
    """
    # 1) aria-controls
    pid = btn.get_attribute("aria-controls")
    panel = None
    if pid:
        try:
            panel = driver.find_element(By.ID, pid)
        except: panel = None

    # 2) 형제/부모 기준 추정 (다양한 사이트 구조 대응)
    if panel is None:
        for xp in [
            "./following-sibling::*[1]",
            "../following-sibling::*[1]",
            "../../following-sibling::*[1]",
            "./ancestor::*[self::li or self::div][1]/following-sibling::*[1]"
        ]:
            try:
                p = btn.find_element(By.XPATH, xp)
                # 패널일만한 클래스/role 판별
                klass = (p.get_attribute("class") or "").lower()
                role  = (p.get_attribute("role") or "").lower()
                if any(k in klass for k in ["panel","answer","content","accordion"]) or role in ["region","group"]:
                    panel = p
                    break
            except: pass

    if panel is None:
        return ""

    # 3) 텍스트 추출 (.text 우선, 비면 innerText)
    txt = panel.text.strip()
    if not txt:
        try:
            txt = driver.execute_script("return arguments[0].innerText;", panel).strip()
        except: pass
    return txt

def crawl_kia_faq_top10(headless=False, save_csv=True):
    driver = make_driver(headless=headless)
    driver.get(URL)
    wait_body(driver, 12)
    click_confirm_if_any(driver)
    time.sleep(0.6)

    # 화면에 보이는 질문 버튼 수집
    buttons = find_header_buttons(driver)
    if not buttons:
        print("질문 버튼을 찾지 못했습니다. 사이트 구조가 바뀌었을 수 있습니다.")
        driver.quit()
        return []

    # 앞에서 10개만 처리
    rows = []
    opened = 0
    for i, btn in enumerate(buttons[:10], start=1):
        try:
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
            # 펼쳐져 있지 않으면 클릭
            expanded = btn.get_attribute("aria-expanded")
            if expanded is None or expanded.lower() != "true":
                driver.execute_script("arguments[0].click();", btn)
                # aria-expanded가 true가 되거나 패널 텍스트가 생길 때까지 잠깐 대기
                for _ in range(10):
                    time.sleep(0.15)
                    expanded = btn.get_attribute("aria-expanded") or ""
                    if expanded.lower() == "true":
                        break
                opened += 1

            q = (btn.text or "").strip()
            if not q:
                # 버튼 text가 비면 aria-label 또는 innerText 시도
                q = (btn.get_attribute("aria-label") or "").strip()
                if not q:
                    q = (driver.execute_script("return arguments[0].innerText;", btn) or "").strip()

            a = get_panel_text(driver, btn)

            if q and a:
                rows.append(("Kia", "TOP10(or FirstPage)", q, a))
                print(f"[{i}] Q: {q[:40]}... | A_len: {len(a)}")
            else:
                print(f"[{i}] 텍스트 미검출 → q_len={len(q)}, a_len={len(a)}")

        except Exception as e:
            print(f"[{i}] 오류: {e}")

    print("탑10 후보 버튼 클릭 개수(시도):", opened)
    print("TOP10 수집 개수:", len(rows))

    if save_csv:
        pd.DataFrame(rows, columns=["company","category","question","answer"])\
          .to_csv("kia_faq_top10.csv", index=False, encoding="utf-8-sig")
        print("CSV 저장 완료: kia_faq_top10.csv")

    driver.quit()
    return rows

if __name__ == "__main__":
    crawl_kia_faq_top10(headless=False)

