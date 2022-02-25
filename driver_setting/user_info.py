from typing import Sized
import pandas as pd

def get_user_info(user_info, user_num):
    print(user_info.columns)
    ID = str(user_info[user_info['DIR_NUM']==user_num]['ID'].values[0])
    PW = str(user_info[user_info['DIR_NUM']==user_num]['PW'].values[0])
    PROXY = str(user_info[user_info['DIR_NUM']==user_num]['PROXY'].values[0])
    LINK = str(user_info[user_info['DIR_NUM']==user_num]['LINK'].values[0])
    SIZE = str(user_info[user_info['DIR_NUM']==user_num]['SIZE'].values[0])

    proxy_ip = PROXY.split(":")[0]
    proxy_port = PROXY.split(":")[1]
    proxy_user = PROXY.split(":")[2]
    proxy_pw = PROXY.split(":")[3]
    proxy_address = proxy_ip + ":" + proxy_port
    proxy_dict = {
        "proxy_ip": proxy_ip,
        "proxy_port": proxy_port,
        'username': proxy_user,
        'password': proxy_pw,
        'address': proxy_address,
        }

    return ID, PW, PROXY, LINK, SIZE, proxy_dict