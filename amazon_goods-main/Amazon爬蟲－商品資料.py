# -*- coding: utf-8 -*-

# selenium，2022/9/17 將套件更新到4.4.3版本，因此寫法全部都更新過
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
from random import randint
import pandas as pd
import re
thing = '花襯衫'

# 自動下載ChromeDriver
service = ChromeService(executable_path=ChromeDriverManager().install())

# 關閉通知提醒
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
# driver = webdriver.Chrome()
# 開啟瀏覽器
driver = webdriver.Chrome(service=service, options=chrome_options)
time.sleep(5)   

theurl = []
for i in range(1):
    # 去到你想要的網頁
    driver.get("https://www.amazon.com/s?k="+ thing +"&page="+ str(i) +"&ref=sr_pg_2&&language=zh_TW")
    geturl = driver.find_elements(by=By.XPATH, value='//div/div/div/div/span/div/div/div[2]/div[1]/a')
    print("抓取")
    for j in geturl:
        print(j.get_attribute('href'))
        theurl.append(j.get_attribute('href'))
        
    time.sleep(5)
    

# 初始化一個空的列表來累積所有商品資料
all_products_data = []

for page in range(0, len(theurl)):
    brand = []
    title = []
    url = []
    price = []
    star = []
    starNum = []
    toosmall = []
    small = []
    goodsize = []
    big = []
    toobig = []
    size_options = []
    color_options = []
    description = []
    productDscrp = []
    global_range = []
    view_url = []
    print('第 '+ str(page) + ' 個商品')
    #儲存網址
    url.append(theurl[page])
    
    # 去到你想要的網頁
    driver.get(theurl[page])
    time.sleep(1)
    
    # 品牌名稱
    if len(driver.find_elements(by=By.ID, value='bylineInfo')) == 0 :
        brand.append('沒有牌子')
    else:
        brand.append(driver.find_element(by=By.ID, value='bylineInfo').text)
    
    # 商品名稱
    title.append(driver.find_element(by=By.ID, value='title').text) 
    
    # 商品定價
    if len(driver.find_elements(by=By.ID, value='corePriceDisplay_desktop_feature_div'))==0:
        getprice = driver.find_element(by=By.ID, value='corePrice_desktop').text
    else:
        getprice = driver.find_element(by=By.ID, value='corePriceDisplay_desktop_feature_div').text
    
    getprice = getprice.replace('US$','') # 先把「US$」拿掉
    if '有了交易' in getprice:
        getprice = getprice[getprice.find('有了交易')+6:]
        getprice = getprice.split('\n')[0]
    elif '\n定價:\n' in getprice:
        getprice = getprice[getprice.find('\n')+1:getprice.find('\n定價:\n')]
        getprice = getprice.replace('\n','.')
    else:
        
        getprice = getprice.replace('定價：','') # 把「定價」拿掉
        if ' -' in getprice: # 利用「 - 」來切割兩個數字
            getprice = re.findall(r'\d+\.\d+|\d+', getprice)
            # getprice = getprice.replace('\n','') # 把「US$」拿掉
            # cutlist = getprice.split(' -')
            # cutlist[1] = re.findall(r'\d+\.\d+|\d+', cutlist[1])
            # print(cutlist)
            getprice = (float(getprice[0]) + float(getprice[1]))/2 # 計算平均
        else:
            getprice = getprice.replace('\n','.')
    price.append(getprice)
    
    
    # 星星評分
    if len(driver.find_elements(by=By.ID, value='acrPopover'))==0:
        star.append('沒有星等')
    else:
        star.append(driver.find_element(by=By.ID, value='acrPopover').get_attribute("title").replace(' 顆星，最高 5 顆星',''))
    # 全球評分數量
    if len(driver.find_elements(by=By.ID, value='acrCustomerReviewText'))==0:
        starNum.append(0)
    else:
        getglobalNum = driver.find_element(by=By.ID, value='acrCustomerReviewText').text
        getglobalNum = getglobalNum.replace('等級','')
        getglobalNum = getglobalNum.replace(',','')
        starNum.append(getglobalNum)
    
    # 客戶回饋大小
    if len(driver.find_elements(by=By.ID, value='fitRecommendationsLinkRatingText')) == 0:
        toosmall.append(0)
        small.append(0)
        goodsize.append(0)
        big.append(0)
        toobig.append(0)
    else:
        time.sleep(5)
        driver.find_element(by=By.ID, value='fitRecommendationsLinkRatingText').click()
        time.sleep(5)
        getrequest = driver.find_elements(by=By.XPATH, value='//td[@class = "a-span1 a-nowrap"]')
        toosmall.append(getrequest[0].text)# 太小
        small.append(getrequest[1].text)# 有點小
        goodsize.append(getrequest[2].text)# 尺寸正確
        big.append(getrequest[3].text)# 有點大
        toobig.append(getrequest[4].text)# 太大
        # 關閉選項
        if len(driver.find_elements(by=By.XPATH, value='//button[@data-action = "a-popover-close"]')) != 0:
            driver.find_element(by=By.XPATH, value='//button[@data-action = "a-popover-close"]').click()
        time.sleep(1)
    
    # 大小選項
    driver.find_element(by=By.XPATH, value='//span[@data-csa-c-slot-id="dropdown_selected_size_name"]').click()
    time.sleep(1)
    containar = []
    for i in driver.find_elements(by=By.XPATH, value='//li[contains(@id, "size_name_")]'):
        if i.text != '選擇' and i.text != '':
            containar.append(i.text)
    size_options.append(containar)
    
    # 顏色選項
    containar = []
    for i in driver.find_elements(by=By.XPATH, value='//li[contains(@id, "color_name_")]'):
        getdata = i.get_attribute("title")
        containar.append(getdata.replace('請按下選擇 ','')) # 取代掉「請按下選擇」
    color_options.append(containar)
    
    # 商品描述
    if len(driver.find_elements(by=By.ID, value='productDescription')) != 0:
        productDscrp.append(driver.find_element(by=By.ID, value='productDescription').text)
    else:
        productDscrp.append('')
    # 產品詳細資訊
    description.append(driver.find_element(by=By.ID, value='detailBullets_feature_div').text)
    # 全球排名
    getdata = driver.find_element(by=By.XPATH, value='//div[@id = "detailBulletsWrapper_feature_div"]/ul').text
    getdata = getdata.replace('暢銷商品排名: ','')
    # getdata = getdata.replace('\n','')
    getdata = getdata.split('#')
    containar = {}
    for i in range(1,len(getdata)):
        rang = getdata[i].split(' 在 ')[0]
        item = getdata[i].split(' 在 ')[1]
        if ' (' in item:
            item = item.split(' (')[0]
        containar[item] = int(rang.replace(',',''))
    global_range.append(containar)
    
    # 留言網址
    if len(driver.find_elements(by=By.XPATH, value='//a[@data-hook = "see-all-reviews-link-foot"]'))== 0 :
        view_url.append('沒有留言')
    else:
        view_url.append(driver.find_element(by=By.XPATH, value='//a[@data-hook = "see-all-reviews-link-foot"]').get_attribute('href'))
    
    dic = {
        '品牌名稱': brand,
        '商品名稱': title,
        '網址': url,
        '商品定價': price,
        '星星評分': star,
        '全球評分數量': starNum,
        '大小選項': size_options,
        '顏色選項': color_options,
        '全球排名': global_range,
        '留言網址': view_url
    }
    
    # 將每個商品的資料追加到 all_products_data 列表中
    all_products_data.append(dic)

# 在所有頁面處理完畢後，將累積的資料寫入 CSV 檔案
pd.DataFrame(all_products_data).to_csv(
    './Amazon商品資料/累積_Amazon商品資料.csv',  # 檔案名稱
    encoding='utf-8-sig',  # 編碼
    index=False  # 是否保留index
)
