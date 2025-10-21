import os
import requests

url = f'https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=ZmEyMDg2ODFlOGY2ZDkyODg3ZjdjMTFmYzc0OWYwNDc=&itmId=M0010+M0011+&objL1=ALL&objL2=ALL&objL3=ALL&objL4=ALL&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=Y&startPrdDe=2023&endPrdDe=2023&orgId=426&tblId=DT_426001_M001'

response = requests.get(url)
#print(response.text)
data_dict = response.json()
import json
json_print = json.dumps(data_dict,indent=4,ensure_ascii=False)
print(json_print)