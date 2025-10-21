import streamlit as st
with st.container(horizontal=True, 
                  gap="medium",border=True
                  ):
    st.button("Button 1")
    st.button("Button 2")
    st.button("Button 3")
    st.button("Button 4")
    st.button("Button 5")
    st.button("Button 6")
    st.button("Button 7")
    st.button("Button 8")
    st.button("Button 9")
    st.button("Button 10")

  
st.title("버튼 예제")

# 버튼 생성
if st.button("눌러보세요!"):
    st.write("버튼이 눌렸습니다 🎉")
else:
    st.write("아직 안 눌림 😅")
