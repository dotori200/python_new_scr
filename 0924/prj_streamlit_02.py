# app_faq.py
import streamlit as st
import pandas as pd
import pymysql
import html

# ====== DB 연결 정보 ======
DB_HOST = "localhost"
DB_USER = "root"
DB_PW   = "root1234"   # <- 실제 비번로 바꿔주세요
DB_NAME = "faq"               # SQL 덤프에 맞춰 'faq' 사용

# ====== 공통: DB에서 DataFrame 읽기 ======
def read_sql(sql):
    conn = pymysql.connect(
        host=DB_HOST, user=DB_USER, password=DB_PW,
        database=DB_NAME, charset="utf8mb4"
    )
    df = pd.read_sql(sql, conn)
    conn.close()
    return df

# TOP10 (faq.tbl: Q/A)  ─ schema: id, category, Q, A
# 참고: 덤프에 따르면 표 이름은 'tbl'이고 Q/A 컬럼명 그대로임  :contentReference[oaicite:3]{index=3}
def load_top10():
    sql = """
    SELECT Q AS question, A AS answer
    FROM tbl
    ORDER BY id ASC
    LIMIT 10;
    """
    return read_sql(sql)

# 전기차 (faq.ev_tbl: question/answer) ─ UNIQUE(question)  :contentReference[oaicite:4]{index=4}
def load_ev():
    sql = """
    SELECT question, answer
    FROM ev_tbl
    ORDER BY id ASC
    LIMIT 10;   -- 현재 덤프엔 6개, 그래도 LIMIT 10으로 여유
    """
    return read_sql(sql)

# 하이브리드 (faq.hyb_tbl: H_Q/H_A) ─ category 기본 'Hybrid'  :contentReference[oaicite:5]{index=5}
def load_hyb():
    sql = """
    SELECT H_Q AS question, H_A AS answer
    FROM hyb_tbl
    ORDER BY id ASC
    LIMIT 10;
    """
    return read_sql(sql)

# ====== Streamlit UI ======
st.set_page_config(page_title="FAQ", layout="wide")
st.title("🚗 자동차 FAQ")

# 버튼 상태를 기억하기 위해 세션 상태 사용 (기본 TOP10)
if "tab" not in st.session_state:
    st.session_state["tab"] = "TOP10"

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("TOP10", use_container_width=True):
        st.session_state["tab"] = "TOP10"
with col2:
    if st.button("전기차", use_container_width=True):
        st.session_state["tab"] = "EV"
with col3:
    if st.button("하이브리드", use_container_width=True):
        st.session_state["tab"] = "HYB"

st.markdown("---")

# 선택된 탭에 따라 데이터 로드
if st.session_state["tab"] == "TOP10":
    st.subheader("TOP10 자주 묻는 질문")
    df = load_top10()
elif st.session_state["tab"] == "EV":
    st.subheader("전기차 FAQ")
    df = load_ev()
else:
    st.subheader("하이브리드 FAQ")
    df = load_hyb()

# 검색(선택사항): 간단 키워드 필터
kw = st.text_input("검색 (질문/답변에서 찾기, 비워두면 전체)")
if kw:
    df = df[df["question"].str.contains(kw, case=False, na=False) |
            df["answer"].str.contains(kw, case=False, na=False)]

# 아코디언(질문 클릭 → 답변 표시)
for i, row in df.reset_index(drop=True).iterrows(): 
    with st.expander(f"{i+1}. {row['question']}"):
        st.write(row["answer"])

