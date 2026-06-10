import json, os
os.chdir("/workspace")
U = []  # units list

def chapter(cid, title, objectives, content, code_samples, exercises, summary):
    return {"chapter_id": cid, "title": title, "objectives": objectives,
            "content": content, "code_samples": code_samples, "exercises": exercises,
            "summary": summary}

def cs(i, title, code, explanation):
    return {"id": i, "title": title, "code": code, "explanation": explanation}

def ex(eid, prompt, starter, test, hints, ref):
    return {"exerciseId": eid, "prompt": prompt, "starterCode": starter,
            "testCode": test, "hints": hints, "referenceAnswer": ref}

# ================== U1: Python 基础 (3章) ==================
U.append({"unitId": "u01", "title": "Python 基础", "chapters": [
    chapter("ch0101", "变量与数据类型",
        ["掌握 print 与变量赋值", "理解 int/float/str/bool 四种类型", "学会类型转换"],
        "Python 是商务数据分析的主流语言。变量用于存储销售金额、产品名称等数据。本章从 print 函数开始介绍整数、浮点数、字符串、布尔值四种核心类型。正确使用数据类型能让分析结果更可靠。",
        [
            cs("cs010101", "print 与变量", "print('Hello')\nprice=2999.99\nprint('单价:'+str(price))",
                "print 输出内容。= 把数据赋值给变量。字符串拼接需要 str() 转换数字。"),
            cs("cs010102", "类型转换", "s='58000'\nnum=float(s)\nprint(num*1.1)",
                "CSV 数据常为字符串，int/float/str 用于类型转换。"),
            cs("cs010103", "算术运算", "p,d,q=1599,0.2,230\nfinal=p*(1-d)\ntotal=final*q\nprint(total)",
                "+-*/ 是标准算术运算符，常用于计算折扣价与总销售额。")
        ],
        [
            ex("ex010101", "定义 name='张三' company='ABC科技' years=3 三个变量并打印拼接介绍。",
                "name=''\ncompany=''\nyears=0\n# 编写代码",
                "assert isinstance(name,str) and len(name)>0\nassert isinstance(company,str) and len(company)>0\nassert isinstance(years,int) and years>=0",
                ["字符串用双引号", "拼接用 +，数字需 str() 转换"],
                "name='张三'\ncompany='ABC科技'\nyears=3\nprint('大家好我是'+name+',在'+company+'工作'+str(years)+'年')"),
            ex("ex010102", "price=1599 discount=0.2 sales=230。计算折后价 final_price、总销售额 total_revenue、再卖50件 extra_revenue。",
                "price=1599\ndiscount=0.2\nsales=230\nfinal_price=0\ntotal_revenue=0\nextra_revenue=0\n# 编写代码",
                "assert abs(final_price-1279.2)<0.01\nassert abs(total_revenue-294216.0)<0.01\nassert abs(extra_revenue-358176.0)<0.01",
                ["折后价=原价*(1-折扣)", "总销售=单价*数量", "再卖50件=280件"],
                "price=1599\ndiscount=0.2\nsales=230\nfinal_price=price*(1-discount)\ntotal_revenue=final_price*sales\nextra_revenue=final_price*(sales+50)\nprint(final_price,total_revenue,extra_revenue)")
        ],
        "本章介绍了 print、变量与四种数据类型。正确识别和转换数据类型是数据分析的基础。"),
    chapter("ch0102", "列表与字典",
        ["掌握 list 的索引、切片、append", "掌握 dict 的键值对操作", "能选择合适的数据结构"],
        "列表用于存储有序同类数据（如月销售额序列），字典用于存储带属性的业务对象（如产品的名称、价格、销量）。两者结合可表示复杂的业务数据。",
        [
            cs("cs010201", "列表基础", "p=['笔记本','平板','手表']\ns=[125,280,198]\nprint(p[0],s[-1])",
                "列表用 [] 创建。索引从 0 开始，-1 指最后一个元素。"),
            cs("cs010202", "切片与 append", "q=[32000,28500,41200,35800,49100]\nprint(q[:3])\nq.append(52000)\nprint(len(q))",
                "list[start:end] 切片选取部分元素。append 在末尾添加。len 获取长度。"),
            cs("cs010203", "字典操作", "p={'name':'手机','price':2999}\np['stock']=350\np['price']=2799\nprint(p)",
                "字典用 {} 创建。dict[key]=value 可新增或修改键值对。")
        ],
        [
            ex("ex010201", "创建 regions=['华东','华北','华南','西南'] 和 sales_data=[48500,39200,42800,31500]，再 append '西北' 和 26800。",
                "regions=[]\nsales_data=[]\n# 编写代码",
                "assert regions==['华东','华北','华南','西南','西北']\nassert sales_data==[48500,39200,42800,31500,26800]",
                ["元素用逗号分隔", "append 在末尾添加元素"],
                "regions=['华东','华北','华南','西南']\nsales_data=[48500,39200,42800,31500]\nregions.append('西北')\nsales_data.append(26800)"),
            ex("ex010202", "创建 customer 字典：name='李晓明',age=35,city='上海',is_vip=True,total_purchase=28600。修改 total_purchase 为 35000，新增 last_order='2025-05-20'。",
                "customer={}\n# 编写代码",
                "assert customer['name']=='李晓明' and customer['age']==35\nassert customer['city']=='上海' and customer['is_vip'] is True\nassert customer['total_purchase']==35000 and customer['last_order']=='2025-05-20'",
                ["key:value 格式", "布尔值首字母大写", "赋值语句修改或新增键值对"],
                "customer={'name':'李晓明','age':35,'city':'上海','is_vip':True,'total_purchase':28600}\ncustomer['total_purchase']=35000\ncustomer['last_order']='2025-05-20'")
        ],
        "列表适合有序同类数据集合，字典适合带属性的业务对象。"),
    chapter("ch0103", "函数与控制流",
        ["掌握 def 函数定义与 return", "掌握 if-elif-else", "掌握 for 循环", "能结合处理商业数据"],
        "函数封装可复用逻辑。条件判断处理业务规则（如会员分级）。for 循环批量处理数据（如遍历销售记录计算利润）。",
        [
            cs("cs010301", "函数定义", "def profit(rev,cost):\n    return rev-cost,(rev-cost)/rev*100\np,r=profit(58000,36200)\nprint(p,round(r,1))",
                "def 定义函数。可 return 多个值用逗号分开。round(x,n) 保留 n 位小数。"),
            cs("cs010302", "条件判断", "s=18500\nif s>=30000:l='钻石'\nelif s>=15000:l='金卡'\nelif s>=5000:l='银卡'\nelse:l='普通'\nprint(l)",
                "条件从高到低排列。每个条件冒号结尾，下一行缩进 4 空格。"),
            cs("cs010303", "for 循环", "recs=[{'a':12500,'r':'华东'},{'a':8900,'r':'华北'},{'a':15600,'r':'华东'}]\nt=0;e=0\nfor x in recs:\n    t=t+x['a']\n    if x['r']=='华东':e=e+x['a']\nprint(t,e)",
                "for 遍历列表每项。循环内可加 if 条件进行筛选和汇总。")
        ],
        [
            ex("ex010301", "写函数 calculate_commission(s)：>=50000 返回 10%，>=20000 返回 7%，>=10000 返回 5%，其他 3%。返回整数。",
                "def calculate_commission(s):\n    return 0\nprint(calculate_commission(65000))",
                "assert calculate_commission(65000)==6500\nassert calculate_commission(28000)==1960\nassert calculate_commission(10000)==500\nassert calculate_commission(8500)==255",
                ["使用 if-elif-else 从高到低判断", "int() 对结果取整避免浮点误差"],
                "def calculate_commission(s):\n    if s>=50000:return int(s*0.10)\n    elif s>=20000:return int(s*0.07)\n    elif s>=10000:return int(s*0.05)\n    else:return int(s*0.03)\nprint(calculate_commission(65000))"),
            ex("ex010302", "q=[120,85,156,78,203,145]，up=[299,1599,899,499,2599,1299]。用 for+索引 计算每产品销售额存入 product_revenues，总销售额 total_revenue。",
                "q=[120,85,156,78,203,145]\nup=[299,1599,899,499,2599,1299]\nproduct_revenues=[]\ntotal_revenue=0\n# 编写代码",
                "assert product_revenues==[35880,135915,140244,38922,527597,188355]\nassert total_revenue==1066913",
                ["range(len(q)) 获取索引 i", "q[i]*up[i] append 到 product_revenues", "total_revenue 循环累加"],
                "q=[120,85,156,78,203,145]\nup=[299,1599,899,499,2599,1299]\nproduct_revenues=[]\ntotal_revenue=0\nfor i in range(len(q)):\n    r=q[i]*up[i]\n    product_revenues.append(r)\n    total_revenue=total_revenue+r\nprint(product_revenues,total_revenue)")
        ],
        "函数让逻辑可复用，条件判断处理业务规则，循环让批量数据处理自动化。")
]})

print("U1 完成")
with open("assets/data/_u1.json", "w", encoding="utf-8") as f:
    json.dump(U, f, ensure_ascii=False, indent=2)
