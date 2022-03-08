from time import sleep

def show_proxy_ip(driver, hold_time,check_ip):
    if((check_ip == 'y') or (check_ip == 'yes')):
        driver.get("https://www.findip.kr/")
        sleep(hold_time)
    else:
        return