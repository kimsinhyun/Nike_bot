import os

#각 사용자마다 각각의 쿠키 파일 연결
def get_cookie_driver_exe(chrome_ver, user_num):
    #크롬 쿠키
    chrome_cookie_path = (str(os.path.abspath(os.getcwd()))).replace('\\driver_setting','') + "\\cookies\\" +str(user_num) + '\Chrome_cookie'
    chrome_cookie_path = chrome_cookie_path.replace('\\first_setting','')
    chrome_cookie_path = chrome_cookie_path.replace('\\driver_setting','')
    #크롬 실행파일
    chrome_exe_path = "C:\Program Files\Google\Chrome\Application\chrome.exe"
    #크롬 드라이버
    chrome_driver_path = str(os.path.abspath(os.getcwd())) + '\\' + str(chrome_ver) + '\\chromedriver.exe'
    chrome_driver_path = chrome_driver_path.replace('\\first_setting','')
    chrome_driver_path = chrome_driver_path.replace('\\driver_setting','')
    print(chrome_driver_path)
    return chrome_cookie_path, chrome_exe_path, chrome_driver_path

get_cookie_driver_exe(98, 0)