import os 
import zipfile
import pandas as pd
from concurrent import futures

# PROXY_HOST = '45.90.202.170'  # rotating proxy or host
# PROXY_PORT = 54328 # port
# PROXY_USER = 'run' # username
# PROXY_PASS = '30kPl0BD' # password

def make_proxy_config(user_info,user_num):
    PROXY = str(user_info[user_info['DIR_NUM']==user_num]['PROXY'].values[0])
    PROXY_HOST = PROXY.split(":")[0]
    PROXY_PORT = PROXY.split(":")[1]
    PROXY_USER = PROXY.split(":")[2]
    PROXY_PASS = PROXY.split(":")[3]
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

    pluginfile = '../proxy_config/' + str(user_num) + 'th_proxy_auth_plugin.zip'

    if not os.path.exists("../proxy_config/"):
        try:
            os.makedirs("../proxy_config/")
        except: 
            pass
    with zipfile.ZipFile(pluginfile, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)
        

def main():
    with futures.ThreadPoolExecutor(max_workers=20) as executor: 
        user_info = pd.read_csv('../info.csv')
        user_num = len(user_info)
        future_test_results = [ executor.submit(make_proxy_config, user_info,i) for i in range(user_num) ] # running same test 6 times, using test number as url
        # future_test_results = [ executor.submit(make_proxy_config, 1)] # running same test 6 times, using test number as url
        for future_test_result in future_test_results:
            try:
                test_result = future_test_result.result(timeout=None)# can use `timeout` to wait max seconds for each thread               
            except: # can give a exception in some thread, but
                print('thread generated an exception: {:0}'.format(Exception))

if __name__ == "__main__":
    main()