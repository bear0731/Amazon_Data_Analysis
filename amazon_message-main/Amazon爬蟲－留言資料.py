# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
from random import randint
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

productData = pd.read_csv('到第1個_Amazon商品資料.csv', encoding = 'utf-8')
productData = productData[productData['留言網址'] != '沒有留言']

# 請求使用Header，可能需要替換cookie
head = {
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7',
        'cookie': 'session-id=136-0340723-9192226; session-id-time=2082787201l; i18n-prefs=USD; lc-main=zh_TW; ubid-main=134-3980769-3693765; sp-cdn="L5Z9:TW"; AMCV_7742037254C95E840A4C98A6%40AdobeOrg=1585540135%7CMCIDTS%7C19217%7CMCMID%7C35766644811422580582570690028170120544%7CMCAAMLH-1660894843%7C11%7CMCAAMB-1660894843%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1660297243s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.4.0; regStatus=pre-register; aws-target-data=%7B%22support%22%3A%221%22%7D; aws-target-visitor-id=1660290058678-241598.32_0; session-token=B/6zeP2udVs1ZsXHb3XMM7b1Q3fdOLgYEYeBXzq8szNmfY9PDKEbVp1YoDGdmp5ghrm1RATTEwtBzI6ba/JqwisTZUTCCPZ79TGQJ4UA2XxbcjaR57KnEInj9Ganl/ra73G5ALSE1JWW1ypsuHtgPld1GqLmYqEiZ1fXD40AlhpfLGjbNwpq6nXZVsfqC8fzIQ1FSoISXjkny3VkPKMRmZQQ760XK/Gj; csm-hit=tb:CGPN06Y24Z2V7X03ABND+s-CGPN06Y24Z2V7X03ABND|1660966628616&t:1660966628616&adb:adblk_no',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
        }

# 初始化 Selenium WebDriver
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

for data in range(len(productData)):
    print(f"正在爬取第{data}個商品的留言資料")
    theproduct = []
    theCommenturl = []
    who = []
    star = []
    thetime = []
    location = []
    sku = []
    comment = []
    helpful = []
    commentCount = 0
    # 決定要抓取的網址
    geturl = productData.iloc[data]['留言網址']
    print(f"留言網址: {geturl}")  # 顯示留言網址
    
    # 使用 Selenium 開啟留言網址
    driver.get(geturl)
    time.sleep(2)  # 等待頁面加載

    doit = True # 決定是否繼續進行留言爬蟲
    page = 0 # 爬到第幾頁
    while doit and commentCount<200:
        if page == 0: # 判斷是否為第一頁
            url = geturl
        else:
            url = geturl.split('/ref')[0] + '/ref=cm_cr_getr_d_paging_btm_next_'+ str(page) +'?ie=UTF8&reviewerType=all_reviews&pageNumber=' + str(page)
        
        #請求網站
        list_req = requests.get(url, headers= head)
        #將整個網站的程式碼爬下來
        soup = BeautifulSoup(list_req.content, "html.parser")
        getdata = soup.find_all('div', {'data-hook':'review'})
        if len(getdata) > 0: # 判斷是否有流言資料，沒有就直接將doit改成False，停止執行
            for i in getdata:
                theproduct.append(productData.iloc[data]['商品名稱']) # 儲存商品名稱
                theCommenturl.append(productData.iloc[data]['留言網址']) # 儲存留言網址
                
                who.append(i.find('span', {'class':'a-profile-name'}).text) # 儲存留言者
                
                # 處理星星
                getstart = i.find('span', {'class':'a-icon-alt'}).text
                getstart = getstart.replace(' 顆星，最高 5 顆星','') # 中文網頁
                getstart = getstart.replace(' out of 5 stars','') # 英文網頁
                star.append(float(getstart))
                
                # 處理購買時間、地點
                gettime = i.find('span', {'data-hook':'review-date'}).text
                if 'Reviewed' in gettime: # 判斷是否為英文網頁
                    # 將英文月份換成數字，這樣待會才能給datetime辨別
                    gettime = gettime.replace('January','1')
                    gettime = gettime.replace('February','2')
                    gettime = gettime.replace('March','3')
                    gettime = gettime.replace('April','4')
                    gettime = gettime.replace('May','5')
                    gettime = gettime.replace('June','6')
                    gettime = gettime.replace('July','7')
                    gettime = gettime.replace('August','8')
                    gettime = gettime.replace('September','9')
                    gettime = gettime.replace('October','10')
                    gettime = gettime.replace('November','11')
                    gettime = gettime.replace('December','12')
                    
                    gettime_list = gettime.split(' on ')
                    thetime.append(datetime.strptime(gettime_list[1], "%m %d, %Y")) # 儲存留言時間
                    location.append(gettime_list[0].replace('Reviewed in the ','')) # 儲存留言地點
                else:
                    if '於' in gettime: # 有時會出現不同呈現字串，範例:'在 2022年7月10日 於瑞典評論'
                        gettime = gettime.replace('在 ','')
                        gettime_list = gettime.split(' 於')
                    else:
                        gettime_list = gettime.split('在')
                    cuttime = gettime_list[0].replace(' ','')
                    thetime.append(datetime.strptime(cuttime, "%Y年%m月%d日")) # 儲存留言時間
                    location.append(gettime_list[1].replace('評論','')) # 儲存留言地點
                
                comment.append(i.find('span', {'data-hook':'review-body'}).text) # 儲存留言內容
                
                # 處理覺得留言有用人數
                gethelpful = i.findAll('span', {'data-hook':'helpful-vote-statement'}) # 儲存覺得留言有用人數
                if len(gethelpful) != 0: # 判斷是否有資料
                    
                    gethelpful = gethelpful[0].text
                    gethelpful = gethelpful.replace(',','') # 把千分位的「,」拿掉
                    gethelpful = gethelpful.replace(' 個人覺得有用','') # 中文網頁
                    gethelpful = gethelpful.replace(' people found this helpful','') # 英文網頁
                    if '一人覺得有用' == gethelpful or 'One person found this helpful' == gethelpful: # 判斷是否只有一人
                        helpful.append(1)
                    else:
                        helpful.append(int(gethelpful))
                else:
                    helpful.append(0)
                
                
                # 處理購買顏色、尺寸
                getsku = i.find_all('a', {'data-hook':'format-strip'})
                if len(getsku) == 1: # 判斷是否有資料
                    sku.append(getsku[0].text)
                else:
                    sku.append(None)
        else:
            doit = False
        print('累計資料數量： '+ str(len(who)))
        page = page + 1
        # time.sleep(1) # 睡覺覺
        # time.sleep(randint( 5, 20)) # 睡覺覺
        dic = {
        '商品名稱' : theproduct,
        '留言網址' : theCommenturl,
        '留言者' : who,
        '星等' : star,
        '留言時間' : thetime,
        '留言地點' : location,
        'SKU' : sku,
        '留言內容' : comment,
        '覺得留言有用人數' : helpful,
        }
    
        pd.DataFrame(dic).to_csv('Amazon留言資料.csv', 
                            encoding = 'utf-8-sig', 
                            index=False)
        

        pd.DataFrame(dic).to_csv('第'+str(data)+'個商品_Amazon留言資料.csv', 
                                 encoding = 'utf-8-sig', 
                                 index=False)
    print(productData.iloc[data]['商品名稱']+ ' 執行完畢')

# 完成後關閉瀏覽器
driver.quit()

