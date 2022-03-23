def checking_item_uploaded(Chrome_driver, link):
    for i in range(30):
        print("checking item uploaded")
        if(Chrome_driver.page_source.find("사이즈 선택") != -1):
            print("item uploaded!")
            return Chrome_driver
        else:
            if(Chrome_driver.page_source.find("더 이상 확인 할 수 없는") != -1):
                Chrome_driver.get(link)
                print("item not uploaded yet")