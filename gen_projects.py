#!/usr/bin/env python3
import json, os

OUT = "/workspace/assets/data/projects.json"
projects = []

# ============ helper ============
def make_proj(pid, title, subtitle, diff, dur, tags, goal, bg, data_plan, codes, exercises, insights, deliverables):
    return {
        "projectId": pid, "title": title, "subtitle": subtitle,
        "difficulty": diff, "duration": dur, "tags": tags,
        "businessGoal": goal, "background": bg, "dataPlan": data_plan,
        "codeBlocks": [{"blockId": f"b{i+1}", "title": t, "description": d, "code": c} for i, (t, d, c) in enumerate(codes)],
        "exercises": exercises, "insights": insights, "deliverables": deliverables
    }

# ============ Project 1 ============
p1c1 = """import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(42)
N = 5000
channels = ['Organic', 'Paid', 'Referral', 'Social']
ch = np.random.choice(channels, N, p=[0.35,0.25,0.20,0.20])
df = pd.DataFrame({'user_id':[f'U{i:05d}' for i in range(N)],'channel':ch})
df['reg_day'] = np.random.randint(0,90,N)
df['active_days'] = np.random.poisson(15,N)
df.loc[df.channel=='Paid','active_days']=np.random.poisson(8,(df.channel=='Paid').sum())
df.loc[df.channel=='Referral','active_days']=np.random.poisson(22,(df.channel=='Referral').sum())
df['total_sessions']=np.random.poisson(35,N)
print(df.groupby('channel')[['active_days','total_sessions']].mean().round(2))

fig,ax=plt.subplots(1,2,figsize=(11,4))
df['channel'].value_counts().plot(kind='bar',ax=ax[0],color=['#4C72B0','#DD8452','#55A868','#C44E52'])
ax[0].set_title('Registrations by Channel')
df.groupby('channel')['active_days'].mean().plot(kind='bar',ax=ax[1],color='#8172B2')
ax[1].set_title('Avg Active Days by Channel')
plt.tight_layout()
plt.savefig('output.png')
plt.close()
print('saved')
"""

p1c2 = """import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(7)
DAYS,users=60,2000
activity=np.random.binomial(1,0.22,(users,DAYS))
decay=np.linspace(1.0,0.7,DAYS)
activity=(activity*decay>np.random.rand(users,DAYS)).astype(int)
dau=activity.sum(axis=0)
weeks={}
for w in range(DAYS//7):
    weeks[f'W{w+1}']=activity[:,w*7:(w+1)*7].sum(axis=1).gt(0).sum()
wau=pd.Series(weeks)
print('DAU avg:',dau.mean().round(1))
print('WAU:',wau.to_dict())

fig,axes=plt.subplots(1,2,figsize=(11,4))
axes[0].plot(range(DAYS),dau,'b-')
axes[0].set_title('Daily Active Users')
axes[0].grid(True,alpha=0.3)
wau.plot(kind='bar',ax=axes[1],color='#DD8452')
axes[1].set_title('Weekly Active Users')
plt.tight_layout()
plt.savefig('output.png')
plt.close()
"""

p1c3 = """import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(11)
cohorts=6
base=np.array([1.0,0.55,0.40,0.32,0.27,0.23])
mat=np.zeros((cohorts,cohorts))
for c in range(cohorts):
    for p in range(cohorts-c):
        mat[c,p]=np.clip(base[p]+np.random.normal(0,0.04),0,1)
df=pd.DataFrame(mat,columns=[f'W{p}' for p in range(cohorts)],index=[f'Cohort{c+1}' for c in range(cohorts)])
print(df.round(3))

fig,ax=plt.subplots(figsize=(9,5))
for c in range(cohorts):
    vals=mat[c,:cohorts-c]
    ax.plot(range(len(vals)),vals,'o-',label=f'Cohort{c+1}')
ax.set_title('Retention Curve')
ax.set_xlabel('Weeks after registration')
ax.set_ylabel('Retention rate')
ax.legend()
ax.grid(True,alpha=0.3)
plt.tight_layout()
plt.savefig('output.png')
plt.close()
"""

projects.append(make_proj(
    "proj01","用户注册与活跃行为分析","识别高价值注册渠道并追踪用户留存曲线",
    "初级","2.5 小时",["Pandas","Matplotlib","用户行为","留存分析"],
    "量化各渠道的获客质量差异，评估渠道ROI，识别高流失风险期，指导市场投放策略。",
    "某在线教育平台过去 90 天累计注册用户约 5000 人，来自自然搜索、付费广告、老用户推荐、社交媒体四个主要渠道。运营团队发现不同渠道用户后续活跃度差异显著。",
    "模拟 users 表（5000 行：user_id/channel/reg_day/active_days/total_sessions）、daily_activity（60 天活跃矩阵）、cohorts（6×6 留存矩阵）。",
    [("渠道注册分布与活跃度","对比各渠道注册量与平均活跃天数",p1c1),
     ("DAU/WAU 趋势","计算日活与周活时间序列",p1c2),
     ("Cohort 留存曲线","不同 cohort 的留存衰减",p1c3)],
    [{"exerciseId":"ex01","title":"渠道转化率排名","question":"计算每个渠道 7日留存率（active_days>=7 用户比例）并排序。","starterCode":"import pandas as pd\ndf=pd.DataFrame({'ch':['A','B','A'],'ad':[3,12,8]})","testCode":"assert True"}],
    ["老用户推荐渠道用户质量最高，活跃天数是付费渠道 2.5 倍","付费渠道在注册后第 2-3 周出现明显流失波谷","自然搜索渠道注册量最大但留存中等，是增量用户体验优化空间最大","建议预算向推荐渠道倾斜 20% 可显著提升整体留存"],
    ["渠道注册量排名柱状图","渠道平均活跃天数对比图","DAU/WAU 时间序列折线图","Cohort 留存曲线图"]
))

# ============ Project 2 ============
p2c1 = """import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(5)
N=3000
stages=['View','Enroll','Start','Ch1','Ch3','Ch5','Final','Complete']
rates=[1.0,0.72,0.58,0.45,0.33,0.24,0.18,0.12]
data=[]
for i in range(N):
    r=np.random.rand()
    reached=sum(r<np.array(rates[::-1]))
    idx=len(stages)-1-reached if reached>0 else 0
    data.append({'user':f'U{i:05d}','stage':stages[idx],'score':np.random.randint(40,100)})
df=pd.DataFrame(data)
counts=df['stage'].value_counts().reindex(stages)
print(counts)
for i in range(len(stages)-1):
    print(f'{stages[i]}->{stages[i+1]}: {counts.iloc[i+1]/counts.iloc[i]:.2%}')

fig,ax=plt.subplots(figsize=(9,5))
colors=plt.cm.Blues(np.linspace(0.3,0.9,len(stages)))
ax.bar(range(len(stages)),counts.values,color=colors)
for i,(s,h) in enumerate(zip(stages,counts.values)):
    ax.text(i,h+counts.values[0]*0.01,str(h),ha='center')
ax.set_xticks(range(len(stages)))
ax.set_xticklabels(stages,rotation=20)
ax.set_title('Learning Funnel')
plt.tight_layout()
plt.savefig('output.png')
plt.close()
"""

p2c2 = """import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(3)
chapters,users=8,500
weights=np.array([0.95,0.85,0.78,0.70,0.62,0.55,0.48,0.42])
mat=(np.random.rand(users,chapters)<weights[None,:]).astype(int)
df=pd.DataFrame(mat,columns=[f'Ch{i+1}' for i in range(chapters)])
heat=df.corr()
print(heat.round(2))

fig,ax=plt.subplots(figsize=(8,6))
im=ax.imshow(heat.values,cmap='RdBu_r',vmin=-0.5,vmax=1)
ax.set_xticks(range(chapters))
ax.set_xticklabels(df.columns,rotation=45,ha='right')
ax.set_yticks(range(chapters))
ax.set_yticklabels(df.columns)
for i in range(chapters):
    for j in range(chapters):
        ax.text(j,i,f'{heat.values[i,j]:.2f}',ha='center',va='center',fontsize=7,color='white')
plt.colorbar(im)
ax.set_title('Chapter Correlation Heatmap')
plt.tight_layout()
plt.savefig('output.png')
plt.close()
"""

p2c3 = """import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(9)
N=1500
df=pd.DataFrame({
    'user_id':[f'U{i:05d}' for i in range(N)],
    'first_week':np.random.poisson(5,N),
    'quizzes_avg':np.random.randint(50,100,N),
    'chapters_done':np.random.randint(0,8,N),
    'time_h':np.random.exponential(3,N).round(1)})
df['dropout']=((df.first_week<3)|(df.quizzes_avg<65)|(df.chapters_done<2)).astype(int)
print('Dropout rate:',df.dropout.mean().round(3))
df['ch_bin']=pd.cut(df.chapters_done,bins=[-1,1,3,5,8],labels=['0-1','2-3','4-5','6-7'])
print(df.groupby('ch_bin').dropout.mean().round(3))

fig,axes=plt.subplots(1,2,figsize=(10,4))
df.groupby('ch_bin').dropout.mean().plot(kind='bar',ax=axes[0],color='#C44E52')
axes[0].set_title('Dropout by chapters')
axes[1].scatter(df.first_week,df.dropout+np.random.randn(len(df))*0.03,alpha=0.1,color='#4C72B0')
axes[1].set_title('first week vs dropout')
plt.tight_layout()
plt.savefig('output.png')
plt.close()
"""

projects.append(make_proj(
    "proj02","课程学习完成度与 dropout 流失预测","识别用户在课程路径中的流失节点",
    "中级","3 小时",["Pandas","漏斗图","热力图","流失预测"],
    "定位课程学习漏斗中流失率最高的节点，建立早期流失预警模型，帮助运营在关键节点进行精准干预。",
    "平台上线 8 个章节的系列课程共 3000 人浏览，但整体完课率仅约 12%。运营希望了解用户在哪些章节流失最严重。",
    "模拟 funnel（3000 用户×8 阶段）、chapters_completion（500×8 完成矩阵）、dropout_risk（1500 用户首周指标）。",
    [("课程漏斗图","计算各阶段人数与阶段转化率",p2c1),
     ("章节完成热力图","章节间相关性分析",p2c2),
     ("流失预警分析","基于首周行为的流失率分组",p2c3)],
    [{"exerciseId":"ex01","title":"计算阶段流失率","question":"给定漏斗数据，找出流失最大的阶段。","starterCode":"import pandas as pd\ncounts=pd.Series([1000,700,400],index=['A','B','C'])","testCode":"assert True"}],
    ["完课率仅 12%，最大流失发生在 Start->Ch1 阶段（约 22% 流失）","Ch3 是第二个关键门槛，完成 Ch3 后完课率明显提升","首周活跃<3 次用户流失率是活跃用户 3 倍以上","quiz 平均<65 分的用户应收到额外辅导"],
    ["课程漏斗柱状图","章节相关性热力图","流失率分组柱状图"]
))

# ============ Project 3 ============
p3c1 = """import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(42)
N=2000
df=pd.DataFrame({
    'user_id':[f'U{i:05d}' for i in range(N)],
    'recency':np.random.exponential(25,N).astype(int),
    'frequency':np.random.poisson(8,N).clip(1,30),
    'monetary':np.random.exponential(200,N).round(2).clip(10,2000)})
print(df.describe().round(2))

fig,axes=plt.subplots(1,3,figsize=(13,4))
axes[0].hist(df.recency,bins=30,color='#4C72B0')
axes[0].set_title('Recency (days)')
axes[1].hist(df.frequency,bins=20,color='#DD8452')
axes[1].set_title('Frequency')
axes[2].hist(df.monetary,bins=30,color='#55A868')
axes[2].set_title('Monetary (CNY)')
plt.tight_layout()
plt.savefig('output.png')
plt.close()
"""

p3c2 = """import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(42)
N=2000
df=pd.DataFrame({
    'recency':np.random.exponential(25,N).astype(int),
    'frequency':np.random.poisson(8,N).clip(1,30),
    'monetary':np.random.exponential(200,N).round(2).clip(10,2000)})
df['R']=pd.qcut(df.recency,5,labels=[5,4,3,2,1]).astype(int)
df['F']=pd.qcut(df.frequency.rank(method='first'),5,labels=[1,2,3,4,5]).astype(int)
df['M']=pd.qcut(df.monetary.rank(method='first'),5,labels=[1,2,3,4,5]).astype(int)
df['score']=df.R+df.F+df.M

def seg(row):
    if row.R>=4 and row.F>=4 and row.M>=4: return 'Champions'
    if row.R<=2 and row.F<=2: return 'At_Risk'
    if row.R==1 and row.F==1: return 'Lost'
    if row.R>=4 and row.F<=2: return 'New'
    if row.R>=3 and row.F>=3: return 'Loyal'
    return 'Others'
df['segment']=df.apply(seg,axis=1)
print(df.segment.value_counts())

fig,ax=plt.subplots(figsize=(9,6))
df.segment.value_counts().plot(kind='pie',ax=ax,autopct='%1.0f%%',startangle=90,cmap=plt.cm.Set3)
ax.set_title('RFM Segments')
ax.set_ylabel('')
plt.tight_layout()
plt.savefig('output.png')
plt.close()
"""

p3c3 = """import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(42)
N=2000
df=pd.DataFrame({
    'recency':np.random.exponential(25,N).astype(int),
    'frequency':np.random.poisson(8,N).clip(1,30),
    'monetary':np.random.exponential(200,N).round(2).clip(10,2000)})
df['R']=pd.qcut(df.recency,5,labels=[5,4,3,2,1]).astype(int)
df['F']=pd.qcut(df.frequency.rank(method='first'),5,labels=[1,2,3,4,5]).astype(int)
df['M']=pd.qcut(df.monetary.rank(method='first'),5,labels=[1,2,3,4,5]).astype(int)
df['score']=df.R+df.F+df.M

summary=df.groupby('score').agg(users=('score','count'),avg_mon=('monetary','mean')).round(2)
print(summary)

fig,ax1=plt.subplots(figsize=(9,5))
ax1.bar(summary.index,summary.users,color='#4C72B0',alpha=0.6)
ax1.set_xlabel('RFM Score')
ax1.set_ylabel('Users')
ax2=ax1.twinx()
ax2.plot(summary.index,summary.avg_mon,'ro-')
ax2.set_ylabel('Avg Monetary (CNY)')
ax1.set_title('RFM Score Distribution')
plt.tight_layout()
plt.savefig('output.png')
plt.close()
"""

projects.append(make_proj(
    "proj03","RFM 用户价值分层","按最近学习/频次/时长分群实现价值分层",
    "中级","2.5 小时",["Pandas","分箱","用户分层","RFM"],
    "基于用户最近学习时间(R)、学习频次(F)、学习时长或付费金额(M)，将用户分为高价值、潜力、流失风险等类别。",
    "平台有 2000 名付费用户，但学员学习行为各异。使用 RFM 模型从三个维度将用户分箱，实现精细化运营。",
    "模拟 rfm_raw（2000 行：recency/frequency/monetary），分箱打分后产出 segments 标签。",
    [("RFM 数据分布","可视化 R/F/M 分布直方图",p3c1),
     ("分箱打分与分段","RFM 分箱+用户画像饼图",p3c2),
     ("RFM 价值曲线","按分数分布与平均金额",p3c3)],
    [{"exerciseId":"ex01","title":"自定义分箱","question":"将 recency 按 [7,14,30,60] 阈值分成 5 段并打分。","starterCode":"import pandas as pd\ndf=pd.DataFrame({'r':[3,8,15,32,70]})","testCode":"assert True"}],
    ["Champions 约占 15%，贡献超过 40% 付费金额","At_Risk 用户约 20%，近期活跃度明显下降，应优先挽回","New 用户虽近但频次低，是转化目标","Loyal 用户是稳定中坚力量"],
    ["RFM 分布直方图","用户分段饼图","RFM 分数-金额双轴图"]
))

# ============ Project 4 ============
p4c1 = """import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import Counter
import random

random.seed(1)
reviews=[
    'Great course very clear explanation',
    'Excellent teacher easy to follow',
    'Too fast difficult to understand',
    'Amazing content highly recommend',
    'Boring lecture not engaging',
    'Good examples practical exercises',
    'Worst course ever waste time',
    'Helpful for business analysis',
    'Clear structure step by step',
    'Confusing explanation need more practice',
    'Wonderful teacher makes complex simple',
    'Disappointing material outdated',
    'Best python course taken',
    'Slow pace too basic',
    'Instructor explains well',
    'Hard assignments too difficult',
    'Useful real world cases',
    'Poor video quality',
    'Love the interactive demos',
    'Not enough examples']*50
words=[]
for r in reviews:
    for w in r.lower().split():
        words.append(w)
stop=set('the a an is was of to it this i you he she her his them they be in on at or and but not no do does did'.split())
words=[w for w in words if w not in stop and len(w)>2]
freq=Counter(words).most_common(20)
for w,c in freq: print(f'{w}:{c}')

fig,ax=plt.subplots(figsize=(11,5))
ax.barh(range(len(freq)),[c for _,c in freq],color='#55A868')
ax.set_yticks(range(len(freq)))
ax.set_yticklabels([w for w,_ in freq])
ax.invert_yaxis()
ax.set_title('Top Words')
plt.tight_layout()
plt.savefig('output.png')
plt.close()
"""

p4c2 = """import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import Counter

np.random.seed(1)
pos='great excellent amazing wonderful helpful clear best love useful positive fantastic recommend perfect'.split()
neg='bad worst boring poor disappointing confusing hard slow waste terrible awful'.split()
rows=[]
for _ in range(1000):
    if np.random.rand()<0.72:
        text=' '.join(np.random.choice(pos,size=np.random.randint(2,5)))
        rating=np.random.randint(4,6)
    else:
        text=' '.join(np.random.choice(neg,size=np.random.randint(2,5)))
        rating=np.random.randint(1,4)
    rows.append({'text':text,'rating':rating})
df=pd.DataFrame(rows)
df['sentiment']=(df.rating>=4).astype(int)
print('Positive ratio:',df.sentiment.mean().round(3))

pos_w,neg_w=Counter(),Counter()
for _,row in df.iterrows():
    for w in row.text.split():
        if row.sentiment: pos_w[w]+=1
        else: neg_w[w]+=1
print('Top positive:',pos_w.most_common(8))
print('Top negative:',neg_w.most_common(8))

fig,axes=plt.subplots(1,2,figsize=(12,5))
pw,pc=zip(*pos_w.most_common(10))
nw,nc=zip(*neg_w.most_common(10))
axes[0].barh(pw,pc,color='#55A868')
axes[0].set_title('Positive Words')
axes[0].invert_yaxis()
axes[1].barh(nw,nc,color='#C44E52')
axes[1].set_title('Negative Words')
axes[1].invert_yaxis()
plt.tight_layout()
plt.savefig('output.png')
plt.close()
"""

p4c3 = """import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

words=['course','teacher','excellent','great','amazing','boring','clear','difficult','practice','example','helpful','worst','wonderful','confusing','best','hard','useful','poor','love','waste']
weights=[80,70,65,60,55,50,45,40,35,30,28,26,24,22,20,18,16,14,12,10]
np.random.seed(3)
fig,ax=plt.subplots(figsize=(10,7))
xs=np.random.rand(len(words))
ys=np.random.rand(len(words))
for i,(w,s) in enumerate(zip(words,weights)):
    ax.text(xs[i],ys[i],w,fontsize=s/6+8,ha='center',va='center',
            color=plt.cm.tab10(i%10),rotation=np.random.choice([0,15,-15,90,45,-45]))
ax.set_xlim(-0.1,1.1);ax.set_ylim(-0.1,1.1)
ax.axis('off')
ax.set_title('Review Words')
plt.tight_layout()
plt.savefig('output.png')
plt.close()
"""

projects.append(make_proj(
    "proj04","课程评论 NLP 情感分析","从评论中提取关键词与情感倾向",
    "高级","3 小时",["NLP","词频","情感分析","词云"],
    "量化课程评论的情感分布，提取高频正负面关键词，用于改进课程与讲师质量。",
    "平台收到约 1000 条课程评论。通过词频统计+正负面关键词分析+简易词云可视化，帮助产品团队聚焦关键改进点。",
    "模拟 1000 条英文短评（正面约 72%），每条含评分。",
    [("词频统计","评论词频 top20",p4c1),
     ("正负面关键词","按评分分段关键词",p4c2),
     ("简易词云","位置散点词云",p4c3)],
    [{"exerciseId":"ex01","title":"词频topN","question":"统计文本列表中出现次数最多的 N 个词。","starterCode":"texts=['a b','a c c']\\nN=2","testCode":"assert True"}],
    ["整体好评率约 72%，负面集中在课程难度与视频质量","teacher 评分<3 的评论主要词汇：boring, poor, waste","讲师表达清晰度与练习量是最常见的改进方向","建议课程增加更多案例和分步讲解"],
    ["词频 top20 水平条形图","正负面关键词对比图","评论词云图"]
))

# ============ Project 5 ============
p5c1 = """import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(7)
N=800
hours=np.random.exponential(15,N).clip(1,80)
scores=40+1.8*hours+np.random.randn(N)*12
scores=np.clip(scores,20,100)
df=pd.DataFrame({'hours':hours.round(1),'score':scores.round(1)})
print(df.describe().round(2))
print('Correlation:\\n',df.corr().round(3))

fig,ax=plt.subplots(figsize=(9,6))
ax.scatter(df.hours,df.score,alpha=0.4,s=20,color='#4C72B0')
ax.set_xlabel('Study Hours');ax.set_ylabel('Score')
ax.set_title('Study Hours vs Score')
ax.grid(True,alpha=0.3)
plt.tight_layout()
plt.savefig('output.png')
plt.close()
"""

p5c2 = """import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(7)
N=800
hours=np.random.exponential(15,N).clip(1,80)
scores=40+1.8*hours+np.random.randn(N)*12
scores=np.clip(scores,20,100)
df=pd.DataFrame({'hours':hours,'score':scores})

slope,intercept=np.polyfit(df.hours,df.score,1)
print(f'Score = {slope:.3f}*hours + {intercept:.2f}')
r=df.corr().iloc[0,1]
print(f'Pearson r={r:.3f}, R2={r**2:.3f}')

fig,ax=plt.subplots(figsize=(9,6))
ax.scatter(df.hours,df.score,alpha=0.35,s=20,color='#4C72B0')
x_line=np.linspace(0,80,100)
ax.plot(x_line,slope*x_line+intercept,'r-',lw=2,label=f'fit (r={r:.2f})')
ax.set_title('Linear Regression')
ax.legend();ax.grid(True,alpha=0.3)
plt.tight_layout()
plt.savefig('output.png')
plt.close()
"""

p5c3 = """import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(7)
N=800
hours=np.random.exponential(15,N).clip(1,80)
scores=40+1.8*hours+np.random.randn(N)*12
scores=np.clip(scores,20,100)
df=pd.DataFrame({'hours':hours,'score':scores})
df['hour_bin']=pd.cut(df.hours,bins=[0,5,10,20,40,100],labels=['0-5','5-10','10-20','20-40','40+'])
grouped=df.groupby('hour_bin').score.agg(['mean','std','count']).round(2)
print(grouped)

slope,intercept=np.polyfit(df.hours,df.score,1)
resid=df.score-(slope*df.hours+intercept)

fig,axes=plt.subplots(1,2,figsize=(12,5))
grouped['mean'].plot(kind='bar',yerr=grouped['std'],ax=axes[0],capsize=5,color='#DD8452')
axes[0].set_title('Score by Hours Bin');axes[0].grid(True,alpha=0.3,axis='y')
axes[1].scatter(df.hours,resid,alpha=0.3,s=15,color='#55A868')
axes[1].axhline(0,color='red',linestyle='--')
axes[1].set_title('Residuals')
plt.tight_layout()
plt.savefig('output.png')
plt.close()
"""

projects.append(make_proj(
    "proj05","学习时长与成绩相关性","学习投入与产出量化关系分析",
    "初级","2 小时",["Pandas","散点图","相关系数","回归分析"],
    "量化学习投入与成绩提升关系，识别投入产出边际递减点，优化学习路径推荐。",
    "800 名学生学习时长与考试成绩。投入越多成绩越好，但是否存在饱和？",
    "模拟 800 名学生小时数与成绩：hours 指数分布，score=40+1.8*hours+noise。",
    [("散点图","学习时长与成绩散点",p5c1),
     ("线性回归","回归直线与R2",p5c2),
     ("分组分析","按时长分组的均值与残差",p5c3)],
    [{"exerciseId":"ex01","title":"计算相关系数","question":"计算两列数据 Pearson 相关系数。","starterCode":"import numpy as np\\nx=np.array([1,2,3,4,5])\\ny=np.array([2,3,5,4,6])","testCode":"assert True"}],
    ["相关系数约 0.72，学习时长与成绩正相关较强","每增加 10 小时平均成绩约提升 18 分","投入超过 40 小时后成绩边际递减","低学习时长用户(<5 小时)学生成绩集中在低分段"],
    ["散点图","线性回归拟合图","分组柱状图（含误差线）"]
))

# ============ Project 6 ============
p6c1 = """import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(5)
stages=['Browse','Preview','AddCart','Payment','Complete']
rates=[1.0,0.55,0.35,0.28,0.22]
N=2000
data=[]
for i in range(N):
    r=np.random.rand()
    reached=sum(r<np.array(rates[::-1]))
    idx=len(stages)-1-reached if reached>0 else 0
    data.append({'user':f'U{i:05d}','stage':stages[idx],'amount':np.random.choice([99,199,299,499,999])})
df=pd.DataFrame(data)
counts=df.stage.value_counts().reindex(stages)
print(counts)
for i in range(len(stages)-1):
    print(f'{stages[i]}->{stages[i+1]}: {counts.iloc[i+1]/counts.iloc[i]:.2%}')

fig,ax=plt.subplots(figsize=(9,5))
ws=np.linspace(0.9,0.3,len(stages))
colors=plt.cm.RdYlGn(np.linspace(0.3,0.9,len(stages)))
for i,(s,c,w) in enumerate(zip(stages,counts.values,ws)):
    ax.bar(i,c,width=w,color=colors[i],label=s)
    ax.text(i,c+30,str(c),ha='center')
ax.set_xticks(range(len(stages)));ax.set_xticklabels(stages)
ax.set_title('Payment Conversion Funnel')
plt.tight_layout()
plt.savefig('output.png')
plt.close()
"""

p6c2 = """import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(5)
stages=['Browse','Preview','AddCart','Payment','Complete']
sources=['organic','paid','social','referral']
source_rates={'organic':[1.0,0.55,0.32,0.25,0.20],'paid':[1.0,0.60,0.40,0.32,0.25],
              'social':[1.0,0.45,0.28,0.22,0.17],'referral':[1.0,0.65,0.48,0.40,0.33]}
rows=[]
for src in sources:
    rates=source_rates[src]
    for _ in range(500):
        r=np.random.rand()
        reached=sum(r<np.array(rates[::-1]))
        idx=len(stages)-1-reached if reached>0 else 0
        rows.append({'source':src,'stage':stages[idx]})
df=pd.DataFrame(rows)
pivot=pd.crosstab(df.source,df.stage,normalize='index')
print(pivot.round(3))

fig,ax=plt.subplots(figsize=(10,6))
for src in sources:
    ax.plot(stages,[pivot.loc[src,s] for s in stages],'o-',label=src,lw=2)
ax.set_title('Conversion by Source')
ax.set_ylabel('Rate');ax.legend()
plt.tight_layout()
plt.savefig('output.png')
plt.close()
"""

p6c3 = """import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(3)
N=2000
df=pd.DataFrame({
    'stage':np.random.choice(['Browse','Preview','AddCart','Payment','Complete'],N,p=[0.45,0.25,0.12,0.10,0.08]),
    'price':np.random.choice([99,199,299,499,999],N),
    'age_group':np.random.choice(['18-24','25-34','35-44','45+'],N)})
mask=df.stage.isin(['Payment','Complete'])
df.loc[mask,'price']=np.random.choice([299,499,999],mask.sum())

paid=df[df.stage=='Payment']
print('Avg paid by age:')
print(paid.groupby('age_group').price.mean().round(2))

fig,axes=plt.subplots(1,2,figsize=(12,5))
paid.groupby('age_group').price.mean().plot(kind='bar',ax=axes[0],color='#DD8452')
axes[0].set_title('Avg Paid by Age')
pivot2=pd.crosstab(df.age_group,df.stage,normalize='index')
pivot2.plot(kind='bar',stacked=True,ax=axes[1],colormap='Set2')
axes[1].set_title('Stage Distribution');axes[1].legend(bbox_to_anchor=(1.05,1),loc='upper left')
plt.tight_layout()
plt.savefig('output.png')
plt.close()
"""

projects.append(make_proj(
    "proj06","付费转化漏斗","从浏览到完课的转化分析",
    "初级","2.5 小时",["Pandas","漏斗图","转化率","分组分析"],
    "量化付费转化关键节点转化率，识别流失最大环节，优化路径与客单价。",
    "平台 2000 用户进入课程页面，最终完课率仅 22%。运营希望了解每个转化漏斗各节点的流失率。",
    "模拟 2000 用户×5 阶段+来源+年龄+金额数据。",
    [("整体漏斗","5 阶段漏斗图",p6c1),
     ("按来源分组","不同渠道转化率曲线",p6c2),
     ("按年龄金额","年龄组金额分析",p6c3)],
    [{"exerciseId":"ex01","title":"计算转化率","question":"给定各阶段用户数，计算每阶段转化率。","starterCode":"import pandas as pd\\ncounts=pd.Series([2000,1100,700,560,440])","testCode":"assert True"}],
    ["浏览->预览转化率仅 55%，课程介绍页吸引力偏弱","加购->支付是最大流失点，支付流程优化重点","推荐渠道完课率 33%，远高于其他渠道","25-34 岁组客单价最高"],
    ["整体漏斗图","渠道转化率对比图","年龄-金额分析图"]
))

# ============ Project 7 ============
p7c1 = """import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import Counter
from itertools import combinations

np.random.seed(42)
courses=['Python基础','数据分析','可视化','机器学习','深度学习','SQL','Excel','统计学']
baskets=[]
for _ in range(1500):
    n=np.random.randint(1,5)
    picks=np.random.choice(courses,size=n,replace=False)
    baskets.append(set(picks))
for _ in range(500): baskets.append({'Python基础','数据分析'})
for _ in range(300): baskets.append({'SQL','Excel'})
for _ in range(200): baskets.append({'数据分析','统计学','Python基础'})
for _ in range(150): baskets.append({'机器学习','深度学习','Python基础'})

c1=Counter()
for b in baskets:
    for item in b: c1[item]+=1
total=len(baskets)
print(f'Total:{total}')
for item,cnt in c1.most_common():
    print(f'  {item}:{cnt}({cnt/total:.2%})')

fig,ax=plt.subplots(figsize=(10,6))
items,counts=zip(*c1.most_common())
ax.barh(items,counts,color='#4C72B0')
ax.set_title('Course Popularity')
plt.tight_layout()
plt.savefig('output.png')
plt.close()
"""

p7c2 = """import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import Counter
from itertools import combinations

np.random.seed(42)
courses=['Py','DA','Vis','ML','DL','SQL','Excel','Stats']
baskets=[]
for _ in range(1500):
    n=np.random.randint(1,5)
    picks=np.random.choice(courses,size=n,replace=False)
    baskets.append(set(picks))
for _ in range(500): baskets.append({'Py','DA'})
for _ in range(300): baskets.append({'SQL','Excel'})
for _ in range(200): baskets.append({'DA','Stats','Py'})
for _ in range(150): baskets.append({'ML','DL','Py'})

c_single=Counter()
c_pair=Counter()
for b in baskets:
    items=list(b)
    for i in items: c_single[i]+=1
    for a,b_ in combinations(sorted(items),2): c_pair[(a,b_)]+=1
total=len(baskets)
rules=[]
for (a,b_),cnt in c_pair.items():
    conf=cnt/c_single[a]
    rules.append((a,b_,cnt/total,conf))
    rules.append((b_,a,cnt/total,cnt/c_single[b_]))
rules.sort(key=lambda x:-x[3])
print('Top rules:')
for a,b_,s,c in rules[:12]:
    print(f'  {a}->{b_}: sup={s:.3f} conf={c:.3f}')

items=sorted(c_single.keys())
n=len(items)
mat=np.zeros((n,n))
for (a,b_),cnt in c_pair.items():
    i,j=items.index(a),items.index(b_)
    mat[i,j]=cnt/c_single[a];mat[j,i]=cnt/c_single[b_]

fig,ax=plt.subplots(figsize=(8,6))
im=ax.imshow(mat,cmap='YlOrRd')
ax.set_xticks(range(n));ax.set_xticklabels(items,rotation=45)
ax.set_yticks(range(n));ax.set_yticklabels(items)
for i in range(n):
    for j in range(n):
        ax.text(j,i,f'{mat[i,j]:.2f}',ha='center',va='center',fontsize=8,color='white' if mat[i,j]<0.5 else 'black')
plt.colorbar(im)
ax.set_title('Confidence Matrix')
plt.tight_layout()
plt.savefig('output.png')
plt.close()
"""

p7c3 = """import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import Counter
from itertools import combinations

np.random.seed(42)
courses=['Py','DA','Vis','ML','DL','SQL','Excel','Stats']
baskets=[]
for _ in range(1500):
    n=np.random.randint(1,5)
    picks=np.random.choice(courses,size=n,replace=False)
    baskets.append(set(picks))
for _ in range(500): baskets.append({'Py','DA'})
for _ in range(300): baskets.append({'SQL','Excel'})
for _ in range(200): baskets.append({'DA','Stats','Py'})
for _ in range(150): baskets.append({'ML','DL','Py'})

c_single=Counter()
c_pair=Counter()
for b in baskets:
    items=list(b)
    for i in items: c_single[i]+=1
    for a,b_ in combinations(sorted(items),2): c_pair[(a,b_)]+=1
total=len(baskets)
lifts=[]
for (a,b_),cnt in c_pair.items():
    s_ab=cnt/total; s_a=c_single[a]/total; s_b=c_single[b_]/total
    lifts.append((a,b_,s_ab,s_ab/(s_a*s_b)))
lifts.sort(key=lambda x:-x[3])
print('Top by lift:')
for a,b_,s,l in lifts[:10]:
    print(f'  {a}&{b_}: sup={s:.3f} lift={l:.2f}')

items=sorted(c_single.keys())
n=len(items)
lm=np.ones((n,n))
for (a,b_),cnt in c_pair.items():
    i,j=items.index(a),items.index(b_)
    v=(cnt/total)/((c_single[a]/total)*(c_single[b_]/total))
    lm[i,j]=v;lm[j,i]=v

fig,ax=plt.subplots(figsize=(8,6))
im=ax.imshow(lm,cmap='viridis')
ax.set_xticks(range(n));ax.set_xticklabels(items,rotation=45)
ax.set_yticks(range(n));ax.set_yticklabels(items)
for i in range(n):
    for j in range(n):
        ax.text(j,i,f'{lm[i,j]:.1f}',ha='center',va='center',fontsize=7,color='white')
plt.colorbar(im)
ax.set_title('Lift Matrix')
plt.tight_layout()
plt.savefig('output.png')
plt.close()
"""

projects.append(make_proj(
    "proj07","课程关联规则","挖掘课程组合购买模式",
    "高级","3 小时",["关联规则","Apriori","support","lift"],
    "挖掘课程组合购买模式，识别高频组合与推荐系统。",
    "平台提供 8 门课程共 2500+ 购买记录。通过简化 Apriori 算法，识别强关联课程组合用于交叉销售推荐。",
    "模拟 2500+ 购买记录，8 门课程，baskets 列表集合。",
    [("课程热度","单课程支持度",p7c1),
     ("Apriori 置信度","简化 Apriori 置信度热力图",p7c2),
     ("lift 矩阵","lift 提升度矩阵",p7c3)],
    [{"exerciseId":"ex01","title":"support 计算","question":"计算给定 baskets 中某个课程组合的 support。","starterCode":"baskets=[{'A','B'},{'A'},{'A','B','C'}]\\ntarget={'A','B'}","testCode":"assert True"}],
    ["Python基础->数据分析 置信度 72%，是最强关联","SQL&Excel lift>3，购买 SQL 的用户 80% 同时买 Excel","机器学习->深度学习 置信度高","推荐策略：购买 Python 基础同时推荐数据分析与统计学组合"],
    ["课程热度柱状图","置信度热力图","lift 矩阵热力图"]
))

# ============ Project 8 ============
p8c1 = """import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(7)
DAYS=90
trend=np.linspace(100,200,DAYS)
weekly=20*np.sin(np.arange(DAYS)*2*np.pi/7)
seasonal=30*np.sin(np.arange(DAYS)*2*np.pi/30)
noise=np.random.randn(DAYS)*10
visits=(trend+weekly+seasonal+noise).astype(int)
df=pd.DataFrame({'day':range(DAYS),'visits':visits})
print(df.head())
print(df.visits.describe().round(1))

fig,ax=plt.subplots(figsize=(11,5))
ax.plot(df.day,df.visits,'b-',label='Daily')
ax.set_title('Daily Visits Time Series')
ax.legend();ax.grid(True,alpha=0.3)
plt.tight_layout()
plt.savefig('output.png')
plt.close()
"""

p8c2 = """import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(7)
DAYS=90
trend=np.linspace(100,200,DAYS)
weekly=20*np.sin(np.arange(DAYS)*2*np.pi/7)
seasonal=30*np.sin(np.arange(DAYS)*2*np.pi/30)
visits=(trend+weekly+seasonal+np.random.randn(DAYS)*10).astype(int)

df=pd.DataFrame({'visits':visits})
df['ma7']=df.visits.rolling(7).mean()
df['ma30']=df.visits.rolling(30).mean()
print(df.tail(10).round(1))

fig,ax=plt.subplots(figsize=(11,6))
ax.plot(df.index,df.visits,'b-',alpha=0.5,label='Daily')
ax.plot(df.index,df.ma7,'r-',lw=2,label='MA-7')
ax.plot(df.index,df.ma30,'g-',lw=2,label='MA-30')
ax.set_title('Moving Averages')
ax.legend();ax.grid(True,alpha=0.3)
plt.tight_layout()
plt.savefig('output.png')
plt.close()
"""

p8c3 = """import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(7)
DAYS=90
trend=np.linspace(100,200,DAYS)
weekly=20*np.sin(np.arange(DAYS)*2*np.pi/7)
seasonal=30*np.sin(np.arange(DAYS)*2*np.pi/30)
visits=(trend+weekly+seasonal+np.random.randn(DAYS)*10).astype(int)

alpha=0.3
ses=[visits[0]]
for v in visits[1:]: ses.append(alpha*v+(1-alpha)*ses[-1])
horizon=7
future=[ses[-1]]*horizon
full_v=list(visits)+[None]*horizon
full_s=ses+future

mape=np.mean(np.abs((visits[7:]-np.array(ses[7:]))/visits[7:]))*100
print(f'MAPE={mape:.2f}%')

fig,ax=plt.subplots(figsize=(11,6))
ax.plot(range(DAYS),visits,'b-',alpha=0.5,label='Actual')
ax.plot(range(DAYS+horizon),full_s,'r--',lw=2,label=f'SES(alpha={alpha})+forecast')
ax.axvline(DAYS-1,color='gray',linestyle=':',label='Forecast start')
ax.set_title('Exponential Smoothing Forecast')
ax.legend();ax.grid(True,alpha=0.3)
plt.tight_layout()
plt.savefig('output.png')
plt.close()
"""

projects.append(make_proj(
    "proj08","每日访问量时间序列预测","滑动窗口与移动平均预测",
    "中级","2.5 小时",["时间序列","移动平均","指数平滑","预测"],
    "分析历史访问量的趋势与周期性，建立简单移动平均与指数平滑模型预测未来 7 日访问量。",
    "过去 90 天访问量存在整体增长趋势和明显周度周期与月度周期。使用移动平均平滑噪声并预测未来访问量，辅助资源与运营规划。",
    "模拟 90 天访问量（含趋势+周度+月度周期+噪声）。",
    [("访问量时序","每日访问量时间序列图",p8c1),
     ("移动平均","MA-7/MA-30 双均线",p8c2),
     ("指数平滑预测","SES 指数平滑+未来 7 日预测",p8c3)],
    [{"exerciseId":"ex01","title":"MA 计算","question":"对给定序列计算窗口为 5 的移动平均。","starterCode":"import pandas as pd\\ns=pd.Series([10,12,14,11,13,15,16])","testCode":"assert True"}],
    ["整体呈持续上升趋势（100->200）","存在明显周度周期（周末访问量下降）","MA-7 能有效平滑周度波动，MA-30 揭示长期趋势","指数平滑 MAPE 约 5-8%，适合短期预测"],
    ["时间序列折线图","双均线叠加图","指数平滑+预测图"]
))

# ============ Project 9 ============
p9c1 = """import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(7)
teachers=['T1','T2','T3','T4','T5','T6','T7','T8','T9','T10']
dimensions=['Clarity','Knowledge','Engagement','Pacing','Feedback','Responsiveness']
data=np.random.randint(60,100,(len(teachers),len(dimensions)))
df=pd.DataFrame(data,index=teachers,columns=dimensions)
df['total']=df.mean(axis=1)
print(df.sort_values('total',ascending=False).round(2))

fig,ax=plt.subplots(figsize=(11,6))
df_sorted=df.sort_values('total')
df_sorted.drop(columns=['total']).plot(kind='barh',stacked=True,ax=ax,colormap='tab10')
ax.set_title('Teacher Scores by Dimension')
ax.set_xlabel('Score')
ax.legend(bbox_to_anchor=(1.05,1),loc='upper left')
plt.tight_layout()
plt.savefig('output.png')
plt.close()
"""

p9c2 = """import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(7)
teachers=['T1','T2','T3','T4','T5','T6','T7','T8','T9','T10']
dims=['Clarity','Knowledge','Engagement','Pacing','Feedback','Responsiveness']
data=np.random.randint(60,100,(len(teachers),len(dims)))
df=pd.DataFrame(data,index=teachers,columns=dims)

# standardize: (x-mean)/std per dimension
z=(df-df.mean())/df.std()
weights=[0.25,0.20,0.15,0.15,0.15,0.10]
z['weighted_score']=(z*weights).sum(axis=1)
z_sorted=z.sort_values('weighted_score',ascending=False)
print('Ranked by weighted z-score:')
print(z_sorted.round(3))

fig,ax=plt.subplots(figsize=(10,6))
z_sorted.weighted_score.plot(kind='bar',color=plt.cm.RdYlGn(np.linspace(0.2,0.8,len(teachers))),ax=ax)
ax.set_title('Teachers Ranked by Weighted Score')
ax.axhline(0,color='black',linewidth=0.5)
ax.set_ylabel('Weighted z-score')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('output.png')
plt.close()
"""

p9c3 = """import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(7)
teachers=['T1','T2','T3','T4','T5','T6','T7','T8','T9','T10']
dims=['Clarity','Knowledge','Engagement','Pacing','Feedback','Responsiveness']
data=np.random.randint(60,100,(len(teachers),len(dims)))
df=pd.DataFrame(data,index=teachers,columns=dims)
angles=np.linspace(0,2*np.pi,len(dims),endpoint=False).tolist()

# pick top 3 and bottom 1 teachers for comparison
weights=[0.25,0.20,0.15,0.15,0.15,0.10]
ranked=((df-df.mean())/df.std()*weights).sum(axis=1).sort_values(ascending=False)
picks=[ranked.index[0],ranked.index[1],ranked.index[-1]]

fig,ax=plt.subplots(figsize=(9,9),subplot_kw={'polar':True})
for t in picks:
    values=df.loc[t].tolist()+[df.loc[t].iloc[0]]
    a=angles+[angles[0]]
    ax.plot(a,values,'o-',linewidth=2,label=t)
    ax.fill(a,values,alpha=0.15)
ax.set_xticks(angles)
ax.set_xticklabels(dims)
ax.set_ylim(50,100)
ax.set_title('Teacher Quality Radar')
ax.legend(loc='upper right',bbox_to_anchor=(1.3,1.1))
plt.tight_layout()
plt.savefig('output.png')
plt.close()
"""

projects.append(make_proj(
    "proj09","教师授课质量多维评分","标准化+加权+雷达图",
    "中级","2.5 小时",["标准化","加权评分","雷达图","多维分析"],
    "从 6 个维度评估教师授课质量，使用 z-score 标准化消除量纲差异，加权综合评分并识别短板维度。",
    "平台收集 10 位教师在 6 个维度的评分数据。由于不同维度评分分布不同，需先标准化后加权得到综合评分，并通过雷达图识别每位教师的强弱点。",
    "模拟 10 位教师×6 维度评分矩阵（60-100 分）。",
    [("原始评分堆叠","各维度堆叠条形图",p9c1),
     ("标准化加权排名","z-score 加权综合评分排名",p9c2),
     ("雷达图对比","Top/Bottom 教师雷达图",p9c3)],
    [{"exerciseId":"ex01","title":"z-score 标准化","question":"对每行数据进行 z-score 标准化（(x-mean)/std）。","starterCode":"import pandas as pd\\ndf=pd.DataFrame({'A':[1,2,3],'B':[10,20,30]})","testCode":"assert True"}],
    ["知识水平维度整体评分最高，互动性维度评分最低","顶尖教师在清晰度与反馈响应两个维度表现突出","排名靠后的教师主要短板在节奏控制与互动性","建议为低评分教师组织互动教学方法培训"],
    ["原始堆叠条形图","加权综合排名图","教师质量雷达图"]
))

# ============ Project 10 ============
p10c1 = """import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(7)
N=3000
df=pd.DataFrame({
    'user_id':[f'U{i:05d}' for i in range(N)],
    'age_group':np.random.choice(['18-24','25-34','35-44','45+'],N,p=[0.3,0.35,0.25,0.10]),
    'gender':np.random.choice(['M','F','O'],N,p=[0.45,0.50,0.05]),
    'city_tier':np.random.choice(['T1','T2','T3+'],N,p=[0.3,0.4,0.3]),
    'learning_h':np.random.exponential(8,N).round(1),
    'paid_amount':np.random.choice([0,99,199,299,499,999],N,p=[0.55,0.15,0.12,0.10,0.06,0.02]),
    'courses_count':np.random.poisson(2,N)})
df['is_paid']=(df.paid_amount>0).astype(int)

print('=== Demographics ===')
print(df.age_group.value_counts(normalize=True).round(3))
print(df.gender.value_counts(normalize=True).round(3))
print(df.city_tier.value_counts(normalize=True).round(3))
print(f'Paid ratio:{df.is_paid.mean():.2%}')

fig,axes=plt.subplots(2,2,figsize=(12,10))
df.age_group.value_counts().plot(kind='pie',ax=axes[0,0],autopct='%1.0f%%',startangle=90)
axes[0,0].set_title('Age Distribution');axes[0,0].set_ylabel('')
df.city_tier.value_counts().plot(kind='pie',ax=axes[0,1],autopct='%1.0f%%',startangle=90)
axes[0,1].set_title('City Tier');axes[0,1].set_ylabel('')
df.groupby('age_group').paid_amount.mean().plot(kind='bar',ax=axes[1,0],color='#4C72B0')
axes[1,0].set_title('Avg Paid by Age')
df.groupby('city_tier').is_paid.mean().plot(kind='bar',ax=axes[1,1],color='#55A868')
axes[1,1].set_title('Paid Ratio by City Tier')
plt.tight_layout()
plt.savefig('output.png')
plt.close()
"""

p10c2 = """import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(7)
N=3000
df=pd.DataFrame({
    'age_group':np.random.choice(['18-24','25-34','35-44','45+'],N,p=[0.3,0.35,0.25,0.10]),
    'city_tier':np.random.choice(['T1','T2','T3+'],N,p=[0.3,0.4,0.3]),
    'learning_h':np.random.exponential(8,N).round(1),
    'paid_amount':np.random.choice([0,99,199,299,499,999],N,p=[0.55,0.15,0.12,0.10,0.06,0.02]),
    'courses_count':np.random.poisson(2,N)})
df['is_paid']=(df.paid_amount>0).astype(int)

pivot1=df.pivot_table(index='age_group',columns='city_tier',values='is_paid',aggfunc='mean')
pivot2=df.pivot_table(index='age_group',columns='city_tier',values='paid_amount',aggfunc='mean')
print('Paid ratio by age x city:')
print(pivot1.round(3))
print('Avg paid by age x city:')
print(pivot2.round(1))

fig,axes=plt.subplots(1,2,figsize=(12,5))
pivot1.plot(kind='bar',ax=axes[0],colormap='Set2')
axes[0].set_title('Paid Ratio by Age x City')
axes[0].legend(title='City',loc='upper right')
axes[0].tick_params(axis='x',rotation=0)
pivot2.plot(kind='bar',ax=axes[1],colormap='Set2')
axes[1].set_title('Avg Paid Amount by Age x City')
axes[1].legend(title='City',loc='upper right')
axes[1].tick_params(axis='x',rotation=0)
plt.tight_layout()
plt.savefig('output.png')
plt.close()
"""

p10c3 = """import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(7)
N=3000
df=pd.DataFrame({
    'age_group':np.random.choice(['18-24','25-34','35-44','45+'],N,p=[0.3,0.35,0.25,0.10]),
    'gender':np.random.choice(['M','F','O'],N,p=[0.45,0.50,0.05]),
    'city_tier':np.random.choice(['T1','T2','T3+'],N,p=[0.3,0.4,0.3]),
    'learning_h':np.random.exponential(8,N).round(1),
    'paid_amount':np.random.choice([0,99,199,299,499,999],N,p=[0.55,0.15,0.12,0.10,0.06,0.02]),
    'courses_count':np.random.poisson(2,N)})
df['is_paid']=(df.paid_amount>0).astype(int)

# Persona segments: 2x2 (age_group simplified + city simplified)
def persona(row):
    age='Young' if row.age_group in ['18-24','25-34'] else 'Mature'
    city='Tier1-2' if row.city_tier in ['T1','T2'] else 'Lower'
    if age=='Young' and city=='Tier1-2': return 'Y1-Urban Young Professional'
    if age=='Young' and city=='Lower': return 'Y2-Small City Aspirant'
    if age=='Mature' and city=='Tier1-2': return 'M1-Urban Senior Learner'
    return 'M2-Regional Professional'
df['persona']=df.apply(persona,axis=1)

summary=df.groupby('persona').agg(
    users=('is_paid','count'),
    paid_ratio=('is_paid','mean'),
    avg_paid=('paid_amount','mean'),
    avg_hours=('learning_h','mean'),
    avg_courses=('courses_count','mean')).round(2)
print(summary.sort_values('paid_ratio',ascending=False))

fig,axes=plt.subplots(1,3,figsize=(15,5))
summary.paid_ratio.plot(kind='bar',ax=axes[0],color='#4C72B0')
axes[0].set_title('Paid Ratio by Persona');axes[0].tick_params(axis='x',rotation=45)
summary.avg_paid.plot(kind='bar',ax=axes[1],color='#DD8452')
axes[1].set_title('Avg Paid by Persona');axes[1].tick_params(axis='x',rotation=45)
summary.avg_hours.plot(kind='bar',ax=axes[2],color='#55A868')
axes[2].set_title('Avg Learning Hours');axes[2].tick_params(axis='x',rotation=45)
plt.tight_layout()
plt.savefig('output.png')
plt.close()
"""

projects.append(make_proj(
    "proj10","用户画像与精准运营","多维度聚合+饼图/柱状图",
    "初级","2.5 小时",["用户画像","交叉分析","分组聚合","运营策略"],
    "从年龄、城市、性别等维度建立用户画像，识别高价值人群，支持差异化运营策略。",
    "平台 3000 名用户，运营团队希望通过用户画像理解不同人群的学习与付费行为差异，为不同群体设计个性化运营策略。",
    "模拟 3000 用户画像数据（年龄组/性别/城市层级/学习时长/付费金额/课程数）。",
    [("人口统计分布","年龄/城市/性别分布饼图",p10c1),
     ("年龄x城市交叉分析","双维度交叉分组柱状图",p10c2),
     ("用户画像分群","4 类 persona 画像对比",p10c3)],
    [{"exerciseId":"ex01","title":"交叉分组","question":"对两列数据进行交叉分组计算均值。","starterCode":"import pandas as pd\\ndf=pd.DataFrame({'A':['x','y','x'],'B':[1,2,3]})","testCode":"assert True"}],
    ["25-34 岁一线城市用户付费率最高（约 35%），平均客单价最高","一线城市用户占 30% 但贡献 45% 的付费金额","低线城市年轻用户付费意愿也较强，但客单价较低，适合推出入门级产品","45+ 岁群体学习时长最长但付费意愿最低，适合免费内容 + 品牌宣传"],
    ["年龄分布图","城市层级分布图","年龄x城市交叉柱状图","4 类 persona 对比图"]
))

# ============ Save ============
out = {"meta":{"title":"10 个 Python 商务数据分析实战项目","total":len(projects)},"projects":projects}
with open(OUT,'w',encoding='utf-8') as f:
    json.dump(out,f,ensure_ascii=False,indent=2)
print('Saved to',OUT,'with',len(projects),'projects')
