from time import sleep

def show_proxy_ip(driver, hold_time):
    driver.get("https://search.naver.com/search.naver?where=nexearch&sm=top_sug.pre&fbm=1&acr=1&acq=%EC%95%84%EC%9D%B4%ED%94%BC+%EC%A3%BC%EC%86%8C&qdt=0&ie=utf8&query=%EB%82%B4+%EC%95%84%EC%9D%B4%ED%94%BC+%EC%A3%BC%EC%86%8C+%ED%99%95%EC%9D%B8")
    sleep(1)
    driver.refresh()

    driver.get("https://www.nike.com/kr/ko_kr/")
    driver.maximize_window()
    sleep(hold_time)