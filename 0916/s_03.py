# session 개념
# 파이썬에서 세션을 사용한다는 것 = 상태를 유지한다는 것 
# 세션 상태 관리

import streamlit as st
count = 0
if st.button('카운트 증가'):
    st.write('버튼 클릭됨')
    count += 1
st.write('현재 카운트:' , count) 
