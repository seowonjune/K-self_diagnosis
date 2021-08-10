from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from datetime import datetime
import schedule
import time
import random

url='https://hcs.eduro.go.kr/#/loginHome'

#실행 함수
def code(city, school_level, school, name, birth, password):
    passlist1 = [int(i) for i in ' '.join(password).split()]
    options = webdriver.ChromeOptions()

    emptylist = [(4,0),(5,1),(5,2),(5,3),(5,4),(6,0),(7,0),(8,1),(8,2),(8,3),(8,4),(9,0)]

    driver = webdriver.Chrome('/Users/seowonjune/Desktop/chromedriver') #chrome driver 로드
    driver.implicitly_wait(3) #driver가 로드 될 때까지 다리게 함, selenium에서는 자동으로 맞춰주지만 이 코드로 수동으로 변경 가능

    # 사람처럼 보이게 하는 옵션들, 링크:https://devyurim.github.io/python/crawler/2018/08/11/crawler-2.html
    options.add_argument("disable-gpu")   # 가속 사용 x
    options.add_argument("lang=ko_KR")    # 가짜 플러그인 탑재
    #options.add_argument('dasktop')  # user-agent 이름 설정

    driver.get(url) #url에 지정된 주소로 크롬에서 실행

    driver.find_element_by_xpath('//*[@id="btnConfirm2"]').click() #시작 화면에서 넘어가기
    driver.implicitly_wait(2)

    driver.find_element_by_xpath('//*[@id="WriteInfoForm"]/table/tbody/tr[1]/td/button').click() #학교 찾기 클릭
    driver.implicitly_wait(1)

    #시/도 선택
    select=Select(driver.find_element_by_id("sidolabel"))
    select.select_by_index(1) #select index value
    select.select_by_visible_text(city) # select visible text

    #학교급 선택
    select=Select(driver.find_element_by_id("crseScCode"))
    select.select_by_index(1) #select index value
    select.select_by_visible_text(school_level) # select visible text

    #학교명 입력
    driver.find_element_by_id('orgname').send_keys(school)
    driver.implicitly_wait(2)

    #검색 클릭
    driver.find_element_by_xpath('//*[@id="softBoardListLayer"]/div[2]/div[1]/table/tbody/tr[3]/td[2]/button').click()
    driver.implicitly_wait(6)

    #학교 선택
    driver.find_element_by_xpath('//*[@id="softBoardListLayer"]/div[2]/div[1]/ul/li/a/p/a').click()
    driver.implicitly_wait(3)

    #학교 선택 버튼 클릭
    driver.find_element_by_class_name("layerFullBtn").click()
    driver.implicitly_wait(6)

    #이름 입력
    driver.find_element_by_id('user_name_input').send_keys(name)
    driver.implicitly_wait(6)

    #생년월일 입력
    driver.find_element_by_id('birthday_input').send_keys(birth)
    driver.implicitly_wait(6)

    #확인 클릭
    driver.find_element_by_id('btnConfirm').click()
    driver.implicitly_wait(6)

    #password 클릭 
    driver.implicitly_wait(30)
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="password"]').click()
    driver.implicitly_wait(30)
    time.sleep(3)

    for j in range(4,10):
        if j == 5 or j == 8:
            k = 1
            for k in range(1,5):
                tar = '//*[@id="password_mainDiv"]/div['+str(j) + ']/a[' + str(k) + ']'
                checkkey = driver.find_element_by_xpath(tar)
                if '빈칸' in checkkey.get_attribute('aria-label'):
                    emptylist.remove((j,k))
        else:
            k = 0
            tar = '//*[@id="password_mainDiv"]/div['+str(j) + ']/a'
            checkkey = driver.find_element_by_xpath(tar)
            if '빈칸' in checkkey.get_attribute('aria-label'):
                emptylist.remove((j,k))

    time.sleep(2)
    for s in passlist1:
        (j,k) = emptylist[s]
        if k ==0:
            tar = '//*[@id="password_mainDiv"]/div['+str(j) + ']/a'
            driver.find_element_by_xpath(tar).click()
            time.sleep(1)
            driver.implicitly_wait(6)
        else:
            tar = '//*[@id="password_mainDiv"]/div['+str(j) + ']/a[' + str(k) + ']'
            driver.find_element_by_xpath(tar).click()
            time.sleep(1)
            driver.implicitly_wait(6)

    driver.find_element_by_xpath('//*[@id="btnConfirm"]').click()

    time.sleep(3)

    #사용자 설정
    driver.find_element_by_xpath('//*[@id="container"]/div/section[2]/div[2]/ul/li[1]/a/span[1]').click()
    #자가진단
    driver.find_element_by_id('survey_q1a1').click()
    driver.find_element_by_id('survey_q2a1').click()
    driver.find_element_by_id('survey_q3a1').click()

    driver.find_element_by_id('btnConfirm').click()        

    driver.find_element_by_xpath('//*[@id="topMenuWrap"]/ul/li[4]/button').click()
    driver.find_element_by_xpath('/html/body/app-root/div/div[1]/div/button').click()
    print(name +"complete")
    driver.close()

#초기 함수
def start():
    city = '대구광역시'
    school_level=['고등학교', '중학교']
    school = ['대구일과학고등학교', '영남중학교']
    name = ['서원준', '서민준']
    birth = ['041102', '070504']
    passlist = ['1102', '0504']

    for l in range(0, len(name)):
        #time.sleep(random.randrange(300,600))
        code(city, school_level[l], school[l], name[l], birth[l], passlist[l])

schedule.every().day.at("20:51").do(start)

while True:
    schedule.run_pending()
    time.sleep(1)
