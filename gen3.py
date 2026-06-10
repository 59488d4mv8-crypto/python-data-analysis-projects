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

# ================== U3: Pandas 基础 (4章) ==================
UNIT3 = {"unitId": "u03", "title": "Pandas 基础", "chapters": [
    chapter("ch0301", "Series 与 DataFrame",
        ["了解 Pandas 的核心数据结构", "掌握从字典/列表创建 DataFrame", "掌握从 Series 创建与索引", "学会 head/shape/columns/index 浏览方法"],
        "Pandas 是基于 NumPy 构建的数据分析库，提供 Series（一维带标签数组）和 DataFrame（二维带标签表格）两种核心结构。DataFrame 可以想象成 Excel 表格，每列是一个 Series，每行有行索引，每列有列名。与 NumPy 数组不同，DataFrame 的每列可以存储不同类型的数据（文本、数字、日期等），非常适合真实世界的销售报表、客户信息等混合类型数据。",
        [
            cs("cs030101", "从字典创建 DataFrame",
                "import pandas as pd\nsales={'月份':['1月','2月','3月','4月'],'产品A':[32000,28500,41200,35800],'产品B':[18000,22300,19500,25600]}\ndf=pd.DataFrame(sales)\nprint(df)\nprint('形状:',df.shape)\nprint('列名:',df.columns.tolist())",
                "pd.DataFrame(字典) 将 Python 字典转为 DataFrame。字典的每个键成为一列，列表值按顺序成为各行数据。shape 返回(行数, 列数)。"),
            cs("cs030102", "Series 的创建与方法",
                "import pandas as pd\ns=pd.Series([32000,28500,41200,35800,49100],index=['1月','2月','3月','4月','5月'],name='产品A销售额')\nprint(s)\nprint('前2行:')\nprint(s.head(2))\nprint('总和:',s.sum(),'均值:',int(s.mean()))\nprint('最大月份:',s.idxmax(),'值:',s.max())",
                "pd.Series(数据, index=索引, name=名称) 创建一维 Series。head(n) 浏览前 n 行。sum/mean/max/idxmax 提供聚合统计。"),
            cs("cs030103", "列访问与新增列",
                "import pandas as pd\ndata={'产品':['A','B','C','D'],'单价':[299,1599,899,499],'销量':[120,85,156,78]}\ndf=pd.DataFrame(data)\ndf['销售额']=df['单价']*df['销量']\ndf['利润率估算']=df['销售额']*0.25\nprint(df)\nprint('\\n仅产品和销售额:')\nprint(df[['产品','销售额']])",
                "df['列名'] 访问单列。df[['列1','列2']] 访问多列。df['新列']=... 基于已有列计算新增列。向量化运算比 for 循环快得多。")
        ],
        [
            ex("ex030101", "创建产品销售 DataFrame：列名为 ['产品名称','单价','销量']，5行产品数据为：产品A/299/88，产品B/1599/145，产品C/3999/210，产品D/899/380，产品E/2599/120。然后新增一列 销售额 = 单价 * 销量，存储在变量 df 中。",
                "import pandas as pd\ndf=None",
                "import pandas as pd\nassert isinstance(df,pd.DataFrame)\nassert list(df.columns)==['产品名称','单价','销量','销售额']\nassert df.shape==(5,4)\nassert df['销售额'].tolist()==[26312,231855,839790,341620,311880]\nassert df['单价'].tolist()==[299,1599,3999,899,2599]",
                ["先构造字典：键是列名，值是数据列表", "pd.DataFrame(字典) 创建 DataFrame", "df['销售额']=df['单价']*df['销量'] 新增列"],
                "data={'产品名称':['产品A','产品B','产品C','产品D','产品E'],'单价':[299,1599,3999,899,2599],'销量':[88,145,210,380,120]}\ndf=pd.DataFrame(data)\ndf['销售额']=df['单价']*df['销量']"),
            ex("ex030102", "创建 Series sales_series：数据 [48500,39200,42800,31500,52800,61200]，索引 ['1月','2月','3月','4月','5月','6月']，名称 '华东月销售额'。然后计算：total=总和，avg=平均值，top_month=最大值对应的索引月份。",
                "import pandas as pd\nsales_series=None\ntotal=0\navg=0\ntop_month=''",
                "import pandas as pd\nassert isinstance(sales_series,pd.Series)\nassert sales_series.tolist()==[48500,39200,42800,31500,52800,61200]\nassert list(sales_series.index)==['1月','2月','3月','4月','5月','6月']\nassert total==276000\nassert abs(avg-46000.0)<0.01\nassert top_month=='6月'",
                ["pd.Series(数据列表, index=索引列表, name=名称)", "sum() 返回总和", "mean() 返回均值", "idxmax() 返回最大值对应的索引标签"],
                "sales_series=pd.Series([48500,39200,42800,31500,52800,61200],index=['1月','2月','3月','4月','5月','6月'],name='华东月销售额')\ntotal=sales_series.sum()\navg=sales_series.mean()\ntop_month=sales_series.idxmax()")
        ], "Series 和 DataFrame 是 Pandas 两大核心结构。从字典构造 DataFrame、新增计算列、浏览数据是数据分析的起点。"),
    chapter("ch0302", "读取 CSV 与数据浏览",
        ["掌握从 CSV/文本创建 DataFrame", "学会使用 head()/tail()/sample() 浏览数据", "掌握 info()/describe()/dtypes 检查数据结构", "了解数据类型检查在清洗中的重要性"],
        "在真实的商务数据分析项目中，原始数据往往存储在 CSV、Excel 或数据库中。CSV 是最常见的数据交换格式。Pandas 提供 pd.read_csv() 函数可以一键加载 CSV 文件。数据加载后，第一步不是立即开始分析，而是对数据进行快速浏览检查以确认数据质量。养成先查看数据再做分析的习惯，可以避免很多由于数据类型问题、缺失值问题等导致的错误分析结论。",
        [
            cs("cs030201", "从文本构造 CSV 并读取",
                "import pandas as pd\nimport io\ntext='''产品,单价,销量,上架日期\nA,299,120,2025-01-15\nB,1599,145,2025-02-10\nC,3999,210,2025-01-28\nD,899,380,2025-03-05\nE,2599,256,2025-02-22\n'''\ndf=pd.read_csv(io.StringIO(text))\nprint('形状:',df.shape)\nprint('前3行:')\nprint(df.head(3))\nprint('后2行:')\nprint(df.tail(2))",
                "pd.read_csv() 从文件读取 CSV。通过 io.StringIO 可以把字符串当作文件对象使用，便于演示和测试。head(n)/tail(n) 查看前 n 行或后 n 行。"),
            cs("cs030202", "info() 检查数据结构",
                "import pandas as pd\nimport io\ntext='''订单号,客户,产品,数量,单价,金额\nORD001,张小明,笔记本,1,4999,4999\nORD002,王丽,平板,2,2599,5198\nORD003,李华,手机,1,3999,3999\nORD004,赵敏,耳机,3,899,2697\nORD005,刘强,手表,2,1599,3198\n'''\ndf=pd.read_csv(io.StringIO(text))\nprint(df.info())\nprint('\\n列名:',df.columns.tolist())\nprint('\\n数据类型:')\nprint(df.dtypes)",
                "info() 打印每列的名称、非空值数量和数据类型。object 通常代表字符串，int64 是整数，float64 是浮点数，datetime64 是日期时间。检查数据类型是清洗的第一步。"),
            cs("cs030203", "describe() 生成统计摘要",
                "import pandas as pd\nimport io\ntext='''区域,订单数,总销售额,客户数,平均客单价\n华东,1250,589200,856,688.54\n华北,980,412300,645,576.34\n华南,1520,726800,1023,711.80\n西南,680,285400,412,478.65\n西北,320,138600,198,520.75\n东北,540,218900,367,607.63\n'''\ndf=pd.read_csv(io.StringIO(text))\nprint('数值列摘要:')\nprint(df.describe())\nprint('\\n订单数中位数:',df['订单数'].median())\nprint('销售额总和:',df['总销售额'].sum())\nprint('平均客单价标准差:',round(df['平均客单价'].std(),2))",
                "describe() 默认对所有数值列生成统计摘要，包括 count、mean、std、min、25%/50%/75% 分位数、max。可以对单列单独调用 median()/sum()/std() 等方法。")
        ],
        [
            ex("ex030201", "构造包含 6 行数据的 DataFrame df：列名为 日期、访客数、下单数、支付金额。数据：2025-06-01 访客1520 下单185 支付28500；6月2日 1780/210/32800；6月3日 1340/156/21200；6月4日 2100/298/45600；6月5日 1950/265/39400；6月6日 2300/340/52100。然后提取前 3 行存入 df_head3。",
                "import pandas as pd\nimport io\ntext='''日期,访客数,下单数,支付金额\n'''\ndf=pd.read_csv(io.StringIO(text))\ndf_head3=None",
                "import pandas as pd\nassert isinstance(df,pd.DataFrame)\nassert df.shape==(6,4)\nassert list(df.columns)==['日期','访客数','下单数','支付金额']\nassert df['访客数'].tolist()==[1520,1780,1340,2100,1950,2300]\nassert df['支付金额'].tolist()==[28500,32800,21200,45600,39400,52100]\nassert isinstance(df_head3,pd.DataFrame) and df_head3.shape==(3,4)",
                ["CSV 文本首行是列名，用逗号分隔", "每行数据对应一条记录，逗号分隔", "pd.read_csv(io.StringIO(text)) 读取", "df.head(3) 获取前 3 行"],
                "text='''日期,访客数,下单数,支付金额\n2025-06-01,1520,185,28500\n2025-06-02,1780,210,32800\n2025-06-03,1340,156,21200\n2025-06-04,2100,298,45600\n2025-06-05,1950,265,39400\n2025-06-06,2300,340,52100\n'''\ndf=pd.read_csv(io.StringIO(text))\ndf_head3=df.head(3)"),
            ex("ex030202", "基于上一题的 df（6行4列），请计算：shape_result = df.shape 元组；total_pay = 支付金额列总和；avg_orders = 下单数平均值；max_visitors = 访客数最大值。",
                "import pandas as pd\nimport io\ntext='''日期,访客数,下单数,支付金额\n2025-06-01,1520,185,28500\n2025-06-02,1780,210,32800\n2025-06-03,1340,156,21200\n2025-06-04,2100,298,45600\n2025-06-05,1950,265,39400\n2025-06-06,2300,340,52100\n'''\ndf=pd.read_csv(io.StringIO(text))\nshape_result=None\ntotal_pay=0\navg_orders=0\nmax_visitors=0",
                "assert shape_result==(6,4)\nassert total_pay==219600\nassert abs(avg_orders-242.333)<0.01\nassert max_visitors==2300",
                ["df.shape 返回 (行数,列数) 元组", "df['支付金额'].sum() 求和", "df['下单数'].mean() 求平均", "df['访客数'].max() 求最大值"],
                "shape_result=df.shape\ntotal_pay=df['支付金额'].sum()\navg_orders=df['下单数'].mean()\nmax_visitors=df['访客数'].max()")
        ], "读取 CSV 是实际分析的第一步。养成先用 head/info/describe 浏览和检查数据的习惯，可以避免大量数据质量问题导致的错误分析。"),
    chapter("ch0303", "选择列与筛选行",
        ["掌握使用方括号选择单列和多列", "掌握 df.loc[] 按标签选择", "掌握 df.iloc[] 按位置索引选择", "掌握布尔索引按条件筛选行", "能够组合多条件完成复杂筛选"],
        "在实际分析工作中，我们很少对整张表做操作，更多时候需要从数据中提取感兴趣的子集。例如：只看华东区域的销售数据，只分析销售额超过 10000 的订单，只关注 VIP 客户。Pandas 提供多种灵活的数据选择方法：df['列名'] 选择单列；df[['列1','列2']] 选择多列；布尔索引通过条件表达式筛选满足条件的行；df.loc[行,列] 按标签选择；df.iloc[行,列] 按位置索引选择。将这些方法组合使用，可以从数万行数据中精准提取需要的子集。",
        [
            cs("cs030301", "选择列与基础布尔筛选",
                "import pandas as pd\nimport io\ntext='''产品,区域,单价,销量,销售额\n笔记本,华东,4999,88,439912\n平板,华北,2599,145,376855\n手机,华南,3999,210,839790\n耳机,华东,899,380,341620\n手表,华北,1599,256,409344\n相机,华南,5999,65,389935\n'''\ndf=pd.read_csv(io.StringIO(text))\nprint('产品和销售额两列:')\nprint(df[['产品','销售额']])\nprint('\\n销售额>400000 的行:')\nprint(df[df['销售额']>400000])\nprint('\\n华东区域的订单:')\nprint(df[df['区域']=='华东'])",
                "df[['列1','列2']]（两层方括号）选择多列。布尔索引 df[条件] 筛选满足条件的行。条件表达式生成布尔 Series。"),
            cs("cs030302", "df.loc 按标签选择行列",
                "import pandas as pd\nimport io\ntext='''月份,华东,华北,华南,西南\n1月,125,98,112,68\n2月,118,105,128,72\n3月,142,112,135,81\n4月,156,128,142,89\n5月,168,135,156,95\n6月,185,148,172,108\n'''\ndf=pd.read_csv(io.StringIO(text),index_col='月份')\nprint('3月这一行:')\nprint(df.loc['3月'])\nprint('\\n2月到4月、华东和华南两列:')\nprint(df.loc['2月':'4月',['华东','华南']])\nprint('\\n华东>150 的月份:')\nprint(df.loc[df['华东']>150,:])",
                "df.loc[行标签, 列标签] 是 Pandas 推荐的选择方式。行标签可以是单个值、切片（包含两端，与 Python 原生不同）、列表或布尔条件。set_index 或 read_csv 的 index_col 参数可以设置索引列。"),
            cs("cs030303", "df.iloc 按位置与多条件筛选",
                "import pandas as pd\nimport io\ntext='''客户名,城市,会员等级,年消费,订单数\n张小明,上海,钻石,58200,42\n王丽,北京,金卡,28500,25\n李华,深圳,钻石,72800,58\n赵敏,杭州,银卡,12600,15\n刘强,上海,金卡,35200,32\n陈静,北京,钻石,65400,48\n周涛,深圳,普通,5800,8\n'''\ndf=pd.read_csv(io.StringIO(text))\nprint('前3行前2列(位置索引):')\nprint(df.iloc[:3,:2])\nprint('\\n上海且年消费>30000:')\nprint(df[(df['城市']=='上海')&(df['年消费']>30000)])\nprint('\\n钻石或订单数>40:')\nprint(df[(df['会员等级']=='钻石')|(df['订单数']>40)])",
                "df.iloc[行位置, 列位置] 使用从 0 开始的整数索引，行为与 Python 列表切片一致（左闭右开）。多条件组合：& 同时满足，| 满足其一。每个独立条件必须用圆括号包裹。")
        ],
        [
            ex("ex030301", "读取产品销售数据到 DataFrame df（6行：产品/区域/单价/销量/销售额，数据：笔记本/华东/4999/88/439912，平板/华北/2599/145/376855，手机/华南/3999/210/839790，耳机/华东/899/380/341620，手表/华北/1599/256/409344，相机/华南/5999/65/389935）。然后：选择产品和销售额两列存入 df_cols；筛选销售额大于 380000 的行存入 df_high；筛选区域为华东的行存入 df_east。",
                "import pandas as pd\nimport io\ntext='''产品,区域,单价,销量,销售额\n笔记本,华东,4999,88,439912\n平板,华北,2599,145,376855\n手机,华南,3999,210,839790\n耳机,华东,899,380,341620\n手表,华北,1599,256,409344\n相机,华南,5999,65,389935\n'''\ndf=pd.read_csv(io.StringIO(text))\ndf_cols=None\ndf_high=None\ndf_east=None",
                "assert isinstance(df_cols,pd.DataFrame)\nassert list(df_cols.columns)==['产品','销售额']\nassert df_cols.shape==(6,2)\nassert isinstance(df_high,pd.DataFrame) and df_high.shape[0]==3\nassert '手机' in df_high['产品'].tolist()\nassert isinstance(df_east,pd.DataFrame)\nassert df_east.shape[0]==2\nassert df_east['产品'].tolist()==['笔记本','耳机']",
                ["选择多列使用 df[['产品','销售额']] 注意两层方括号", "筛选：df[df['销售额']>380000]", "文本匹配：df[df['区域']=='华东']"],
                "df_cols=df[['产品','销售额']]\ndf_high=df[df['销售额']>380000]\ndf_east=df[df['区域']=='华东']"),
            ex("ex030302", "DataFrame df 客户数据：客户名/城市/会员等级/年消费/订单数，数据：张小明/上海/钻石/58200/42，王丽/北京/金卡/28500/25，李华/深圳/钻石/72800/58，赵敏/杭州/银卡/12600/15，刘强/上海/金卡/35200/32，陈静/北京/钻石/65400/48，周涛/深圳/普通/5800/8。请：筛选上海客户且年消费>30000 存入 shanghai_high；筛选钻石会员或订单数>40 存入 vip_many；仅从 vip_many 选择客户名、会员等级、订单数三列。",
                "import pandas as pd\nimport io\ntext='''客户名,城市,会员等级,年消费,订单数\n张小明,上海,钻石,58200,42\n王丽,北京,金卡,28500,25\n李华,深圳,钻石,72800,58\n赵敏,杭州,银卡,12600,15\n刘强,上海,金卡,35200,32\n陈静,北京,钻石,65400,48\n周涛,深圳,普通,5800,8\n'''\ndf=pd.read_csv(io.StringIO(text))\nshanghai_high=None\nvip_many=None",
                "assert shanghai_high.shape[0]==2 and '张小明' in shanghai_high['客户名'].tolist()\nassert vip_many.shape[0]==4\nassert sorted(vip_many['客户名'].tolist())==sorted(['张小明','李华','陈静','刘强'])",
                ["两个条件用 & 连接，每个条件必须用 () 包裹：(df['城市']=='上海')&(df['年消费']>30000)", "或条件用 |：(df['会员等级']=='钻石')|(df['订单数']>40)", "可以先筛选再选列，也可以在 loc 中同时指定"],
                "shanghai_high=df[(df['城市']=='上海')&(df['年消费']>30000)]\nvip_many=df[(df['会员等级']=='钻石')|(df['订单数']>40)]\nvip_many=vip_many[['客户名','会员等级','订单数']]")
        ], "灵活使用列选择、布尔索引、loc/iloc 可以精准地从大量数据中提取所需子集，这是销售分析、客户细分、市场筛选等场景的基础操作。"),
    chapter("ch0304", "排序、分组聚合与数据合并",
        ["掌握 sort_values 排序数据", "掌握 groupby + agg 进行分组统计", "学会 value_counts / unique 探索分类列", "能够使用 merge/concat 合并数据"],
        "销售分析中最常见的需求之一是：按区域分组计算总销售额、按产品类别排序找出 TOP 产品、按月份汇总对比。Pandas 的 groupby 功能强大，它会先按某列或多列的值将数据分成多个组，然后对每组分别执行聚合函数（sum/mean/count/min/max 等），最后合并结果。sort_values 可以按一列或多列排序。value_counts() 可以快速统计某个分类列的各个值出现多少次，非常适合探索客户等级分布、区域分布等。merge/concat 可以将多张表合并，相当于 SQL 的 JOIN 或 UNION。",
        [
            cs("cs030401", "排序 sort_values",
                "import pandas as pd\nimport io\ntext='''产品,区域,单价,销量,销售额\n笔记本,华东,4999,88,439912\n平板,华北,2599,145,376855\n手机,华南,3999,210,839790\n耳机,华东,899,380,341620\n手表,华北,1599,256,409344\n相机,华南,5999,65,389935\n'''\ndf=pd.read_csv(io.StringIO(text))\nprint('按销售额降序:')\nprint(df.sort_values('销售额',ascending=False))\nprint('\\n按区域升序再按销量降序:')\nprint(df.sort_values(['区域','销量'],ascending=[True,False]))",
                "df.sort_values('列名', ascending=False) 按某列降序排序。传入列表可按多列排序，同时给出对应 ascending 列表决定每列升序(True)或降序(False)。"),
            cs("cs030402", "groupby 分组聚合",
                "import pandas as pd\nimport io\ntext='''产品,区域,单价,销量,销售额\n笔记本,华东,4999,88,439912\n平板,华北,2599,145,376855\n手机,华南,3999,210,839790\n耳机,华东,899,380,341620\n手表,华北,1599,256,409344\n相机,华南,5999,65,389935\n'''\ndf=pd.read_csv(io.StringIO(text))\nprint('按区域汇总:')\nprint(df.groupby('区域')[['销售额','销量']].sum())\nprint('\\n每个区域的平均客单价和订单数:')\nprint(df.groupby('区域').agg(总销售额=('销售额','sum'),平均单价=('单价','mean'),产品数=('产品','count')))\nprint('\\n各会员等级分布:')\nprint(pd.Series(['钻石','金卡','银卡','钻石','金卡','普通','钻石']).value_counts())",
                "df.groupby('分组列')[['列1','列2']].sum() 按分组列分组后对数值列求和。agg() 可以同时对不同列应用不同聚合函数，使用 named aggregation 语法 新列名=('原列名','函数名') 更清晰。value_counts() 统计分类列的频次。"),
            cs("cs030403", "合并 merge/concat",
                "import pandas as pd\ndf1=pd.DataFrame({'月份':['1月','2月','3月'],'华东':[125,118,142],'华北':[98,105,112]})\ndf2=pd.DataFrame({'月份':['4月','5月','6月'],'华东':[156,168,185],'华北':[128,135,148]})\nprint('纵向拼接(行拼接):')\nprint(pd.concat([df1,df2],ignore_index=True))\ndf_a=pd.DataFrame({'产品':['A','B','C'],'单价':[299,599,899]})\ndf_b=pd.DataFrame({'产品':['A','B','C'],'销量':[120,85,156]})\nprint('\\n横向合并(按产品名匹配):')\nprint(pd.merge(df_a,df_b,on='产品'))",
                "pd.concat([df1,df2],ignore_index=True) 纵向拼接多行（列名相同）。pd.merge(left,right,on='键') 按键列横向合并两表（类似 SQL JOIN）。ignore_index=True 让拼接后索引重置。")
        ],
        [
            ex("ex030401", "DataFrame df 的产品销售数据与前面练习相同（6行5列）。请：按销售额降序排序后存入 df_sorted；按区域对销售额和销量求和存入 region_summary（要求索引为区域，包含销售额和销量两列）；筛选 TOP3 销售额产品存入 df_top3（只保留产品和销售额两列）。",
                "import pandas as pd\nimport io\ntext='''产品,区域,单价,销量,销售额\n笔记本,华东,4999,88,439912\n平板,华北,2599,145,376855\n手机,华南,3999,210,839790\n耳机,华东,899,380,341620\n手表,华北,1599,256,409344\n相机,华南,5999,65,389935\n'''\ndf=pd.read_csv(io.StringIO(text))\ndf_sorted=None\nregion_summary=None\ndf_top3=None",
                "assert df_sorted.iloc[0]['销售额']==839790\nassert df_sorted.iloc[-1]['销售额']==341620\nassert region_summary.loc['华东','销售额']==781532\nassert region_summary.loc['华北','销量']==401\nassert df_top3.shape==(3,2)\nassert df_top3['销售额'].tolist()==sorted(df_top3['销售额'].tolist(),reverse=True)",
                ["df.sort_values('销售额', ascending=False)", "df.groupby('区域')[['销售额','销量']].sum()", "先按销售额降序，再取前 3 行和两列"],
                "df_sorted=df.sort_values('销售额',ascending=False)\nregion_summary=df.groupby('区域')[['销售额','销量']].sum()\ndf_top3=df_sorted[['产品','销售额']].head(3)"),
            ex("ex030402", "有两张表：df_a 为产品信息（产品/单价：A/299，B/599，C/899，D/1299）；df_b 为销售信息（产品/销量/区域：A/120/华东，B/85/华北，C/156/华南，D/78/华东）。请：使用 pd.concat 纵向演示（不必存）；以产品为键合并 df_a 与 df_b 存入 merged；然后计算 merged 中每个产品的销售额存入 merged['销售额']；最后按区域分组计算总销售额存入 region_total。",
                "import pandas as pd\ndf_a=pd.DataFrame({'产品':['A','B','C','D'],'单价':[299,599,899,1299]})\ndf_b=pd.DataFrame({'产品':['A','B','C','D'],'销量':[120,85,156,78],'区域':['华东','华北','华南','华东']})\nmerged=None\nregion_total=None",
                "assert list(merged.columns)==['产品','单价','销量','区域','销售额']\nassert merged['销售额'].tolist()==[35880,50915,140244,101322]\nassert region_total.loc['华东']==137202\nassert region_total.loc['华南']==140244\nassert region_total.loc['华北']==50915",
                ["pd.merge(df_a, df_b, on='产品') 合并", "merged['销售额']=merged['单价']*merged['销量']", "按区域分组，对销售额求和"],
                "merged=pd.merge(df_a,df_b,on='产品')\nmerged['销售额']=merged['单价']*merged['销量']\nregion_total=merged.groupby('区域')['销售额'].sum()")
        ], "排序、分组聚合、数据合并是 Pandas 进行商务数据分析的核心操作。掌握 groupby/agg/sort_values/merge 后，你就能完成绝大多数销售报表汇总、区域对比、TOP 产品分析等实际业务需求。")
]}

with open("assets/data/u3.json", "w", encoding="utf-8") as f:
    json.dump(UNIT3, f, ensure_ascii=False, indent=2)
print("U3 章数:", len(UNIT3["chapters"]))
