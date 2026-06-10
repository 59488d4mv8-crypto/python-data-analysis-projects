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

# ================== U2: NumPy 数值计算 (3章) ==================
UNIT2 = {"unitId": "u02", "title": "NumPy 数值计算", "chapters": [
    chapter("ch0201", "ndarray 基础",
        ["了解 NumPy 在数据分析中的定位", "掌握从列表创建 ndarray", "掌握 shape/dtype/size 属性", "学会 zeros/ones/arange/linspace"],
        "NumPy 是 Python 数值计算的基础库，提供高性能多维数组 ndarray。Pandas 等库都建立在 NumPy 之上。ndarray 的内存占用小、运算速度快，非常适合处理销售数据矩阵、用户特征向量等大规模数值数据。",
        [
            cs("cs020101", "从列表创建数组",
                "import numpy as np\nmonthly=[32000,28500,41200,35800,49100]\narr=np.array(monthly)\nprint(arr, arr.shape, arr.dtype)",
                "np.array() 将 Python 列表转为 ndarray。shape 返回形状，dtype 返回元素类型。"),
            cs("cs020102", "zeros/ones 与二维数组",
                "import numpy as np\nz=np.zeros((3,4),dtype=int)\nprint(z)\nprint('形状:',z.shape)\nprint('元素数:',z.size)",
                "np.zeros((行,列)) 创建全零数组，np.ones 创建全1数组。传入元组指定形状。"),
            cs("cs020103", "向量化运算",
                "import numpy as np\nsales=np.array([120,85,156,78,203,145])\nprices=np.array([299,1599,899,499,2599,1299])\nrev=sales*prices\nprint('各产品销售:',rev)\nprint('总销售:',rev.sum())\nprint('平均:',int(rev.mean()))",
                "NumPy 的核心优势是向量化运算。* 直接对两数组按元素相乘，不需要手写 for 循环。sum()、mean() 等方法快速聚合。")
        ],
        [
            ex("ex020101", "创建 NumPy 二维数组 sales_data：3行产品 x 4列季度。数据：[32000,28500,41200,35800]、[18000,22300,19500,25600]、[45000,48200,52300,55800]。打印数组；打印 shape；计算所有数据总和 total_sum；计算每行（每产品年度）总和存入 product_yearly。",
                "import numpy as np\nsales_data=None\ntotal_sum=0\nproduct_yearly=None",
                "import numpy as np\nassert isinstance(sales_data,np.ndarray)\nassert sales_data.shape==(3,4)\nassert sales_data.tolist()==[[32000,28500,41200,35800],[18000,22300,19500,25600],[45000,48200,52300,55800]]\nassert total_sum==398700\nassert product_yearly.tolist()==[137500,85400,201800]",
                ["np.array(嵌套列表) 创建二维数组", "shape 属性获取维度", "sum() 不指定轴返回总总和", "sum(axis=1) 按行求和"],
                "sales_data=np.array([[32000,28500,41200,35800],[18000,22300,19500,25600],[45000,48200,52300,55800]])\ntotal_sum=sales_data.sum()\nproduct_yearly=sales_data.sum(axis=1)"),
            ex("ex020102", "prices=np.array([299,599,899,1299,1599,2599])，quantities=np.array([380,245,189,156,98,67])。计算每个商品销售额存入 revenues；计算总销售额 total_rev；计算平均销售额 avg_rev（整数）；创建折后价数组 discounted_prices = 价格 * 0.8。",
                "import numpy as np\nprices=np.array([299,599,899,1299,1599,2599])\nquantities=np.array([380,245,189,156,98,67])\nrevenues=None\ntotal_rev=0\navg_rev=0\ndiscounted_prices=None",
                "assert revenues.tolist()==[113620,146755,170911,202644,156702,174133]\nassert total_rev==964765\nassert abs(avg_rev-160794)<1\nassert np.allclose(discounted_prices,prices*0.8)",
                ["两数组直接 * 相乘即按元素相乘", "sum() 求和，mean() 求平均", "数组与标量运算自动广播到每个元素"],
                "revenues=prices*quantities\ntotal_rev=revenues.sum()\navg_rev=int(revenues.mean())\ndiscounted_prices=prices*0.8")
        ], "ndarray 是 NumPy 核心。向量化运算比 Python 原生循环快得多，为 Pandas 打下基础。"),
    chapter("ch0202", "索引与切片",
        ["掌握一维数组的索引与切片", "掌握二维数组的行列索引", "学会布尔索引进行条件筛选", "能够花式索引选取特定位置"],
        "数据分析中经常需要从数组中提取特定部分。NumPy 提供丰富的索引方式：一维数组的索引与列表类似；二维数组可用 arr[row,col] 同时指定行列；布尔索引通过条件表达式筛选；花式索引通过索引数组批量选取。",
        [
            cs("cs020201", "一维索引与切片",
                "import numpy as np\ns=np.array([32000,28500,41200,35800,49100,52000,48700])\nprint('首元素:',s[0])\nprint('末元素:',s[-1])\nprint('前3个:',s[:3])\nprint('位置2到4:',s[2:5])\nprint('每隔1个:',s[::2])",
                "索引从 0 开始。切片 [start:end:step] 与 Python 列表一致。负数索引从末尾数。"),
            cs("cs020202", "二维数组的行列索引",
                "import numpy as np\nregion=np.array([[12500,13800,15200],[9800,10500,11200],[11200,12800,13500],[6800,7200,8100]])\nprint('华北Q1:',region[1,0])\nprint('华东所有:',region[0,:])\nprint('Q2所有区域:',region[:,1])\nprint('前2行后2列:')\nprint(region[:2,1:])",
                "二维数组使用 arr[row, col] 格式。冒号 : 选取所有行或列。灵活组合即可提取任意子矩阵。"),
            cs("cs020203", "布尔索引与花式索引",
                "import numpy as np\ns=np.array([12500,8900,15600,4200,18200,11000,22500,7800])\nprint('大于10000:',s[s>10000])\nprint('5000-15000:',s[(s>=5000)&(s<=15000)])\nidx=np.array([0,2,4,6])\nprint('奇数月:',s[idx])\nprint('TOP3:',s[np.argsort(-s)[:3]])",
                "布尔索引通过条件生成布尔数组。多条件组合用 & 连接，每个条件用圆括号包裹。argsort(-s) 得到降序索引。")
        ],
        [
            ex("ex020201", "5行(产品)x6列(月份) 矩阵 sales_matrix：[[32000,28500,41200,35800,49100,52000],[18000,22300,19500,25600,31200,34800],[45000,48200,52300,55800,58200,61500],[15000,16500,17800,19200,21500,23800],[28000,31500,34200,38500,42000,46500]]。提取：产品C(第3行)存入 product_c；所有产品的3月份(第3列)存入 march_sales；前3个产品、后3个月的子矩阵存入 sub_matrix（应为 3x3，且 sub_matrix[0,0]=35800, sub_matrix[2,2]=61500）；产品A和E的2月和5月数据（2x2）存入 ae_matrix（值应为 [[28500,49100],[31500,42000]]）。",
                "import numpy as np\nsales_matrix=np.array([[32000,28500,41200,35800,49100,52000],[18000,22300,19500,25600,31200,34800],[45000,48200,52300,55800,58200,61500],[15000,16500,17800,19200,21500,23800],[28000,31500,34200,38500,42000,46500]])\nproduct_c=None\nmarch_sales=None\nsub_matrix=None\nae_matrix=None",
                "assert product_c.tolist()==[45000,48200,52300,55800,58200,61500]\nassert march_sales.tolist()==[41200,19500,52300,17800,34200]\nassert sub_matrix.shape==(3,3) and sub_matrix[0,0]==35800 and sub_matrix[2,2]==61500\nassert ae_matrix.tolist()==[[28500,49100],[31500,42000]]",
                ["整行: arr[行号,:]", "整列: arr[:,列号]", "子矩阵: arr[行切片,列切片]", "花式: arr[np.ix_([行], [列])] 或 arr[[行号]][:,[列号]]"],
                "product_c=sales_matrix[2,:]\nmarch_sales=sales_matrix[:,2]\nsub_matrix=sales_matrix[:3,3:]\nae_matrix=sales_matrix[np.ix_([0,4],[1,4])]"),
            ex("ex020202", "customer_spending = np.array([8500,32000,15600,48000,22000,58000,9500,42000,28000,55000])。筛选 >=30000 存入 big_spenders；筛选 10000-40000 存入 mid_spenders；big_count 为 big_spenders 的数量；TOP3 消费额存入 top3。",
                "import numpy as np\ncustomer_spending=np.array([8500,32000,15600,48000,22000,58000,9500,42000,28000,55000])\nbig_spenders=None\nmid_spenders=None\nbig_count=0\ntop3=None",
                "assert big_spenders.tolist()==[32000,48000,58000,42000,55000]\nassert mid_spenders.tolist()==[32000,15600,22000,28000]\nassert big_count==5\nassert top3.tolist()==[58000,55000,48000]",
                ["arr[条件] 筛选", "(条件1)&(条件2) 多条件组合，注意括号", "len(arr) 或 arr.size 获取数量", "np.argsort(-arr)[:3] 得到 TOP3 索引"],
                "big_spenders=customer_spending[customer_spending>=30000]\nmid_spenders=customer_spending[(customer_spending>=10000)&(customer_spending<=40000)]\nbig_count=len(big_spenders)\ntop3=customer_spending[np.argsort(-customer_spending)[:3]]")
        ], "NumPy 提供灵活的索引方式：基础索引、布尔索引、花式索引，能精准提取数据子集。"),
    chapter("ch0203", "数组运算与统计",
        ["掌握数组算术运算与广播机制", "掌握 sum/mean/max/min/std/median 等聚合函数", "掌握按轴 (axis) 计算", "能够进行简单的矩阵运算"],
        "NumPy 支持直接对整个数组进行算术运算（加减乘除），这称为向量化。当运算的两个数组形状不同时，NumPy 通过广播机制自动扩展维度，使得小数组可以与大数组高效运算，在处理跨区域跨月份销售数据加权时非常实用。",
        [
            cs("cs020301", "广播机制",
                "import numpy as np\nregion_month=np.array([[12500,13800,15200],[9800,10500,11200],[11200,12800,13500]])\ngrowth=np.array([1.05,1.08,1.10])\nprint('月度增长:')\nprint(region_month*growth)\nbonus=np.array([1.2,1.0,1.1]).reshape(3,1)\nprint('区域奖励:')\nprint(np.round(region_month*bonus,0))",
                "数组与形状匹配的一维数组相乘时自动广播。reshape(3,1) 变为列向量可按列广播。"),
            cs("cs020302", "聚合统计",
                "import numpy as np\ns=np.array([32000,28500,41200,35800,49100,52000,48700,55200])\nprint('总和:',s.sum())\nprint('均值:',int(s.mean()))\nprint('最大:',s.max(),'位置:',s.argmax())\nprint('最小:',s.min(),'位置:',s.argmin())\nprint('标准差:',int(s.std()))\nprint('中位数:',np.median(s))\nprint('75分位:',np.percentile(s,75))\nprint('累计和:',s.cumsum())",
                "ndarray 内置 sum/mean/max/min/std/argmax/argmin/cumsum 等方法。np.median/np.percentile 提供分位数计算。"),
            cs("cs020303", "按轴计算与矩阵点积",
                "import numpy as np\nsales=np.array([[12500,13800,15200,16800],[9800,10500,11200,12100],[11200,12800,13500,14500],[6800,7200,8100,9200],[15600,16200,17800,19500]])\nprint('各季度总和:',sales.sum(axis=0))\nprint('各区域年度:',sales.sum(axis=1))\nw=np.array([0.20,0.25,0.25,0.30])\nprint('加权得分:',np.round(sales@w,0))",
                "axis=0 沿行方向聚合（保留列维度），axis=1 沿列方向聚合（保留行维度）。@ 运算符做矩阵乘法，适合加权求和。")
        ],
        [
            ex("ex020301", "5产品x4季度 矩阵 product_sales：[[32000,28500,41200,35800],[18000,22300,19500,25600],[45000,48200,52300,55800],[15000,16500,17800,19200],[28000,31500,34200,38500]]。计算：每个产品全年 yearly(长度5)；每季度全产品总和 quarterly(长度4)；每个产品的季度平均 avg_q(长度5)；每个产品的季度最高 max_q(长度5)。",
                "import numpy as np\nproduct_sales=np.array([[32000,28500,41200,35800],[18000,22300,19500,25600],[45000,48200,52300,55800],[15000,16500,17800,19200],[28000,31500,34200,38500]])\nyearly=None\nquarterly=None\navg_q=None\nmax_q=None",
                "assert yearly.tolist()==[137500,85400,201800,68500,132200]\nassert quarterly.tolist()==[138000,147000,165000,174900]\nassert np.allclose(avg_q,[34375,21350,50450,17125,33050])\nassert max_q.tolist()==[41200,25600,55800,19200,38500]",
                ["每行求和: sum(axis=1)", "每列求和: sum(axis=0)", "mean(axis=1) 按行求平均", "max(axis=1) 按行求最大值"],
                "yearly=product_sales.sum(axis=1)\nquarterly=product_sales.sum(axis=0)\navg_q=product_sales.mean(axis=1)\nmax_q=product_sales.max(axis=1)"),
            ex("ex020302", "categories=[125,89,156,203]（千件），avg_prices=[299,599,899,1299]（元）。计算：每个品类销售额 cat_revenues；总销售额 total_rev；品类销售占比百分比 cat_share；整体平均单价 overall_avg_price = 总销售额/总销量（元，保留2位小数）。",
                "import numpy as np\ncategories=np.array([125,89,156,203])\navg_prices=np.array([299,599,899,1299])\ncat_revenues=None\ntotal_rev=0\ncat_share=None\noverall_avg_price=0",
                "assert cat_revenues.tolist()==[37375,53311,140244,264297]\nassert abs(cat_share.sum()-100)<0.1\nassert abs(cat_share[0]-7.46)<0.1\nassert abs(overall_avg_price-934.7)<1.0",
                ["cat_revenues = categories * avg_prices", "total_rev = cat_revenues.sum()", "cat_share = cat_revenues / total_rev * 100", "overall_avg_price = total_rev / categories.sum()"],
                "cat_revenues=categories*avg_prices\ntotal_rev=cat_revenues.sum()\ncat_share=cat_revenues/total_rev*100\noverall_avg_price=round(total_rev/categories.sum(),2)")
        ], "NumPy 的广播机制让数组间运算非常高效。按轴聚合与矩阵点积是商务数据统计分析的核心能力。")
]}

with open("assets/data/u2.json", "w", encoding="utf-8") as f:
    json.dump(UNIT2, f, ensure_ascii=False, indent=2)
print("U2 章数:", len(UNIT2["chapters"]))
