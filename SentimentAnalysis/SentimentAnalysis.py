import numpy as np
import pandas as pd
from textblob import TextBlob
import re

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
# import nltk

# import ssl

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

# # nltk.download('vader_lexicon')
# from nltk.sentiment import SentimentIntensityAnalyzer

# # nltk.downloader.download('vader_lexicon')
# sia = SentimentIntensityAnalyzer()
# for text in CommentOfBrand.values():
#     score = sia.polarity_scores(str(text))
#     print(score)
   
for text in CommentOfBrand.values():
    blob = TextBlob(str(text))
    print(blob.sentiment)


