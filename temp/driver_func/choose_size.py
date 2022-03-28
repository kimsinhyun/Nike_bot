from selenium.webdriver.common.by import By 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains

import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from driver_func.wait_size_elements_ko_kr import wait_size_elements_ko_kr
from driver_func.wait_size_elements_launch import wait_size_elements_launch
from driver_func.select_size_ko_kr import select_size_ko_kr
from driver_func.select_size_launch import select_size_launch
from driver_func.checking_item_uploaded import checking_item_uploaded
from driver_func.detect_progress_div import detect_progress_div
from driver_func.check_size_select_success import check_size_select_success

from time import sleep
import random

#1. 예약시간에 해당 링크로 이동
#2. 가끔씩 시간이 됐는데도 상품이 안올라왔을 때 최대 10번 동안 새로고침 (너무 많이 하게 되면 벤 먹기 때문에 10번으로 설정함 -> 추후에 변경 가능)
#3. 희망하는 시이즈로 ****한 번만**** 시도 (한 번 실패할 경우 무조건 랜덤으로만 선택 됨)
#4. 희망하는 사이즈가 없을 경우 랜덤으로 사이즈 선택
def goto_page(Chrome_driver, link, size, get_size_mode, retry_time):
    Chrome_driver.get(link)
    wait = WebDriverWait(Chrome_driver, 10, 0.1)
    # sleep(1)
    #==============================url에 "launch"가 없을 때 (스텔스 구매 페이지)==============================
    if(link.find('launch') == -1):
        #==========================아직 발매가 시작 안됐을 때 계속 새로고침==========================
        Chrome_driver = checking_item_uploaded(Chrome_driver, link)

        #==========================최대 100번 재시도==================
        for i in range(100):
            #=======================사이즈 element 들이 활성화 될 때까지 대기 후 size elements return==============================
            Chrome_driver, size_elements = wait_size_elements_ko_kr(Chrome_driver, link, retry_time)

            #======================= 사이즈 선택 ============================
            Chrome_driver = select_size_ko_kr(Chrome_driver, size_elements, size)

            #===========================우선 처리 중이라는 div가 끝날 때까지 기다리거나 popup 및 no-access 감지============================
            Chrome_driver, success = detect_progress_div(Chrome_driver)

            #===========================no-access로 갔는지 혹은 "지연 되고 있습니다" or "재고가 없습니다" 일 경우 다시 사이즈 선택으로 재시도============================
            if(success == False):
                print("retry select size")
                Chrome_driver.get(link)
                continue
            else:
                return Chrome_driver


    #==============================url에 "launch"가 있을 때 (스니커즈 구매 페이지) 위와 비슷, 설명 생략==============================
    else:
        #----------------------아직 발매가 시작 안됐을 때--------------------
        Chrome_driver = checking_item_uploaded(Chrome_driver, link)
        #----------------------아직 발매가 시작 안됐을 때--------------------
        action = ActionChains(Chrome_driver)
        for i in range(100):
            #=======================구매 버튼이 활성화 될 때까지 대기 후 size elements return==============================
            Chrome_driver, size_select_box, size_elements = wait_size_elements_launch(Chrome_driver, link, retry_time)

            #======================= 사이즈 선택 ============================
            Chrome_driver = select_size_launch(Chrome_driver, size_select_box, size_elements, size)

            #===========================우선 처리 중이라는 div가 끝날 때까지 기다리거나 popup 및 no-access 감지============================
            Chrome_driver, success = detect_progress_div(Chrome_driver)
            if(success == False):
                print("retry select size")
                Chrome_driver.get(link)
                continue
            else:
                return
        