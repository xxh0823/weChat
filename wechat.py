# 核心代码出自知行论坛帖子
import itchat
import numpy as np

import matplotlib.pyplot as plt


import pandas as pd

import jieba
import re
from wordcloud import WordCloud, ImageColorGenerator
import PIL.Image as Image

from numpy import *
#get_ipython().run_line_magic('matplotlib', 'notebook')

import pylab
#from IPython import get_ipython

#get_ipython().run_line_magic('matplotlib', 'notebook')


import time


# 调用itchat的登录方法获取登录二维码，实现扫码登录
itchat.login()


# 获取朋友列表
friends = itchat.get_friends(update=True)


# # 分析数据内容

# ## 数据为数组字典，每个字典包含联系人信息
# - 字典主要包含字段:
#     + UserName: 用户名
#     + NickName: 昵称
#     + HeadImgUrl: 头像图片链接
#     + RemarkName: 备注
#     + Province:省份
#     + City: 城市
#     + Sex：性别
#     + ……:等等

# # 绘制性别比例图



# 获取性别比例
def get_gender_ratio(friends):
    male = female = other = 0
    # 第0个是自己
    for i in friends[1:]:
        sex = i['Sex']
        if sex == 1:
            male += 1
        elif sex == 2:
            female += 1
        else:
            other += 1
    # 避免微信好友为0，除0异常
    persons = len(friends[1:]) if len(friends[1:]) >0 else 1
    return male/persons, female/persons, other/persons
male_ration, female_ration, other_ration = get_gender_ratio(friends)





x=[x for x in range(1,4)]

# 图表显示中文:
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


plt.figure()
plt.bar(x,height=[male_ration, female_ration, other_ration], color=['deepskyblue','deeppink','lightgreen'])
plt.xticks(x,['男','女','未知'])

plt.savefig('D:/1.jpg')

# # 分析地理分布
#

# ## pandas DataFrame建数据结构
# ### pandas DataFrame类似于表结构，更方便分析结构化数据

# In[6]:


# 生成pandas dataframe 方便数据分析
def get_Dataframe(friends):
    columns = ['UserName', 'Province', 'City', 'Sex', 'Signature','NickName']
    df = pd.DataFrame(columns=columns)
    for friend in friends[1:]:
        data = []
        for j in range(len(columns)):
            data.append(friend[columns[j]])
        df = df.append(pd.Series(data, index=columns), ignore_index=True)
    return df


df = get_Dataframe(friends)

# ## 绘制省份人口分布
# - 选择前20个省份进行绘制

# In[7]:


plt.figure()

pd.set_option('mpl_style', 'default')
plt.rc('font', **{'family': 'SimHei'})
df.groupby(['Province']).size().sort_values(ascending=False)[:20].plot(kind='bar')

plt.savefig('D:/2.jpg')
# ## 查看具体省份城市级别分布

# In[8]:


# 北京地区的人口分布
plt.figure()
df[df['Province'] == u'北京'].groupby(['City']).size().sort_values().plot(kind='bar')

plt.savefig('D:/3.jpg')
# ## 绘制个性签名云图

# ## 获取个性签名

# In[9]:


def get_signatures(df):
    siglist = []
    for index, friend in df.iterrows():
        signature=friend['Signature'].strip().replace('span','').replace('class','').replace('emoji','')
        rep = re.compile('1f\d+\w*|[<>/=]')
        signature = rep.sub('',signature)
        siglist.append(signature)
    text = "".join(siglist)
    return text
text = get_signatures(df)



def get_NickName(df):
    siglist = []
    for index, friend in df.iterrows():
        nickName=friend['NickName'].strip().replace('span','').replace('class','').replace('emoji','')
        rep = re.compile('1f\d+\w*|[<>/=]')
        nickName = rep.sub('',nickName)
        siglist.append(nickName)
    text = "".join(siglist)
    return text

nicknametext = get_NickName(df)
# ## 中文文本分词

# In[10]:


wordlist = jieba.cut(text, cut_all=True)
wordlist2 = jieba.cut(nicknametext, cut_all=True)


# In[11]:


word_space_split=' '.join(wordlist)
#word_space_split

word_space_split2=' '.join(wordlist2)
#word_space_split
word_space_split3=' '.join(nicknametext)

# ## 绘制词云图

# In[14]:


coloring = np.array(Image.open('./1.jpg'))
coloring2 = np.array(Image.open('./2.png'))

# In[15]:


my_wordcloud = WordCloud(background_color='white', max_words=2000, mask=coloring, max_font_size=120,random_state=
                        42,scale=2,font_path='C:/Windows/Fonts/simhei.ttf').generate(word_space_split)

my_wordcloud2 = WordCloud(background_color='white', max_words=5000, mask=coloring, max_font_size=50,random_state=
                        20,scale=1,font_path='C:/Windows/Fonts/simhei.ttf').generate(word_space_split2)

my_wordcloud3 = WordCloud(background_color='white', max_words=5000, mask=coloring, max_font_size=50,random_state=
                        20,scale=2,font_path='C:/Windows/Fonts/simhei.ttf').generate(nicknametext)


# In[16]:


image_colors = ImageColorGenerator(coloring)
image_colors2 = ImageColorGenerator(coloring)

# In[17]:


plt.figure(figsize=(16,9))
plt.imshow(my_wordcloud.recolor(color_func=image_colors))
plt.imshow(my_wordcloud)
plt.axis('off')
plt.savefig('D:/4.jpg')

plt.figure(figsize=(16,9))
plt.imshow(my_wordcloud2.recolor(color_func=image_colors2))
plt.imshow(my_wordcloud2)
plt.axis('off')
plt.savefig('D:/5.jpg',dpi=600)

plt.figure(figsize=(16,9))
plt.imshow(my_wordcloud3.recolor(color_func=image_colors))
plt.imshow(my_wordcloud3)
plt.axis('off')
plt.savefig('D:/6.jpg',dpi=600)
#plt.show()

#pylab.show()