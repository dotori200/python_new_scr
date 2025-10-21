import requests # requests = 웹페이지 접속할 때 사용하는 라이브러리
url = 'https://www.hollys.co.kr/store/korea/korStore2.do'
# 서버에 보낼 데이터
from_data = {
'pageNo' : 1,
'sido' : '',
'gugun' :'',
'store' : ''
}

response = requests.post(url,data=from_data)
print (response.text[:500])

