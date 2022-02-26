from concurrent import futures
import shutil, errno
import pandas as pd


user_info = pd.read_csv('../info.csv')
#몇 개의 계정을 돌릴건지 확인 -> 쓰레드 갯수 때문에 필요함
user_num = len(user_info)

def copyanything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno in (errno.ENOTDIR, errno.EINVAL):
            shutil.copy(src, dst)
        else: raise

# for i in range(user_num):
#     copyanything("../cookie_with_SwitchOmega","../cookies/" + str(user_num))

def do_copy(user_num):
    try:
        copyanything("../cookie_with_SwitchOmega","../cookies/" + str(user_num))
    except:
        print(user_num,"번째 쿠키는 이미 존재합니다")

with futures.ThreadPoolExecutor(max_workers=20) as executor: 
    future_test_results = [ executor.submit(do_copy, i) for i in range(user_num) ] # running same test 6 times, using test number as url
    for future_test_result in future_test_results: 
        try:        
            test_result = future_test_result.result(timeout=None) # can use `timeout` to wait max seconds for each thread               
        except: # can give a exception in some thread, but 
            print('thread generated an exception: {:0}'.format(Exception))