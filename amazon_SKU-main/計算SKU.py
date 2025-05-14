# -*- coding: utf-8 -*-

import pandas as pd
import re
from IPython.display import display
import numpy as np
#--- 匯入資料
# comment_data = pd.read_csv('../到第2個商品_Amazon留言資料.csv')
totalGoods=69
Total_file = []
comment_data = pd.DataFrame()
for i in range(0,totalGoods,1):
    Total_file.append(f'../第{i}個商品_Amazon留言資料.csv')

for file_path in (Total_file):
    df = pd.read_csv(file_path,encoding='utf8')
    comment_data = pd.concat([comment_data,df])

# 查看資料欄位
comment_data.columns

color =['黑', '白', '藍', '紅', '綠', '黃', '粉', '灰', '橘', '紫']

size = {'Small':'1', 'Medium':'2', 'Large':'3', 'X-Large':'4', 'XX-Large':'5', '3X-Large':'6'}

#--- 創造市場SKU統計表
counter=[]
for c in color:
    container=[]
    for s in size.keys():
        data = comment_data['SKU']
        container.append(len(comment_data['SKU']
                [comment_data['SKU'].str.contains(s) & comment_data['SKU'].str.contains(c)]))
    counter.append(container)
    
buyer = pd.DataFrame(counter)
buyer.columns = size
buyer.index = color
display(buyer)

