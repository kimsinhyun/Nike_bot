def checking_item_uploaded(Chrome_driver, link):
    for i in range(30):
        print("checking item uploaded")
        if(Chrome_driver.page_source.find("사이즈 선택") != -1):
            print("item uploaded!")
            return Chrome_driver
        elif(Chrome_driver.page_source.find("품절") != -1):
            print("품절되었습니다.")
            return Chrome_driver
            
        else:
            if(Chrome_driver.page_source.find("더 이상 확인 할 수 없는") != -1):
                Chrome_driver.get(link)
                print("item not uploaded yet")
            elif(Chrome_driver.page_source.find("Coming Soon") != -1):
                print("item not uploaded yet")
                Chrome_driver.get(link)