from time import sleep

def show_proxy_ip(driver, hold_time):
    driver.get("https://www.findip.kr/")
    sleep(1)

    driver.maximize_window()
    sleep(hold_time)