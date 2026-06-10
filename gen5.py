import json, os
os.chdir("/workspace")

def chapter(cid, title, objectives, content, code_samples, exercises, summary):
    return {"chapter_id": cid, "title": title, "objectives": objectives,
            "content": content, "code_samples": code_samples, "exercises": exercises, "summary": summary}
def cs(i, title, code, explanation):
    return {"id": i, "title": title, "code": code, "explanation": explanation}
def ex(eid, prompt, starter, test, hints, ref):
    return {"exerciseId": eid, "prompt": prompt, "starterCode": starter,
            "testCode": test, "hints": hints, "referenceAnswer": ref}

# ================== U5: 商务统计分析 (4章) ==================
UNIT5 = {"unitId": "u05", "title": "商务统计分析", "chapters": [
    chapter("ch0501", "描述统计：集中趋势与离散程度",
        ["掌握 mean/median/mode 三种集中趋势度量", "掌握 std/var/quantile/min/max 离散程度度量", "学会使用 describe() 生成完整统计摘要", "能够在商务场景中正确解读统计量"],
        "在商务数据分析中，我们常常需要回答这些问题：平均每个客户的年消费是多少？销售额的波动大不大？最常见的订单金额是多少？描述统计学正是用来回答这些问题的。集中趋势度量（均值、中位数、众数）告诉我们数据的中心位置；离散程度度量（标准差、方差、分位数、极差）告诉我们数据的分散程度。均值对极端值敏感，中位数更稳健；在存在大额 VIP 客户的消费数据分析中，中位数往往比均值更能代表典型客户水平。标准差越大说明销售波动越大，经营风险越高。分位数可以揭示 TOP 客户贡献了多少销售额。掌握这些基本统计量是所有高级分析的基础。",
        [
            cs("cs050101", "基本描述统计",
                "import pandas as pd\nimport numpy as np\ndata={'客户':['A','B','C','D','E','F','G','H','I','J'],'年消费':[5800,28500,12600,58200,15600,35200,72800,5800,85200,65400]}\ndf=pd.DataFrame(data)\nprint('均值:',int(df['年消费'].mean()))\nprint('中位数:',int(df['年消费'].median()))\nprint('众数:',df['年消费'].mode().tolist())\nprint('标准差:',int(df['年消费'].std()))\nprint('最小值:',df['年消费'].min())\nprint('最大值:',df['年消费'].max())\nprint('极差:',df['年消费'].max()-df['年消费'].min())\nprint('\\n完整描述:')\nprint(df['年消费'].describe())",
                "mean() 计算均值，median() 计算中位数，mode() 返回众数。std() 计算标准差。describe() 一次性生成 count/mean/std/min/25%/50%/75%/max 等常见统计量。注意众数可能有多个，mode() 返回 Series。"),
            cs("cs050102", "分位数与 Pareto 分析",
                "import pandas as pd\nimport numpy as np\nnp.random.seed(0)\n# 模拟 100 位客户的年消费\nconsumption=np.random.exponential(15000,100).astype(int)\ndf=pd.DataFrame({'年消费':consumption})\nprint('25%分位数:',df['年消费'].quantile(0.25))\nprint('50%分位数(中位数):',df['年消费'].quantile(0.50))\nprint('75%分位数:',df['年消费'].quantile(0.75))\nprint('90%分位数:',df['年消费'].quantile(0.90))\nprint('95%分位数:',df['年消费'].quantile(0.95))\n# Pareto 分析：TOP 20% 客户贡献多少销售额\nsorted_df=df.sort_values('年消费',ascending=False)\ntop20=int(len(df)*0.20)\ntop20_sum=sorted_df.head(top20)['年消费'].sum()\ntotal_sum=df['年消费'].sum()\nprint(f'TOP 20%客户贡献占比:{top20_sum/total_sum*100:.1f}%')",
                "quantile(q) 计算 q 分位数。将数据按消费额降序排列，取前 20% 的客户计算其消费总额占比，就是经典的帕累托分析（80/20法则：大约 20% 的客户贡献 80% 的销售额）。分位数分析对于识别高端客户、制定差异化策略非常重要。"),
            cs("cs050103", "按分组计算描述统计",
                "import pandas as pd\nimport io\ntext='''区域,月份,销售额,订单数,客户数\n华东,1月,125000,420,358\n华北,1月,98000,310,265\n华南,1月,112000,380,322\n华东,2月,118000,395,340\n华北,2月,105000,340,278\n华南,2月,128000,420,352\n华东,3月,142000,480,395\n华北,3月,112000,365,290\n华南,3月,135000,450,368\n'''\ndf=pd.read_csv(io.StringIO(text))\nprint('按区域统计销售额:')\nprint(df.groupby('区域')['销售额'].agg(['mean','median','std','min','max','sum']))\nprint('\\n各区域客单价=销售额/订单数:')\nagg=df.groupby('区域').apply(lambda x:pd.Series({'总销售额':x['销售额'].sum(),'总订单':x['订单数'].sum(),'平均客单价':x['销售额'].sum()/x['订单数'].sum()}),include_groups=False)\nprint(agg.round(2))",
                "groupby + agg 可以按区域等维度分组计算多列多个统计量。agg(['mean','median','std','min','max','sum']) 一次计算多个汇总。对更复杂的派生指标（如客单价 = 销售额 / 订单数），可以先分组聚合再相除，得到更准确的结果。")
        ],
        [
            ex("ex050101", "DataFrame df 包含 10 位客户年消费数据：客户 ['A','B','C','D','E','F','G','H','I','J']，年消费 [5800,28500,12600,58200,15600,35200,72800,5800,85200,65400]。请计算：mean_val 均值；median_val 中位数；std_val 标准差；min_val 最小值；max_val 最大值；range_val 极差（最大值-最小值）。所有数值保留整数。",
                "import pandas as pd\ndf=pd.DataFrame({'客户':['A','B','C','D','E','F','G','H','I','J'],'年消费':[5800,28500,12600,58200,15600,35200,72800,5800,85200,65400]})\nmean_val=0\nmedian_val=0\nstd_val=0\nmin_val=0\nmax_val=0\nrange_val=0",
                "import numpy as np\nassert abs(mean_val-38510)<1\nassert abs(median_val-31850)<1\nassert abs(std_val-29356)<5\nassert min_val==5800\nassert max_val==85200\nassert range_val==79400",
                ["df['年消费'].mean() 计算均值", "df['年消费'].median() 中位数", "df['年消费'].std() 标准差", "min()/max() 最值，极差=最大值-最小值", "可以用 int() 或 round() 取整"],
                "mean_val=int(df['年消费'].mean())\nmedian_val=int(df['年消费'].median())\nstd_val=int(df['年消费'].std())\nmin_val=df['年消费'].min()\nmax_val=df['年消费'].max()\nrange_val=max_val-min_val"),
            ex("ex050102", "df 包含 3 区域 3 个月销售数据（区域、销售额、订单数列）。数据：华东/125000/420，华北/98000/310，华南/112000/380，华东/118000/395，华北/105000/340，华南/128000/420，华东/142000/480，华北/112000/365，华南/135000/450。请计算：按区域汇总销售额总和存入 region_sum（Series，索引为区域名）；各区域总销售额除以总订单数得到客单价 avg_price（Series）；最高销售额区域 top_region（字符串）。",
                "import pandas as pd\ndata={'区域':['华东','华北','华南','华东','华北','华南','华东','华北','华南'],'销售额':[125000,98000,112000,118000,105000,128000,142000,112000,135000],'订单数':[420,310,380,395,340,420,480,365,450]}\ndf=pd.DataFrame(data)\nregion_sum=None\navg_price=None\ntop_region=''",
                "import numpy as np\nassert region_sum['华东']==385000 and region_sum['华北']==315000 and region_sum['华南']==375000\nassert abs(avg_price['华东']-297)<1\nassert abs(avg_price['华南']-295)<1\nassert top_region=='华东'",
                ["region_sum = df.groupby('区域')['销售额'].sum()", "订单汇总 = df.groupby('区域')['订单数'].sum()，然后 avg_price = region_sum / 订单汇总", "top_region = region_sum.idxmax()"],
                "region_sum=df.groupby('区域')['销售额'].sum()\norder_sum=df.groupby('区域')['订单数'].sum()\navg_price=(region_sum/order_sum).round(0)\ntop_region=region_sum.idxmax()")
        ], "描述统计是所有数据分析的起点。均值/中位数/众数揭示集中趋势，标准差/分位数/极差揭示离散程度。按分组计算这些统计量可以快速发现不同区域、不同客户群的差异。"),
    chapter("ch0502", "假设检验：独立样本 t 检验与 z 检验",
        ["理解假设检验的基本思想（p 值、显著性水平）", "掌握两独立样本 t 检验的适用场景", "能够解读检验结果并判断差异显著性", "能够在 Python 中使用 scipy.stats 进行检验"],
        "在商务决策中，我们经常需要判断某个变化是否真的产生了影响。例如：新的营销策略实施后，销售额的提升是真的有效还是只是随机波动？两个区域的平均客单价是否真的存在显著差异？假设检验是回答这些问题的科学方法。基本思路是：设立一个原假设（例如 '两组的平均值相等'）和一个备择假设，然后计算在原假设成立的情况下观察到当前数据的概率（即 p 值）。如果 p 值很小（通常 < 0.05），我们就拒绝原假设，认为差异是统计显著的。scipy.stats.ttest_ind() 可以执行两独立样本 t 检验。scipy.stats.ttest_1samp() 可以进行单样本 t 检验。掌握假设检验，可以让你避免将随机波动误判为真正的业务改进，也能帮助真正有效的改进措施获得数据支持。",
        [
            cs("cs050201", "独立样本 t 检验：两区域销售差异",
                "import pandas as pd\nimport numpy as np\nfrom scipy import stats\nnp.random.seed(42)\nregion_a=np.random.normal(520,80,30).round(0)\nregion_b=np.random.normal(480,70,30).round(0)\nprint('区域A平均客单价:',round(region_a.mean(),1))\nprint('区域B平均客单价:',round(region_b.mean(),1))\nt_stat,p_value=stats.ttest_ind(region_a,region_b)\nprint('t统计量:',round(t_stat,4))\nprint('p值:',round(p_value,4))\nif p_value<0.05:\n    print('结论:p<0.05,两区域客单价存在显著差异')\nelse:\n    print('结论:p>=0.05,两区域客单价无显著差异')",
                "np.random.normal(均值, 标准差, 数量) 生成模拟数据。stats.ttest_ind(a, b) 执行两独立样本 t 检验，返回 t 统计量和 p 值。p<0.05 拒绝'两组均值相等'的原假设，认为存在显著差异。"),
            cs("cs050202", "单样本 t 检验：改进后是否显著提升",
                "import numpy as np\nfrom scipy import stats\nnp.random.seed(0)\n# 改进前平均客单价 = 300\noriginal_mean=300\n# 改进后 20 天的客单价数据\nnew_data=np.array([325,318,342,308,335,350,312,298,345,320,338,328,315,348,322,305,340,318,332,327])\nprint('改进后平均:',round(new_data.mean(),1))\nprint('改进后标准差:',round(new_data.std(ddof=1),1))\nt_stat,p_value=stats.ttest_1samp(new_data,original_mean)\nprint('t统计量:',round(t_stat,4))\nprint('p值:',round(p_value,6))\nprint('单边检验p值(改进后是否高于原水平):',round(p_value/2,6))\nif p_value<0.05:\n    print('显著差异:改进有效')\nelse:\n    print('无显著差异')",
                "ttest_1samp(样本, 假设均值) 检验样本均值是否显著不同于假设均值。当只关心是否'高于'（而非'不同'）时，可以用单边检验，此时 p 值需除以 2。如果样本均值高于原假设且双边 p<0.10，单边检验就可以显著。"),
            cs("cs050203", "配对 t 检验：前后对比设计",
                "import numpy as np\nfrom scipy import stats\nnp.random.seed(123)\n# 10个门店培训前后的日销售额\nbefore=np.array([8500,9200,7800,10500,8800,9500,7500,8200,9800,8100])\nafter=np.array([9200,10100,8500,11200,9500,10200,8200,8800,10500,8700])\ndiff=after-before\nprint('每店销售额提升:',diff.tolist())\nprint('平均提升:',int(diff.mean()))\nt_stat,p_value=stats.ttest_rel(after,before)\nprint('配对t检验 p值:',round(p_value,6))\nif p_value<0.05:\n    print('培训显著提升了销售额')\nelse:\n    print('培训效果不显著')",
                "ttest_rel(a, b) 用于配对样本（同一组对象在前后两种条件下的测量）。配对检验比独立样本检验更敏感，因为它消除了个体差异的影响，只关注每个对象自身的变化。在 A/B 测试、培训效果评估等场景中非常适用。")
        ],
        [
            ex("ex050201", "检验两个区域的客单价是否存在显著差异。区域A数据：np.random.seed(42)后 np.random.normal(520,80,30)；区域B数据：np.random.normal(480,70,30)。请计算并存储：mean_a 区域A平均，mean_b 区域B平均，t_stat 和 p_value（ttest_ind 的结果）。所有数值保留 4 位小数。",
                "import numpy as np\nfrom scipy import stats\nnp.random.seed(42)\nregion_a=np.random.normal(520,80,30)\nregion_b=np.random.normal(480,70,30)\nmean_a=0\nmean_b=0\nt_stat=0\np_value=0",
                "assert abs(mean_a-497.2627)<1\nassert abs(mean_b-471.2056)<1\nassert abs(t_stat-1.3206)<0.01\nassert abs(p_value-0.1910)<0.01",
                ["np.random.seed(42) 设置随机种子使结果可复现", "region_a.mean() 计算A组均值", "stats.ttest_ind(region_a, region_b) 返回(t, p)", "round(x, 4) 保留 4 位小数"],
                "mean_a=round(region_a.mean(),4)\nmean_b=round(region_b.mean(),4)\nt_stat,p_value=stats.ttest_ind(region_a,region_b)\nt_stat=round(t_stat,4)\np_value=round(p_value,4)"),
            ex("ex050202", "改进前平均客单价 300 元。改进后 20 天数据：[325,318,342,308,335,350,312,298,345,320,338,328,315,348,322,305,340,318,332,327]。使用 ttest_1samp 检验是否显著不同。存储：new_mean 新均值，t_stat t统计量，p_value p 值。保留 4 位小数。",
                "import numpy as np\nfrom scipy import stats\nnew=np.array([325,318,342,308,335,350,312,298,345,320,338,328,315,348,322,305,340,318,332,327])\nnew_mean=0\nt_stat=0\np_value=0",
                "assert abs(new_mean-325.55)<0.1\nassert abs(t_stat-9.2143)<0.05\nassert p_value<0.0001",
                ["new.mean() 计算新样本均值", "stats.ttest_1samp(new, 300) 单样本 t 检验", "round(x, 4) 保留小数"],
                "new_mean=round(new.mean(),4)\nt_stat,p_value=stats.ttest_1samp(new,300)\nt_stat=round(t_stat,4)\np_value=round(p_value,4)")
        ], "假设检验是统计推断的核心工具。t 检验比较两组均值是否存在显著差异，p 值帮助判断差异的统计显著性。掌握 ttest_ind / ttest_1samp / ttest_rel 三种检验方法，可以应对大部分商务对比分析场景。"),
    chapter("ch0503", "相关性分析：皮尔逊相关系数",
        ["理解相关系数 r 的含义与取值范围 [-1, 1]", "掌握使用 pandas/numpy 计算相关矩阵", "能够正确解读相关关系并警惕因果谬误", "学会使用散点图可视化相关关系"],
        "在商务分析中，我们经常关心两个变量是否一起变化。例如：广告投入增加时销售额是否也增加？客户的年消费额与订单数正相关吗？产品价格与销量是否负相关？皮尔逊相关系数 r 是衡量两个连续变量线性相关程度的标准指标，取值范围 [-1, 1]。r > 0 表示正相关，r < 0 表示负相关，r 的绝对值越接近 1 相关越强。在 Python 中，可以用 df.corr() 一键计算所有变量两两之间的相关系数矩阵。但需要特别注意：相关并不等于因果。两个变量可能因为第三个变量（如季节因素）而呈现虚假相关。在解读相关系数时，一定要结合业务常识进行判断，必要时通过受控实验（如 A/B 测试）来验证因果关系。",
        [
            cs("cs050301", "计算相关系数与相关矩阵",
                "import pandas as pd\nimport numpy as np\nnp.random.seed(42)\ndata={'广告投入':[5000,8000,12000,15000,18000,22000,25000,30000],'销售额':[45000,62000,85000,98000,125000,150000,175000,210000],'客流量':[1200,1600,2100,2400,2800,3200,3500,4000],'客单价':[37.5,38.8,40.5,40.8,44.6,46.9,50.0,52.5]}\ndf=pd.DataFrame(data)\nprint('广告与销售的相关系数:',round(df['广告投入'].corr(df['销售额']),4))\nprint('广告与客流量的相关系数:',round(df['广告投入'].corr(df['客流量']),4))\nprint('客流量与客单价的相关系数:',round(df['客流量'].corr(df['客单价']),4))\nprint('\\n完整相关矩阵:')\nprint(df.corr().round(3))",
                "df['列A'].corr(df['列B']) 计算两列之间的皮尔逊相关系数 r。df.corr() 一次性返回所有数值列之间的相关矩阵，对角线恒为 1。r 接近 1 表示强正相关，接近 -1 表示强负相关，接近 0 表示无线性相关。"),
            cs("cs050302", "散点图 + 拟合线可视化相关",
                "import matplotlib.pyplot as plt\nimport numpy as np\nnp.random.seed(42)\nad=np.array([5000,8000,12000,15000,18000,22000,25000,30000])\nsales=np.array([45000,62000,85000,98000,125000,150000,175000,210000])\nr=np.corrcoef(ad,sales)[0,1]\nfig,ax=plt.subplots(figsize=(7,5))\nax.scatter(ad,sales,s=80,c='#2563eb',alpha=0.8,edgecolors='white',linewidth=1.5)\nz=np.polyfit(ad,sales,1)\np=np.poly1d(z)\nax.plot(ad,p(ad),'--',color='#dc2626',linewidth=2,label=f'拟合线(r={r:.3f})')\nax.set_title('广告投入 vs 销售额',fontproperties='SimHei',fontsize=14)\nax.set_xlabel('广告投入(元)',fontproperties='SimHei')\nax.set_ylabel('销售额(元)',fontproperties='SimHei')\nax.legend(prop={'family':'SimHei'})\nax.grid(True,alpha=0.3)\nprint('相关系数 r=',round(r,4))\nprint('拟合方程:销售额 =',round(z[0],3),'*广告投入 +',round(z[1],0))",
                "np.corrcoef(x, y)[0,1] 也可以计算相关系数。np.polyfit(x, y, 1) 做一次多项式拟合（线性回归），返回斜率和截距。在散点图上叠加回归线，并将相关系数 r 显示在图例中，图表信息更完整。"),
            cs("cs050303", "相关 vs 因果：识别虚假相关",
                "import pandas as pd\nimport numpy as np\nnp.random.seed(0)\nmonths=list(range(1,25))\n# 模拟：冰淇淋销量随季节波动\nicecream=np.array([120,150,200,280,350,420,450,430,380,300,220,160]*2+[0]*1)[:24]\n# 模拟：溺水事故数量同样在夏季增多\ndrowning=np.array([10,15,25,40,55,70,78,75,60,42,28,18]*2+[0]*1)[:24]\ndf=pd.DataFrame({'月份':months,'冰淇淋':icecream,'溺水':drowning})\nr=df['冰淇淋'].corr(df['溺水'])\nprint('冰淇淋销量与溺水事故的相关系数:',round(r,4))\nprint('\\n看起来高度正相关，但二者并无因果关系！')\nprint('共同的原因是:夏季(气温升高)')\nprint('这就是虚假相关/第三变量问题。')\nprint('实际业务中:促销期间广告投入增加 + 销售额增加，但二者可能都由促销驱动。')",
                "相关系数高并不意味着因果关系。两个变量可能都受第三个隐藏变量影响（如季节、天气、经济周期）。在解读相关系数时，始终要结合业务逻辑问：这种关系合理吗？有什么共同因素在起作用？是否需要做控制变量分析或 A/B 测试来验证因果？这是数据分析中最重要的思维习惯之一。")
        ],
        [
            ex("ex050301", "给定数据：广告投入 [5000,8000,12000,15000,18000,22000,25000,30000]，销售额 [45000,62000,85000,98000,125000,150000,175000,210000]，客流量 [1200,1600,2100,2400,2800,3200,3500,4000]，客单价 [37.5,38.8,40.5,40.8,44.6,46.9,50.0,52.5]。请计算：广告投入与销售额的相关系数 r1；广告投入与客流量的相关系数 r2；客流量与客单价的相关系数 r3；销售额与客单价的相关系数 r4。全部保留 4 位小数。",
                "import pandas as pd\nimport numpy as np\ndata={'广告投入':[5000,8000,12000,15000,18000,22000,25000,30000],'销售额':[45000,62000,85000,98000,125000,150000,175000,210000],'客流量':[1200,1600,2100,2400,2800,3200,3500,4000],'客单价':[37.5,38.8,40.5,40.8,44.6,46.9,50.0,52.5]}\ndf=pd.DataFrame(data)\nr1=0\nr2=0\nr3=0\nr4=0",
                "assert abs(r1-0.9978)<0.001\nassert abs(r2-0.9989)<0.001\nassert abs(r3-0.9860)<0.005\nassert abs(r4-0.9908)<0.005",
                ["df['列A'].corr(df['列B']) 计算两列相关系数", "结果可能为正/负，取值 [-1,1]", "round(r, 4) 保留 4 位小数"],
                "r1=round(df['广告投入'].corr(df['销售额']),4)\nr2=round(df['广告投入'].corr(df['客流量']),4)\nr3=round(df['客流量'].corr(df['客单价']),4)\nr4=round(df['销售额'].corr(df['客单价']),4)")
        ], "皮尔逊相关系数 r 衡量两个连续变量的线性相关强度。df.corr() 可快速计算所有变量间的相关矩阵。但必须牢记：相关 ≠ 因果，虚假相关在商务数据中非常常见，需要结合业务常识和实验设计进行验证。"),
    chapter("ch0504", "简单线性回归与预测",
        ["理解简单线性回归 y = a + bx 的含义", "掌握使用 numpy.polyfit 进行线性拟合", "能够解读回归系数 R² 的含义", "学会基于回归模型进行业务预测"],
        "相关系数告诉我们两个变量是否相关，但不能告诉我们一个变量变化时另一个变量会变化多少。线性回归则可以建立这种数量关系。简单线性回归假设 y = a + b * x，其中 b 是斜率（x 每变化 1 单位，y 平均变化 b 单位），a 是截距。在 NumPy 中可以用 np.polyfit(x, y, 1) 快速拟合。拟合后需要评估模型质量，R²（决定系数）是衡量回归效果的标准指标，取值范围 [0, 1]，越接近 1 说明模型解释的变异越多，预测效果越好。线性回归在商务预测中非常实用：你可以建立'广告投入 → 销售额'的回归方程，用于预测不同预算水平下的预期销售额，帮助管理层制定营销预算。但使用回归模型时需要注意：预测不要超出训练数据范围太多（外推风险），并且始终要结合业务常识解读结果。",
        [
            cs("cs050401", "广告投入对销售额的回归预测",
                "import numpy as np\nad=np.array([5000,8000,12000,15000,18000,22000,25000,30000])\nsales=np.array([45000,62000,85000,98000,125000,150000,175000,210000])\ncoef=np.polyfit(ad,sales,1)\nslope=coef[0]\nintercept=coef[1]\nprint('回归方程: 销售额 =',round(slope,3),'* 广告投入 +',round(intercept,0))\nprint('含义:每多投入 1 元广告，销售额平均增加',round(slope,2),'元')\n# 预测: 投入 20000 元广告\npred_20k=slope*20000+intercept\nprint('\\n广告投入 20000 元的预测销售额:',int(pred_20k))\npred_35k=slope*35000+intercept\nprint('广告投入 35000 元的预测销售额:',int(pred_35k))\n# 计算 R²\ny_pred=slope*ad+intercept\nss_res=((sales-y_pred)**2).sum()\nss_tot=((sales-sales.mean())**2).sum()\nr_squared=1-ss_res/ss_tot\nprint('\\nR² =',round(r_squared,4))",
                "np.polyfit(x, y, 1) 返回 [斜率, 截距]。y = slope*x + intercept 即回归方程。slope=7 意味着每增加 1 元广告投入，销售额平均增加 7 元。R² 计算公式为 1 - (残差平方和/总平方和)，衡量 y 的变异中能被 x 解释的比例。"),
            cs("cs050402", "可视化回归线与残差",
                "import matplotlib.pyplot as plt\nimport numpy as np\nad=np.array([5000,8000,12000,15000,18000,22000,25000,30000])\nsales=np.array([45000,62000,85000,98000,125000,150000,175000,210000])\nz=np.polyfit(ad,sales,1)\np=np.poly1d(z)\ny_pred=p(ad)\nfig,(ax1,ax2)=plt.subplots(1,2,figsize=(12,4))\nax1.scatter(ad,sales,s=80,c='#2563eb',alpha=0.8)\nax1.plot(ad,y_pred,'--r',linewidth=2)\nax1.set_title('广告投入 vs 销售额 + 回归线',fontproperties='SimHei')\nax1.set_xlabel('广告投入(元)',fontproperties='SimHei')\nax1.set_ylabel('销售额(元)',fontproperties='SimHei')\nax1.grid(True,alpha=0.3)\nresiduals=sales-y_pred\nax2.scatter(ad,residuals,s=60,c='#f59e0b',alpha=0.8)\nax2.axhline(0,color='gray',linestyle='--')\nax2.set_title('残差图',fontproperties='SimHei')\nax2.set_xlabel('广告投入',fontproperties='SimHei')\nax2.grid(True,alpha=0.3)\nprint('残差:',np.round(residuals,0).tolist())\nprint('平均残差绝对值:',int(abs(residuals).mean()))",
                "残差 = 实际值 - 预测值。残差图是检验回归假设的重要工具：如果残差随机分布在 0 线两侧，没有明显模式，说明线性假设是合理的。如果残差有某种模式（如弯曲、漏斗形），说明模型需要改进。这是专业分析的重要环节。"),
            cs("cs050403", "月度趋势预测：季节性线性回归",
                "import numpy as np\nmonths=np.arange(1,13)\nsales_by_month=np.array([125,118,142,156,168,185,195,188,172,165,178,200])\n# 拟合线性趋势\nz=np.polyfit(months,sales_by_month,1)\np=np.poly1d(z)\nprint('趋势线: y =',round(z[0],2),'*月份 +',round(z[1],2))\nprint('\\n各月预测值:',p(months).round(0).tolist())\nprint('各月实际值:',sales_by_month.tolist())\nprint('\\n下一年1月预测 (month=13):',int(p(13)))\nprint('下一年6月预测 (month=18):',int(p(18)))\n# 识别高于/低于趋势的月份\ndiff=sales_by_month-p(months)\nprint('\\n高于趋势(>0)或低于趋势(<0):')\nfor m,d in enumerate(diff,1):\n    direction='高于' if d>0 else '低于'\n    print(f'{m}月: {direction} 平均 {int(abs(d))} 单位')",
                "对于有时间序列特征的数据，可以将时间作为 x 变量（如月份编号），将销售额作为 y 变量进行回归。斜率 z[0] > 0 表示销售在增长。通过将未来月份代入（如 month=13 代表下一年1月），可以做短期预测。残差符号可以判断哪些月份销售表现超出/低于趋势平均线，这对于识别旺季淡季和异常月份非常有用。")
        ],
        [
            ex("ex050401", "广告投入 ad=[5000,8000,12000,15000,18000,22000,25000,30000]（元），对应销售额 sales=[45000,62000,85000,98000,125000,150000,175000,210000]（元）。请用 np.polyfit(ad, sales, 1) 进行线性回归，得到：slope 斜率（保留 3 位小数），intercept 截距（整数），R²（保留 4 位小数）。并预测：pred_20k = 投入 20000 元时的预测销售额（整数），pred_40k = 投入 40000 元时的预测销售额（整数）。",
                "import numpy as np\nad=np.array([5000,8000,12000,15000,18000,22000,25000,30000])\nsales=np.array([45000,62000,85000,98000,125000,150000,175000,210000])\nslope=0\nintercept=0\nr_squared=0\npred_20k=0\npred_40k=0",
                "assert abs(slope-6.971)<0.01\nassert abs(intercept-7711)<50\nassert abs(r_squared-0.9956)<0.001\nassert abs(pred_20k-147133)<500\nassert abs(pred_40k-286553)<500",
                ["z=np.polyfit(ad,sales,1)；slope=z[0]，intercept=z[1]", "y_pred = slope*ad + intercept 计算预测值", "R² = 1 - ((sales-y_pred)**2).sum() / ((sales-sales.mean())**2).sum()", "pred_20k = slope*20000 + intercept，int() 取整"],
                "z=np.polyfit(ad,sales,1)\nslope=round(z[0],3)\nintercept=int(z[1])\ny_pred=z[0]*ad+z[1]\nss_res=((sales-y_pred)**2).sum()\nss_tot=((sales-sales.mean())**2).sum()\nr_squared=round(1-ss_res/ss_tot,4)\npred_20k=int(z[0]*20000+z[1])\npred_40k=int(z[0]*40000+z[1])")
        ], "简单线性回归 y = a + b*x 是最基础的预测工具。斜率 b 是边际效应（每单位 x 变化带来的 y 变化），截距 a 是 x=0 时的基线值。R² 衡量模型拟合程度。回归模型在广告预测、销售预测、定价分析等场景中极为实用，但要注意外推风险和相关≠因果的限制。")
]}

with open("assets/data/u5.json", "w", encoding="utf-8") as f:
    json.dump(UNIT5, f, ensure_ascii=False, indent=2)
print("U5 章数:", len(UNIT5["chapters"]))
