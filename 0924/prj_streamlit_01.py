import streamlit as st
import pandas as pd
import pymysql
import matplotlib.pyplot as plt

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
st.set_page_config(page_title="연료별 차량 데이터", layout="wide")

# 메인 제목
st.title("🚗 연료별 차량 데이터")

# 사이드바 메뉴
menu = st.sidebar.radio("메뉴 선택", ["연료별 차량 현황", "FAQ"])


# -------------------------------
# 1. 연료별 차량 현황 페이지
# -------------------------------
if menu == "연료별 차량 현황":
    st.subheader("📊 연료별 차량 현황")

    df = load_data()

    # ---------------------------
    # 선택 옵션
    # ---------------------------
    fuel_options = ["전체"] + df["fuel_name"].unique().tolist()
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

    # ---------------------------
    # 그래프 그리기
    # ---------------------------
    grouped = filtered_df.groupby(["year", "fuel_name"])["amount"].sum().reset_index()

    fig, ax = plt.subplots(figsize=(10, 6))

    for fuel in grouped["fuel_name"].unique():
        temp = grouped[grouped["fuel_name"] == fuel]
        ax.plot(temp["year"], temp["amount"], marker="o", label=fuel)

    ax.set_title("연료별 차량 등록 현황")
    ax.set_xlabel("연도")
    ax.set_ylabel("차량 수")
    ax.legend()

    st.pyplot(fig)