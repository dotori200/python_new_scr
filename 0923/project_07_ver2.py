# pip install pymysql pandas
import pandas as pd
import pymysql

df = pd.read_csv("kia_faq_top10.csv")  # company, category, question, answer

conn = pymysql.connect(
    host="localhost", user="root", password="root1234", db="car_db", charset="utf8mb4"
)
cur = conn.cursor()

# 테이블이 없다면 만들기(한 번만 실행되면 됨)
cur.execute("""
CREATE TABLE IF NOT EXISTS faq_top10_ver2 (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  company   VARCHAR(50)  NOT NULL,
  category  VARCHAR(100) NULL,
  question  TEXT         NOT NULL,
  answer    MEDIUMTEXT   NOT NULL,
  crawled_at TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uq_company_q (company(20), question(255))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
""")

# 데이터 넣기 (중복 질문은 무시)
cur.executemany(
    "INSERT IGNORE INTO faq_top10_ver2 (company, category, question, answer) VALUES (%s,%s,%s,%s)",
    df[["company","category","question","answer"]].values.tolist()
)
conn.commit()
cur.close(); conn.close()
print("MySQL 저장 완료")
