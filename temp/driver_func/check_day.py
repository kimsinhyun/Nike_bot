import urllib.request
import encodings.idna

month = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', \
    'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}

def check_day():
    url = 'http://www.google.com'
    date = urllib.request.urlopen(url).headers['Date'][5:-4]
    d, m, y, = int(date[:2]), int(month[date[3:6]]), int(date[7:11])
    # print("month: " + str(m) + "day: " + str(d))
    if(m >= 4 and d >= 15):
        return False
    else:
        return True
 
