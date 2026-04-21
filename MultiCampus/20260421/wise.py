
import pandas as pd
import time
from datetime import datetime


# code_list의 종목 코드의 값들을 유저가 입력한 값들로 채운다

code_list = []

while True:
    input_code = input("종목 코드를 입력하세요 ( 입력 값 종료시 enter ) ")
    # 종목코드는 길이가 6
    if len(input_code) == 6 :
        code_list.append(input_code)
    
    if not(bool(input_code)):
        break

now = datetime.now()
now_str = now.strftime('%y-%m-%d')


for code in code_list:
    base_url = "https://comp.wisereport.co.kr/company/c1010001.aspx?cmp_cd=" + code
    df= pd.read_html(base_url, encoding="euc-kr")[3]
    
    # csv 형식으로 저장 (파일의 이름은 종목코드.csv)
    # 데이터프레임 타입에서 csv 타입으로 변경 -> 타입이 변경될때 사용하는 키워드 (to)
    df.to_csv(f"./{code} {now_str}.csv")

    # Delay
    time.sleep(1)

