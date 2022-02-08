from selenium import webdriver as wd
from selenium.webdriver.common.by import By
import time
import re
import pandas as pd
import numpy as np
import datetime

print("시작 시각:"+str(datetime.datetime.now()))
# 해시태그 검색어
keyword = "야식"
count = 200

# 로그인 정보
username = '아이디'
userpw = '비밀번호'
time.sleep(3)

# 해시태그 url 값
url = "https://www.instagram.com/explore/tags/{}/".format(keyword)

# dataframe 만들기 (해시태그는 총 30개까지 크롤링)
insta_df = pd.DataFrame("", index=np.arange(1, count + 1),
                        columns=["account", "date", "t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8", "t9", "t10", "t11",
                                 "t12", "t13", "t14", "t15", "t16", "t17", "t18", "t19", "t20","t21",
                                 "t22", "t23", "t24", "t25", "t26", "t27", "t28", "t29", "t30",])
instagram_account = []
instagram_tags = []
instagram_tag_dates = []

# 인스타 로그인 URL
loginUrl = 'https://www.instagram.com/accounts/login/'


driver = wd.Chrome("./chromedriver")
driver.get(loginUrl)
time.sleep(2)

# login
driver.find_element_by_name('username').send_keys(username)
driver.find_element_by_name('password').send_keys(userpw)
time.sleep(2)
driver.find_element(By.CSS_SELECTOR,'button.sqdOP.L3NKy.y3zKF').click()
time.sleep(3)

# 정보 나중에 저장하기 클릭하고 넘어가기
driver.find_element(By.CSS_SELECTOR,'button.sqdOP.yWX7d.y3zKF').click()
time.sleep(5)
# 설정 나중에하기 클릭하고 넘어가기
driver.find_element(By.CSS_SELECTOR,'button.aOOlW.HoLwm').click()
time.sleep(5)

# 해시태그 검색 창에 "키워드" 검색
driver.get(url)
time.sleep(10)

# 맨 왼쪽 상단 첫 게시물 클릭
#Nnq7C.weEfm
driver.find_element(By.CSS_SELECTOR,'div.v1Nh3.kIKUG._bz0w').click()
time.sleep(3)

# 데이터 기록, 다음 게시물로 클릭
for i in range(count):
    try:
        # account 데이터 기록
        account_data = driver.find_element(By.CSS_SELECTOR,'a.sqdOP.yWX7d._8A5w5.ZIAjV')
        account_text = account_data.text

        # 날짜 기록 (주단위)
        date = driver.find_element(By.CSS_SELECTOR,"time.FH9sR.Nzb55").text  # 날짜 선택

        #날짜 데이터가 시간, 일, 분 단위이면 0주로 변환
        if date.find('시간') != -1 or date.find('일') != -1 or date.find('분') != -1:
            date_text = '0주'
        else:
            date_text = date

        # 해쉬태그 데이터 기록
        data = driver.find_element(By.CSS_SELECTOR,'.C7I1f.X7jCj')
        tag_raw = data.text
        tag = re.findall('#[A-Za-z0-9가-힣]+', tag_raw)
        tag = ''.join(tag).replace("#", " ")  # "#" 제거
        tag_data = tag.split()
    except:
        tag_data = "error"
        date_text = "error"

    try:  # 최대 50초까지 기다렸다가, > 모양 클릭하여 다음 게시물로 넘어가기
        time.sleep(5+np.random.randint(10))# + 랜덤한 시각

        driver.find_element(By.CSS_SELECTOR,'div.l8mY4.feth3').click()

    except:
        print("크롤링이 비정상적으로 종료되었습니다")
        print("에러 발생 시각:"+str(datetime.datetime.now())+" "+ str(i) + "번째 게시물 오류 발생")
        # 결과값 저장
        insta_df.to_csv(keyword + "_" + str(datetime.datetime.now()) + "_results.csv", encoding='utf-8-sig')
        driver.quit()
        quit()

    time.sleep(3)
    print('{}, {}번째 게시물 탐색 완료'.format(time.strftime('%c', time.localtime(time.time())), i + 1))


    # dataframe에 계정정보, 날짜 저장
    insta_df.iloc[i, 0] = account_text
    insta_df.iloc[i, 1] = date_text

    # 해시태그저장, 20개가 넘으면 20개까지만 저장됨
    for j in range(27):
        try:
            insta_df.iloc[i, j + 2] = tag_data[j]
        except:
            break

# 결과값 저장
insta_df.to_csv(keyword +"_"+str(datetime.datetime.now())+ "_results.csv",encoding='utf-8-sig')

# 크롬드라이버 종료
print('크롤링 종료')
driver.quit()
print("종료 시각:"+str(datetime.datetime.now()))