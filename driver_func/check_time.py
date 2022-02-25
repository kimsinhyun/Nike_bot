import datetime
import urllib.request

#네이버 서버 시간을 기준으로 타이머 설정
def check_time(hour, minute):
    url = 'https://www.naver.com/'
    date = urllib.request.urlopen(url).headers['Date'][5:-4]
    nav_hour, nav_min, nav_sec =  date[12:14], date[15:17], date[18:]
    nav_hour = str((int(nav_hour)+ 9))

    nav_hour = int(nav_hour)
    nav_min = int(nav_min)

    hour = int(hour)
    minute = int(minute)

    # print(nav_hour, ":", nav_min)
    if (nav_hour == hour ) and (nav_min == minute):
        return True
    else: 
        return False