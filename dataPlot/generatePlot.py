import pandas as pd
import re
import numpy as np
from textblob import TextBlob
import matplotlib.pyplot as plt

numberOfGoods = 69
datas = pd.read_csv(f'到第{numberOfGoods}個商品_Amazon商品資料.csv',encoding='utf8')
class brand :
    totoalCommeents = 0
    numOfGoods = 0
    totalStarts = 0.0
    avgStarts = 0.0
    maxPrice = 0.0
    minPrice = 0.0
    avgPrice = 0.0
    totalPrice = 0.0
    avgComments = 0
    name = ''
    def calculateAvg(self):
        self.calculateAvgPrice()
        self.calculateAvgComment()
        self.calculateAvgStarts()
    def calculateAvgStarts(self):
        self.avgStarts = self.totalStarts / self.numOfGoods

    def calculateAvgPrice(self):
        self.avgPrice = self.totalPrice / self.numOfGoods

    def calculateAvgComment(self):
        self.avgComments = self.totoalCommeents / self.numOfGoods
allBrand = {}
allBrandName =[]
for i in range(len(datas['品牌名稱'])):

    brandName = re.findall('\s(.*)\s',datas['品牌名稱'][i])
    if len(brandName) != 0:
        brandName = re.findall('\s(.*)\s',datas['品牌名稱'][i])[0] 
    else:
        continue
    comment = int(re.findall('(.*)\s',datas['全球評分數量'][i])[0])
    
    Price = float(re.findall('\d+\.\d+',datas['商品定價'][i])[0])
    starts = datas['星星評分'][i]
    if brandName not in allBrandName:
        newBrand = brand()
        newBrand.name = brandName
        newBrand.numOfGoods += 1
        newBrand.totoalCommeents += comment
        newBrand.totalPrice += Price
        newBrand.maxPrice = Price
        newBrand.minPrice = Price
        newBrand.totalStarts += starts
        newBrand.calculateAvg()
        allBrand[brandName] = newBrand
        allBrandName.append(brandName)
    else:
        allBrand[brandName].totoalCommeents += comment
        allBrand[brandName].numOfGoods += 1
        allBrand[brandName].totoalCommeents += comment

        allBrand[brandName].totalPrice += Price
        # print(f'min:{allBrand[brandName].minPrice},avg:{allBrand[brandName].avgPrice},max:{allBrand[brandName].maxPrice},price:{Price}')
        if allBrand[brandName].maxPrice<Price:allBrand[brandName].maxPrice = Price
        if allBrand[brandName].minPrice>Price:allBrand[brandName].minPrice = Price
        allBrand[brandName].totalStarts += starts
        allBrand[brandName].calculateAvg()
for v in allBrand.values():
    print(v.totoalCommeents)
MinComments = 0
MinCommentsBrand = 0
topTenCommentsOfBrands = {}
i = 0
for v in allBrand.values():
    if i==0:
        MinComments = v.totoalCommeents
        MinCommentsBrand = v.name
    if i<10:
        topTenCommentsOfBrands[v.name] = v.totoalCommeents
        if MinComments<v.totoalCommeents:
            topTenCommentsOfBrands ={k: v for k, v in sorted(topTenCommentsOfBrands.items(), key=lambda item: item[1],reverse=True)}
            MinComments = list(topTenCommentsOfBrands.values())[-1]
            MinCommentsBrand = list(topTenCommentsOfBrands.keys())[-1]
        i += 1
        continue
    if v.totoalCommeents > MinComments:
        topTenCommentsOfBrands.pop(MinCommentsBrand,None)
        topTenCommentsOfBrands[v.name] = v.totoalCommeents
        topTenCommentsOfBrands ={k: v for k, v in sorted(topTenCommentsOfBrands.items(), key=lambda item: item[1],reverse=True)}
        MinComments = list(topTenCommentsOfBrands.values())[-1]
        MinCommentsBrand = list(topTenCommentsOfBrands.keys())[-1]
    i += 1
topTenCommentsOfBrands = {k: v for k, v in sorted(topTenCommentsOfBrands.items(), key=lambda item: item[1],reverse=True)}
print(topTenCommentsOfBrands)
# 定義資料
commentOfOtherBrand = 0
j=0
for i in list(allBrand.values()):
    if j>4:
        commentOfOtherBrand += int(i.totoalCommeents)
    j += 1
sizes =list(topTenCommentsOfBrands.values())[:5]+[(commentOfOtherBrand)]
labels = list(topTenCommentsOfBrands.keys())[:5]+['Other']
# 繪製圓餅圖
plt.pie(sizes, labels=labels, autopct='%1.1f%%')

# 添加圖表標題
plt.title('market_Size')
plt.savefig('market_size_pie.png', bbox_inches='tight')
# 顯示圖表
plt.show()
goods = []
for i in topTenCommentsOfBrands.keys():
    goods.append(allBrand[i].numOfGoods)
x = goods
y = list(topTenCommentsOfBrands.keys())
mean_value = np.mean(x)

plt.axhline(y=mean_value, color='r', linestyle='--', label='Mean')

plt.bar(y,x)

plt.legend()  # 添加圖例
plt.tight_layout()  # 自動調整子圖的間距，以防止標籤重疊
plt.title('Number_Of_Goods')
plt.xlabel('Brand')
plt.ylabel('Goods')
plt.xticks(rotation=45)
plt.savefig('Total_Goods_chart.png', bbox_inches='tight')
#pic1
plt.show()

allStarts = []
for i in topTenCommentsOfBrands.keys():
    allStarts.append(allBrand[i].avgStarts)
x = allStarts
y = list(topTenCommentsOfBrands.keys())
mean_value = np.mean(x)

plt.axhline(y=mean_value, color='r', linestyle='--', label='Mean')

plt.bar(y,x)

plt.legend()  # 添加圖例
plt.tight_layout()  # 自動調整子圖的間距，以防止標籤重疊
plt.title('Starts_Rank')
plt.xlabel('Brand')
plt.ylabel('Starts')
plt.xticks(rotation=45)
plt.savefig('comments_start_chart.png', bbox_inches='tight')
#pic1
plt.show()
# print(topTenCommentsOfBrands.values())
avgComments = []
totalComments = []
for v in topTenCommentsOfBrands.keys():
    avgComments.append(allBrand[v].avgComments)
    totalComments.append(topTenCommentsOfBrands[v])
    

# y = list(topTenCommentsOfBrands.keys())
mean_value = np.mean(avgComments)
ax = plt.subplot()
plt.axhline(y=mean_value, color='r', linestyle='--', label='MeanOfAvg')
bars1 = ax.bar(topTenCommentsOfBrands.keys(), totalComments, 0.35,label='Total_Comments')
bars2 = ax.bar(topTenCommentsOfBrands.keys(), avgComments, 0.35, label='Avg_Comments')


# 添加標籤、標題等
ax.set_xlabel('Brand')
ax.set_ylabel('Total_Comments')
ax.set_title('Comments_Rank')
plt.xticks(rotation=45)

ax.legend()
# plt.bar(y,x)
# plt.legend()  # 添加圖例
# plt.tight_layout()  # 自動調整子圖的間距，以防止標籤重疊
# plt.title('Comments_Rank')
# plt.xlabel('Brand')
# plt.ylabel('Comments')
# plt.xticks(rotation=45)
plt.savefig('total_comments_chart.png', bbox_inches='tight')
#pic2
plt.show()


numberOfGoods = 69

goodDatas = pd.read_csv(f'到第{numberOfGoods}個商品_Amazon商品資料.csv',encoding='utf8')
Total_file = []
comment_data = pd.DataFrame()

for i in range(0,numberOfGoods,1):
    Total_file.append(f'./第{i}個商品_Amazon留言資料.csv')

i = 0
CommentOfBrand = {str:str}
for file_path in (Total_file):
    comment_data = pd.read_csv(file_path,encoding='utf8')
    brandName = re.findall('\s(.*)\s',goodDatas['品牌名稱'][i])
    if len(brandName) != 0:
        brandName = brandName[0]
        for comment in comment_data['留言內容']:
            if type(comment) == float:
                continue
            if brandName not in CommentOfBrand: 
                CommentOfBrand[brandName] = comment
            else:
                CommentOfBrand[brandName] += comment
    i += 1

sentiment = []
for i in list(topTenCommentsOfBrands.keys()):
    # for text in CommentOfBrand.values():
    blob = TextBlob(str(CommentOfBrand[i]))
    sentiment.append(blob.sentiment[0])

maxSentiment = np.max(sentiment)
time = 1.0/maxSentiment
for i in range(len(sentiment)):
    sentiment[i] *=time

x = list(sentiment)
y = list(topTenCommentsOfBrands.keys())
mean_value = np.mean(x[:10])
plt.axhline(y=mean_value, color='r', linestyle='--', label='Mean')

plt.bar(y,x)

plt.legend()  # 添加圖例
plt.tight_layout()  # 自動調整子圖的間距，以防止標籤重疊
plt.title('Sentiment_Rank')
plt.xlabel('Brand')
plt.ylabel('sentiment')
plt.xticks(rotation=45)
plt.savefig('sentiment_bar_chart.png', bbox_inches='tight')
# pic1
plt.show()
ax = plt.subplot()
bar_width = 0.35

minPrice = []
maxPrice = []
avgPrice = []
for i in topTenCommentsOfBrands.keys():
    print(f'min:{allBrand[i].minPrice},avg:{allBrand[i].avgPrice},max:{allBrand[i].maxPrice}')
    minPrice.append(allBrand[i].minPrice)
    maxPrice.append(allBrand[i].maxPrice)
    avgPrice.append(allBrand[i].avgPrice)

bars3 = ax.bar(topTenCommentsOfBrands.keys(), maxPrice, bar_width, label='maxPrice')
bars2 = ax.bar(topTenCommentsOfBrands.keys(), avgPrice, bar_width, label='avgPrice')
bars1 = ax.bar(topTenCommentsOfBrands.keys(), minPrice, bar_width, label='minPrice')
mean_value = np.mean(avgPrice)
ax.axhline(y=mean_value, color='r', linestyle='--', label='MeanOfAvg')

# 添加標籤、標題等
ax.set_xlabel('Brand')
ax.set_ylabel('Dollers')
ax.set_title('Price range')
plt.xticks(rotation=45)

ax.legend()
plt.savefig('price_range_chart.png', bbox_inches='tight')
# 顯示圖表
plt.show()

