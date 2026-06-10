import json, os, subprocess
os.chdir("/workspace")

# ========== 1. 合并 courses.json ==========
courses = {"meta": {"version": "1.0.0", "course_title": "Python 商业数据分析入门课程",
                    "total_units": 6, "description": "面向商务从业者的 Python 数据分析课程体系"}}

course_list = []
for i in range(1, 7):
    with open(f"assets/data/u{i}.json", "r", encoding="utf-8") as f:
        u = json.load(f)
    if isinstance(u, list):
        u = u[0]
    course_list.append(u)
courses["courses"] = [{"courseId": "c01", "title": "Python 商务数据分析入门", "units": course_list}]

total_chs = 0
for u in course_list:
    chs = len(u["chapters"])
    total_chs += chs
    print(f"{u['unitId']} {u['title']}: {chs} 章")
print(f"Total chapters: {total_chs}")

with open("assets/data/courses.json", "w", encoding="utf-8") as f:
    json.dump(courses, f, ensure_ascii=False, indent=2)

# ========== 2. 生成 quizzes.json ==========
# 使用正确的 Python 语法构建 quizzes
quizzes = {"meta": {"version": "1.0.0"}, "quizzes": []}

# 每个测评：5 道选择题 + 2 道编程题
# 使用独立的函数式构建，避免嵌套引号问题

# ---------- 构建选择题数据 ----------
all_choice_prompts = {
    "q0101": [
        ("以下哪一项是 Python 合法变量名？", ["user_name", "123abc", "total$", "class-name"], 0, "变量名只能字母数字下划线，不能以数字开头，不能含特殊符号。"),
        ("执行 x = [1,2,3]，x[-1] 的值是？", ["1", "2", "3", "报错"], 2, "Python 列表支持负索引，-1 取最后元素。"),
        ("字典 d = {'a':1}，d.get('b', 0) 返回？", ["1", "0", "None", "报错"], 1, "get() 方法在键不存在时返回默认值 0。"),
        ("for i in range(3) 循环几次？", ["2次", "3次", "4次", "无限次"], 1, "range(3) 产生 0,1,2 三个值。"),
        ("def f(a, b=10): return a+b，f(5) 返回？", ["5", "10", "15", "报错"], 2, "b=10 默认值，5+10=15。"),
    ],
    "q0201": [
        ("np.array([1,2,3]) 的 shape 是？", ["(3,)", "(1,3)", "(3,1)", "(1,1,3)"], 0, "一维数组 shape 为 (n,)。"),
        ("np.zeros((2,3)) 创建？", ["2行3列全0", "3行2列全0", "2个元素一维", "报错"], 0, "(2,3) 表示 2 行 3 列。"),
        ("arr = np.array([[1,2,3],[4,5,6]])，arr[1,2] 的值？", ["2", "4", "5", "6"], 3, "arr[行,列]，第二行第三列是 6。"),
        ("a=np.array([1,2]), b=np.array([10,20]), a+b 结果？", ["[11,22]", "[1,2,10,20]", "报错", "[10,40]"], 0, "NumPy 数组对应元素相加。"),
        ("np.mean([1,2,3,4,5]) 返回？", ["2", "2.5", "3", "3.5"], 2, "(1+2+3+4+5)/5 = 3.0。"),
    ],
    "q0301": [
        ("pd.DataFrame({'A':[1,2]}) 几行几列？", ["1行1列", "2行1列", "1行2列", "2行2列"], 1, "一个键对应一列，值列表长度决定行数。"),
        ("df['销售额'].mean() 作用？", ["所有列均值", "销售额列均值", "筛选销售额", "排序销售额"], 1, "df['列名'] 选择该列后计算均值。"),
        ("df[df['年龄']>30] 返回？", ["年龄列>30的值", "年龄>30的行", "所有行", "报错"], 1, "布尔索引筛选条件为真的行。"),
        ("df.groupby('区域')['销售额'].sum() 作用？", ["排序区域", "按区域分组销售额总和", "按销售额分组区域", "报错"], 1, "按区域分组后对销售额求和。"),
        ("df.describe() 作用？", ["显示前5行", "描述性统计摘要", "列名", "数据类型"], 1, "describe() 生成数值列的统计摘要。"),
    ],
    "q0401": [
        ("plt.plot([1,2,3],[10,20,30]) 绘制？", ["散点图", "折线图", "柱状图", "饼图"], 1, "plot() 默认绘制折线图。"),
        ("plt.subplots(2,2) 创建？", ["2张图", "2x2子图网格", "2列2行", "2个饼图"], 1, "plt.subplots(2,2) 创建 2 行 2 列子图。"),
        ("设置图标题用？", ["plt.title()", "plt.xlabel()", "plt.legend()", "plt.grid()"], 0, "title() 设置图标题。"),
        ("color='red' 作用？", ["红色线条", "设置线条红色", "背景红色", "字体红色"], 1, "color 参数设置图形颜色。"),
        ("plt.tight_layout() 作用？", ["关闭图", "调整子图间距", "保存图", "显示网格"], 1, "tight_layout() 自动调整间距防重叠。"),
    ],
    "q0501": [
        ("中位数的意义？", ["数据平均值", "排序后中间值", "最常见值", "最大值减最小值"], 1, "中位数是排序后中间的数值。"),
        ("np.median([3,1,2,4,5]) 返回？", ["2", "3.0", "4", "3"], 1, "排序后 [1,2,3,4,5]，中间值 3。"),
        ("p值 < 0.05 表示？", ["无显著差异", "统计显著", "数据错误", "相关系数"], 1, "p<0.05 认为差异统计显著。"),
        ("相关系数 r 的范围？", ["[0,1]", "[-1,1]", "[0,100]", "任意实数"], 1, "相关系数范围 [-1,1]。"),
        ("np.corrcoef(x,y) 返回？", ["均值", "方差", "相关系数矩阵", "均值矩阵"], 2, "corrcoef 返回相关系数矩阵。"),
    ],
    "q0601": [
        ("RFM 模型中 R 代表？", ["购买频次", "最近购买", "购买金额", "客户编号"], 1, "R=Recency 最近购买时间。"),
        ("ABC 分析中 A 类 SKU 贡献？", ["数量最多", "销售额约70%", "利润最低", "库存最少"], 1, "A 类贡献约 70% 销售额。"),
        ("库存周转天数越低说明？", ["库存积压严重", "库存管理良好", "缺货风险高", "销售额低"], 1, "周转天数越低卖出越快管理良好。"),
        ("df.sort_values('销售额', ascending=False) 作用？", ["升序排序", "降序排序", "随机排序", "不排序"], 1, "ascending=False 降序。"),
        ("高价值客户通常？", ["RFM总分高", "RFM总分低", "只看R", "只看M"], 0, "RFM总分越高客户价值越高。"),
    ],
}

# ---------- 构建编程题数据（使用原始字符串避免转义问题）----------
# 每道题：(prompt, starter_code, test_code, hints_list)
all_coding_data = {
    "q0101": [
        ("编写函数 count_even(lst) 返回列表中偶数个数。例如 count_even([1,2,3,4,5,6]) 返回 3。",
         "def count_even(lst):\n    # 在此编写代码\n    pass\n\nresult = count_even([1,2,3,4,5,6])\nprint(result)",
         "assert count_even([1,2,3,4,5,6])==3\nassert count_even([2,4,6,8,10])==5\nassert count_even([1,3,5])==0\nassert count_even([])==0",
         ["for x in lst 遍历", "x % 2 == 0 判断偶数", "初始化计数器 c=0", "c += 1 累加"]),
        ("编写函数 price_total(items) 接受字典 items 键商品名值单价返回总价。",
         "def price_total(items):\n    # 在此编写代码\n    pass\n\nresult = price_total({'苹果':3, '香蕉':2})\nprint(result)",
         "assert price_total({'苹果':3,'香蕉':2})==5\nassert price_total({})==0\nassert price_total({'A':10,'B':20,'C':30})==60",
         ["items.values() 获取所有值", "sum() 直接求和", "或 for 循环累加"]),
    ],
    "q0201": [
        ("创建形状 (3,4) 的全 1 矩阵元素乘以 5，计算元素总和 total。",
         "import numpy as np\narr = np.zeros((3,4))\n# 在此修改并计算\ntotal = 0\nprint(total)",
         "import numpy as np\nassert isinstance(arr, np.ndarray)\nassert arr.shape == (3,4)\nassert (arr == 5).all()\nassert total == 60",
         ["np.ones((3,4)) 创建全1", "arr * 5 得全5矩阵", "arr.sum() 求和", "3*4*5=60"]),
        ("生成 np.arange(1,13) 重塑为 (3,4)，计算每行均值 row_means。",
         "import numpy as np\nmat = np.arange(1,13).reshape(3,4)\nrow_means = None\nprint(row_means)",
         "import numpy as np\nassert row_means.shape == (3,)\nassert abs(row_means[0] - 2.5) < 0.001\nassert abs(row_means[1] - 6.5) < 0.001\nassert abs(row_means[2] - 10.5) < 0.001",
         ["np.arange(1,13) 产生 1-12", ".reshape(3,4) 重塑", "row_means = mat.mean(axis=1)", "axis=1 对每行计算均值"]),
    ],
    "q0301": [
        ("创建 DataFrame：月份 ['1月','2月','3月'], 销售额 [100,150,200]。计算 total_sales 总和，avg_sales 均值。",
         "import pandas as pd\ndf = pd.DataFrame({'月份': [], '销售额': []})\ntotal_sales = 0\navg_sales = 0\nprint(total_sales, avg_sales)",
         "import pandas as pd\nassert isinstance(df, pd.DataFrame)\nassert df.shape == (3, 2)\nassert total_sales == 450\nassert abs(avg_sales - 150) < 0.001",
         ["pd.DataFrame({'月份':['1月','2月','3月'],'销售额':[100,150,200]})", "df['销售额'].sum()", "df['销售额'].mean()"]),
        ("基于上面的 df，筛选销售额 > 120 的行赋给 df_high，high_count 为数量，high_avg 均值。",
         "import pandas as pd\ndf = pd.DataFrame({'月份':['1月','2月','3月'],'销售额':[100,150,200]})\ndf_high = None\nhigh_count = 0\nhigh_avg = 0\nprint(high_count, high_avg)",
         "import pandas as pd\nassert isinstance(df_high, pd.DataFrame)\nassert df_high.shape[0] == 2\nassert high_count == 2\nassert abs(high_avg - 175) < 0.001",
         ["df_high = df[df['销售额'] > 120]", "len(df_high) 得数量", "df_high['销售额'].mean() 得均值"]),
    ],
    "q0401": [
        ("绘制月份销售折线图：x=[1,2,3,4], y=[100,150,130,200]。红色线条宽 2，标记 'o'，title='月度销售'。",
         "import matplotlib.pyplot as plt\nx=[1,2,3,4]\ny=[100,150,130,200]\n# 在此绘制\nprint('图表生成完成')",
         "import matplotlib\nfig = plt.gcf()\naxes = fig.axes\nassert len(axes) > 0\nax = axes[0]\nlines = ax.get_lines()\nassert len(lines) > 0\nassert ax.get_title() == '月度销售'",
         ["plt.plot(x, y, color='red', marker='o', linewidth=2)", "plt.title('月度销售')"]),
        ("绘制柱状图：regions=['华东','华北','华南'], values=[300,250,400])。颜色 '#2563eb'，title='区域销售'，ylabel='销售额'。",
         "import matplotlib.pyplot as plt\nregions=['华东','华北','华南']\nvalues=[300,250,400]\n# 在此绘制\nprint('图表生成完成')",
         "import matplotlib\nfig = plt.gcf()\naxes = fig.axes\nassert len(axes) > 0\nax = axes[0]\nassert ax.get_title() == '区域销售'\nassert ax.get_ylabel() == '销售额'",
         ["plt.bar(regions, values, color='#2563eb')", "plt.title('区域销售')", "plt.ylabel('销售额')"]),
    ],
    "q0501": [
        ("sales=[120,150,180,210,240,270,300]。计算 mean_val 均值，median_val 中位数，std_val 标准差。",
         "import numpy as np\nsales=[120,150,180,210,240,270,300]\nmean_val = 0\nmedian_val = 0\nstd_val = 0\nprint(mean_val, median_val, std_val)",
         "import numpy as np\nassert abs(mean_val - 210) < 0.01\nassert abs(median_val - 210) < 0.01\nassert std_val > 60",
         ["np.mean(sales)", "np.median(sales)", "np.std(sales)"]),
        ("x=np.array([1,2,3,4,5]), y=np.array([2,4,5,4,5])。计算 corr_val 相关系数。",
         "import numpy as np\nx=np.array([1,2,3,4,5])\ny=np.array([2,4,5,4,5])\ncorr_val = 0\nprint(corr_val)",
         "import numpy as np\nassert -1 <= corr_val <= 1\nassert corr_val > 0.5",
         ["np.corrcoef(x, y)[0,1] 得相关系数", "正相关时 r > 0"]),
    ],
    "q0601": [
        ("销售数据 DataFrame，区域 ['华东','华北','华南'], 销售额 [5000,4000,6000]。找出 top_region 最高销售额区域，total_sales 总和。",
         "import pandas as pd\ndf = pd.DataFrame({'区域':['华东','华北','华南'],'销售额':[5000,4000,6000]})\ntop_region = ''\ntotal_sales = 0\nprint(top_region, total_sales)",
         "import pandas as pd\nassert top_region == '华南'\nassert total_sales == 15000",
         ["df.sort_values('销售额', ascending=False).iloc[0]['区域']", "df['销售额'].sum()"]),
        ("基于上面的 df，筛选销售额 >= 5000 的行存入 df_filtered，filtered_count 为数量。",
         "import pandas as pd\ndf = pd.DataFrame({'区域':['华东','华北','华南'],'销售额':[5000,4000,6000]})\ndf_filtered = None\nfiltered_count = 0\nprint(filtered_count)",
         "import pandas as pd\nassert isinstance(df_filtered, pd.DataFrame)\nassert filtered_count == 2",
         ["df_filtered = df[df['销售额'] >= 5000]", "filtered_count = len(df_filtered)"]),
    ],
}

quiz_list = [
    ("q0101", "u01", "Python 基础单元测评", ["变量数据类型", "列表与字典", "函数与控制流"]),
    ("q0201", "u02", "NumPy 数值计算单元测评", ["ndarray基础", "索引与切片", "数组运算与统计"]),
    ("q0301", "u03", "Pandas 基础单元测评", ["DataFrame基础", "读取CSV", "选择与筛选", "分组与聚合"]),
    ("q0401", "u04", "Matplotlib 可视化单元测评", ["基础绘图", "自定义样式", "多图布局与常见图"]),
    ("q0501", "u05", "商务统计分析单元测评", ["描述统计", "假设检验", "相关性与回归"]),
    ("q0601", "u06", "商业案例实战单元测评", ["销售分析", "客户分群", "库存优化"]),
]

for qid, uid, title, tags in quiz_list:
    questions = []
    for idx, (prompt, opts, ci, expl) in enumerate(all_choice_prompts[qid]):
        questions.append({
            "type": "choice",
            "qid": f"q{idx+1}",
            "prompt": prompt,
            "options": opts,
            "correctIndex": ci,
            "explanation": expl
        })
    for idx, (cp, sc, tc, hints) in enumerate(all_coding_data[qid]):
        questions.append({
            "type": "coding",
            "qid": f"c{idx+1}",
            "prompt": cp,
            "starterCode": sc,
            "testCode": tc,
            "hints": hints
        })
    quizzes["quizzes"].append({
        "quizId": qid,
        "unitId": uid,
        "title": title,
        "questions": questions,
        "weakTags": tags
    })

with open("assets/data/quizzes.json", "w", encoding="utf-8") as f:
    json.dump(quizzes, f, ensure_ascii=False, indent=2)

print("\nquizzes.json 生成完成")
print("测评数量:", len(quizzes["quizzes"]))

# 验证 JSON
r1 = subprocess.run(["python3", "-m", "json.tool", "assets/data/courses.json"], capture_output=True, text=True)
r2 = subprocess.run(["python3", "-m", "json.tool", "assets/data/quizzes.json"], capture_output=True, text=True)
print("courses.json:", "OK" if r1.returncode == 0 else "FAIL")
print("quizzes.json:", "OK" if r2.returncode == 0 else "FAIL")
