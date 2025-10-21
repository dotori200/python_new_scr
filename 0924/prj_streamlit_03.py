# app_faq.py
import streamlit as st
import pandas as pd
import pymysql
import plotly.express as px

# -------------------------------
# DB에서 데이터 불러오기 함수
# -------------------------------
def load_data():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="root1234",
        database="prj1",
        charset="utf8mb4"
    )

    query = """
    SELECT 
        m.year,
        m.amount,
        f.fuel_name,
        c.cartype_name
    FROM main_tbl_rawdata m
    JOIN fuel_tbl f ON m.fuel_tbl_fuel_id = f.fuel_id
    JOIN cartype_tbl c ON m.cartype_tbl_cartype_id = c.cartype_id;
    """

    df = pd.read_sql(query, conn)
    conn.close()
    return df


# -------------------------------
# Streamlit 페이지 구성
# -------------------------------
st.set_page_config(page_title="자동차 연료 등록 현황", layout="wide")

# 메인 제목
st.title("🚗 연료별 차량 데이터")

# # 사이드바 메뉴
# menu = st.sidebar.radio("메뉴 선택", ["연료별 차량 현황", "FAQ"])


# -------------------------------
# Streamlit 페이지
# -------------------------------
menu = st.sidebar.selectbox("메뉴", ["연료별 차량 현황", "연도별 연료별 순위", "FAQ"])

df = load_data()

# -------------------------------
# 1) 연료별 차량 현황
# -------------------------------
if menu == "연료별 차량 현황":
    st.subheader("📊 연료별 차량 현황")

    # ---------------------------
    # 선택 옵션
    # ---------------------------
    fuel_order = ["휘발유", "경유", "LPG", "전기", "CNG", "하이브리드", "수소", "기타"]
    fuel_options = ["전체"] + fuel_order
    fuel_choice = st.radio("연료 종류 선택", fuel_options, horizontal=True)

    cartype_options = ["전체"] + df["cartype_name"].unique().tolist()
    cartype_choice = st.radio("차종 선택", cartype_options, horizontal=True)

    # ---------------------------
    # 데이터 필터링
    # ---------------------------
    filtered_df = df.copy()

    if fuel_choice != "전체":
        filtered_df = filtered_df[filtered_df["fuel_name"] == fuel_choice]

    if cartype_choice != "전체":
        filtered_df = filtered_df[filtered_df["cartype_name"] == cartype_choice]

    filtered_df["year"] = filtered_df["year"].astype(int)

    available_fuels = [f for f in fuel_order if f in filtered_df["fuel_name"].unique()]
    filtered_df["fuel_name"] = pd.Categorical(
        filtered_df["fuel_name"], categories=available_fuels, ordered=True
    )

    grouped = filtered_df.groupby(["year", "fuel_name"])["amount"].sum().reset_index()
    year_range = list(range(2015, 2025))  # 2015~2024

    fuel_colors = {
        "휘발유": "#FF0000", "경유": "#808080", "LPG": "#FFA500",
        "전기": "#0000FF", "CNG": "#00BFFF", "하이브리드": "#008000",
        "수소": "#800080", "기타": "#A52A2A"
    }

    fig = px.line(
        grouped,
        x="year",
        y="amount",
        color="fuel_name",
        markers=True,
        category_orders={"fuel_name": available_fuels, "year": year_range},
        color_discrete_map=fuel_colors,
        labels={"year": "연도", "amount": "차량 수", "fuel_name": "연료 종류"},
        title="연료별 차량 등록 현황"
    )

    y_max = grouped["amount"].max() * 1.5

    fig.update_layout(
        xaxis=dict(title=dict(text="연도", font=dict(size=16)), tickmode="linear", tick0=2015, dtick=1),
        yaxis=dict(title=dict(text="차량 수", font=dict(size=16)), tickformat=",d", range=[0, y_max]),
        legend_title_text="연료 종류",
        font=dict(family="Malgun Gothic"),
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# 2) 연도별 연료별 순위 막대그래프
# -------------------------------
elif menu == "연도별 연료별 순위":
    st.subheader("📊 연도별 연료별 순위")

    # ---------------------------
    # 메인에서 연도 선택
    # ---------------------------
    selected_year = st.selectbox("연도 선택", list(range(2015, 2025)))

    df_year = df[df["year"] == selected_year].copy()

    fuel_order = ["휘발유", "경유", "LPG", "전기", "CNG", "하이브리드", "수소", "기타"]
    available_fuels = [f for f in fuel_order if f in df_year["fuel_name"].unique()]
    df_year["fuel_name"] = pd.Categorical(df_year["fuel_name"], categories=available_fuels, ordered=True)

    grouped = df_year.groupby("fuel_name")["amount"].sum().reset_index()
    grouped = grouped.sort_values("amount", ascending=False)

    fuel_colors = {
        "휘발유": "#FF0000", "경유": "#808080", "LPG": "#FFA500",
        "전기": "#0000FF", "CNG": "#00BFFF", "하이브리드": "#008000",
        "수소": "#800080", "기타": "#A52A2A"
    }

    fig = px.bar(
        grouped,
        x="fuel_name",
        y="amount",
        text="amount",
        color="fuel_name",
        color_discrete_map=fuel_colors,
        labels={"fuel_name": "연료 종류", "amount": "차량 수"},
        title=f"{selected_year}년 연료별 차량 수 순위"
    )

    fig.update_traces(texttemplate='%{text:,}', textposition='outside')

    # Y축 최대값 기준 1.5배
    y_max = grouped["amount"].max() * 1.5

    fig.update_layout(
        yaxis=dict(tickformat=",d", range=[0, y_max]),
        xaxis=dict(title=dict(text="연료 종류", font=dict(size=16))),
        yaxis_title=dict(text="차량 수", font=dict(size=16)),
        font=dict(family="Malgun Gothic"),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)
    
# -------------------------------
# FAQ
# -------------------------------

if menu == "FAQ":
    #st.subheader("📌 FAQ")


    # ====== DB 연결 정보 ======
    DB_HOST = "localhost"
    DB_USER = "root"
    DB_PW   = "root1234"   # <- 실제 비번로 바꿔주세요
    DB_NAME = "faq"        # SQL 덤프에 맞춰 'faq' 사용

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
    def load_top10():
        sql = """
        SELECT Q AS question, A AS answer
        FROM tbl
        ORDER BY id ASC
        LIMIT 10;
        """
        return read_sql(sql)

    # 전기차 (faq.ev_tbl: question/answer)
    def load_ev():
        sql = """
       SELECT E_Q AS question, E_A AS answer
        FROM ev_tbl
        ORDER BY id ASC
        LIMIT 10;
        """
        return read_sql(sql)

    # 하이브리드 (faq.hyb_tbl: H_Q/H_A)
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
    st.title("📌 자동차 FAQ")

    # ---- 검색 상태(버튼 위에서 먼저 준비!)
    if "search_term" not in st.session_state:
        st.session_state.search_term = ""
    if "search_clicked" not in st.session_state:
        st.session_state.search_clicked = False

    # 탭 상태(버튼으로 전환)
    if "tab" not in st.session_state:
        st.session_state["tab"] = "TOP10"

    # 탭 전환 시 검색 상태 초기화 + rerun
    def switch_tab(tab_name: str):
        st.session_state.update({
            "tab": tab_name,
            "search_term": "",
            "search_clicked": False
        })
        st.rerun()

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("TOP10", use_container_width=True):
            switch_tab("TOP10")
    with col2:
        if st.button("전기차", use_container_width=True):
            switch_tab("EV")
    with col3:
        if st.button("하이브리드", use_container_width=True):
            switch_tab("HYB")

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

    def trigger_search():
        st.session_state.search_clicked = True

    # 검색 UI (입력창 + 버튼)
    c1, c2 = st.columns([6, 1])
    with c1:
        st.text_input(
            "",  # 라벨 숨김
            key="search_term",
            placeholder="검색어를 입력하세요",
            label_visibility="collapsed",
            on_change=trigger_search   # 엔터로 검색
        )
    with c2:
        if st.button("검색", use_container_width=True):  # 버튼으로 검색
            trigger_search()

    # 검색 적용 (질문(question)만 검색)
    filtered_df = df.copy()
    if st.session_state.search_clicked and st.session_state.search_term.strip():
        kw = st.session_state.search_term.strip()
        filtered_df = filtered_df[
            filtered_df["question"].str.contains(kw, case=False, na=False)
        ]

    # 결과 건수 문구
    if st.session_state.search_clicked:
        st.write(f"🔍 **‘{st.session_state.search_term}’** 에 대한 검색 결과: **{len(filtered_df)}건**")

    # 결과 표시
    if filtered_df.empty:
        st.warning("검색 결과가 없습니다.")
    else:
        for i, row in filtered_df.reset_index(drop=True).iterrows():
            with st.expander(f"{i+1}. {row['question']}"):
                st.write(row["answer"])
