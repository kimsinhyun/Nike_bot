from concurrent import futures
import shutil, errno
import pandas as pd


user_info = pd.read_csv('./info.csv')
#몇 개의 계정을 돌릴건지 확인 -> 쓰레드 갯수 때문에 필요함
user_num = len(user_info)

def copyanything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno in (errno.ENOTDIR, errno.EINVAL):
            shutil.copy(src, dst)
        else: raise


for i in range (1,user_num):
    copyanything("0",str(i))