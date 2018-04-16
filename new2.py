import operator
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import Series,DataFrame

db='Play.csv'
#读取csv文件，生成data frame
data=pd.read_csv(db,low_memory=False)
#print(data.info())198900*43
#查看前十条数据内容
print(data.iloc[:10])
# 定义两类数据：标称型和数值型
frame1=DataFrame(data,columns=['Date','GameID','Drive','qtr','down','time',
'TimeUnder','SideofField','GoalToGo','FirstDown','posteam','DefensiveTeam','desc','PlayAttempted','sp','Touchdown','ExPointResult'
,'TwoPointConv','DefTwoPoint','Safety',  'Onsidekick','PuntResult',
'PlayType', 'Passer','Passer_ID','PassAttempt',
'PassOutcome','PassLength','QBHit','PassLocation','InterceptionThrown','Interceptor','Rusher','Rusher_ID','RushAttempt',
'RunLocation','RunGap','Receiver','Receiver_ID','Reception','ReturnResult','Returner','BlockingPlayer','Tackler1','Tackler2',
'FieldGoalResult','FieldGoalDistance','Fumble','RecFumbTeam','RecFumbPlayer','Sack','Challenge.Replay','ChalReplayResult',
                               'Accepted.Penalty','PenalizedTeam','PenaltyType','PenalizedPlayer	',
'PosTeamScore','DefTeamScore','ScoreDiff','AbsScoreDiff','HomeTeam','AwayTeam','Timeout_Indicator',
'Timeout_Team','posteam_timeouts_pre','HomeTimeouts_Remaining_Pre','AwayTimeouts_Remaining_Pre',
'HomeTimeouts_Remaining_Post','AwayTimeouts_Remaining_Post','ExPoint_Prob',
'TwoPoint_Prob','Season'])

frame2=DataFrame(data,columns=['TimeSecs','PlayTimeDiff','yrdln','yrdline100','ydstogo','ydsnet',
                               'Yards.Gained','AirYards','YardsAfterCatch','Penalty.Yards','No_Score_Prob',
'Opp_Field_Goal_Prob','Opp_Safety_Prob','Opp_Touchdown_Prob','Field_Goal_Prob','Safety_Prob','Touchdown_Prob',
                               'ExpPts','EPA','airEPA','yacEPA','Home_WP_pre','Away_WP_pre','Home_WP_post','Away_WP_post',
'Win_Prob','WPA','airWPA','yacWPA'])

# **Step 1. 数据摘要**
#
#对标称属性，给出每个可能取值的频数，value_counts()
for i in range(35):
   print('频数为:\n',frame1.iloc[:,[i]].apply(pd.value_counts),'\n')

# 数值属性，给出最大、最小、均值、中位数、四分位数及缺失值的个数。
#用describe（）函数获取最大、最小、均值、中位数、四分位数
statistics=frame2.describe()
#统计数值属性的缺失值数量
statistics.loc['null']=data.shape[0]-statistics.loc['count']
print(statistics)

# **Step 2. 数据可视化 **
#
# - 针对数值属性：
#针对数值属性，绘制直方图，用qq图检验其分布是否为正态分布。绘制盒图，对离群值进行识别

# 直方图
fig = plt.figure(figsize = (20,11))
i = 1
for item in frame2:
    ax = fig.add_subplot(8, 5, i)
    data[item].plot(kind = 'hist', title = item, ax = ax)
    i += 1
plt.subplots_adjust(wspace = 0.3, hspace = 0.3)
fig.savefig('./image2/histogram.png')
print('histogram saved at ./image2/histogram.png')

# - 绘制盒图，对离群值进行识别。
# 盒图
fig = plt.figure(figsize = (20,12))
i = 1
for item in frame2:
    ax = fig.add_subplot(8, 5, i)
    data[item].plot(kind = 'box')
    i += 1
fig.savefig('./image2/boxplot.png')
print('boxplot saved at ./image2/boxplot.png')

# Step3 处理缺失值
#

# 将缺失部分剔除
# 绘制可视化图
nan_list = pd.isnull(data).any(1).nonzero()[0]
DataTable_filtrated = data;
fig = plt.figure(figsize=(20, 15))
n = 6
# 对数值属性，绘制直方图
for i in frame2:
    ax = fig.add_subplot(8, 5, n)

    DataTable_filtrated[i] = DataTable_filtrated[i].dropna()  # 删除
    ax.set_title(i)
    data[i].plot(ax=ax, alpha=0.5, kind='hist', label='origin', legend=True)
    DataTable_filtrated[i].plot(ax=ax, alpha=0.5, kind='hist', label='filtrated', legend=True)
    # pyplot.show()
    ax.axvline(data[i].mean(), color='r')
    ax.axvline(DataTable_filtrated[i].mean(), color='b')
    n += 1
plt.subplots_adjust(wspace=0.3, hspace=0.3)
# 保存图像和处理后数据
fig.savefig('./image2/missing_data_delete.png')
print('filted_missing_data1 saved at ./image2/missing_data_delete.png')

# 用最高频率值来填补缺失值
# 绘制可视化图
DataTable_filtrated = data;
fig = plt.figure(figsize=(20, 15))
n = 6
# 对数值属性，绘制直方图
for i in frame2:
    ax = fig.add_subplot(8, 5, n)
    MostFrequentElement = data[i].value_counts().idxmax();

    DataTable_filtrated[i] = DataTable_filtrated[i].fillna(value=MostFrequentElement);  # 众数填补缺失值
    ax.set_title(i)
    data[i].plot(ax=ax, alpha=0.5, kind='hist', label='origin', legend=True)
    DataTable_filtrated[i].plot(ax=ax, alpha=0.5, kind='hist', label='filtrated', legend=True)
    # pyplot.show()
    ax.axvline(data[i].mean(), color='r')
    ax.axvline(DataTable_filtrated[i].mean(), color='b')
    n += 1
plt.subplots_adjust(wspace=0.3, hspace=0.3)
# 保存图像和处理后数据
fig.savefig('./image2/missing_data_most.png')
print('filted_missing_data1 saved at ./image2/missing_data_most.png')

# 通过属性的相关关系来填补缺失值，插值法
# 绘制可视化图
DataTable_filtrated = data;
fig = plt.figure(figsize=(20, 15))
n = 6
# 对数值属性，绘制直方图
for i in frame2:
    ax = fig.add_subplot(8, 5, n)

    DataTable_filtrated[i].interpolate(inplace=True)  # 插值
    ax.set_title(i)
    data[i].plot(ax=ax, alpha=0.5, kind='hist', label='origin', legend=True)
    DataTable_filtrated[i].plot(ax=ax, alpha=0.5, kind='hist', label='filtrated', legend=True)
    # pyplot.show()
    ax.axvline(data[i].mean(), color='r')
    ax.axvline(DataTable_filtrated[i].mean(), color='b')
    n += 1
plt.subplots_adjust(wspace=0.3, hspace=0.3)
# 保存图像和处理后数据
fig.savefig('./image2/missing_data_corelation.png')
print('filted_missing_data1 saved at ./image2/missing_data_corelation.png')


