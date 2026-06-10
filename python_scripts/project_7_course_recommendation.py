#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目7: 教育平台推荐课程关联规则分析（Apriori）
内容：用户购买/学习的课程组合 → 挖掘关联规则
Python技能：mlxtend.Apriori、关联规则可视化
业务目标：给学生做 "学了这门课还会学什么"
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 生成模拟课程数据
def generate_courses():
    """生成课程数据"""
    courses = [
        'Python数据分析基础',
        'Python数据分析进阶',
        'Excel高级应用',
        'SQL数据库',
        '数据可视化',
        '统计分析',
        '商业智能',
        '机器学习入门',
        '深度学习',
        '大数据分析'
    ]
    return courses

# 生成用户学习记录
def generate_user_courses(courses, num_users=1000):
    """生成用户学习记录"""
    user_courses = []
    user_id = 1
    
    # 课程关联关系（模拟）
    course_relations = {
        'Python数据分析基础': ['Python数据分析进阶', '数据可视化', '统计分析'],
        'Python数据分析进阶': ['机器学习入门', '深度学习', '大数据分析'],
        'Excel高级应用': ['SQL数据库', '商业智能', '数据可视化'],
        'SQL数据库': ['商业智能', '数据可视化', 'Python数据分析基础'],
        '数据可视化': ['商业智能', 'Python数据分析基础', '统计分析'],
        '统计分析': ['机器学习入门', 'Python数据分析进阶', '数据可视化'],
        '商业智能': ['SQL数据库', 'Excel高级应用', '数据可视化'],
        '机器学习入门': ['深度学习', 'Python数据分析进阶', '统计分析'],
        '深度学习': ['机器学习入门', 'Python数据分析进阶', '大数据分析'],
        '大数据分析': ['Python数据分析进阶', '深度学习', 'SQL数据库']
    }
    
    for _ in range(num_users):
        # 随机选择1-4门课程
        num_courses = np.random.randint(1, 5)
        selected_courses = []
        
        # 第一个课程随机选择
        first_course = np.random.choice(courses)
        selected_courses.append(first_course)
        
        # 基于关联关系选择后续课程
        for i in range(1, num_courses):
            # 从已选课程的关联课程中选择
            possible_courses = []
            for course in selected_courses:
                possible_courses.extend(course_relations.get(course, []))
            
            # 去重并排除已选课程
            possible_courses = [c for c in possible_courses if c not in selected_courses]
            
            if possible_courses:
                next_course = np.random.choice(possible_courses)
                selected_courses.append(next_course)
            else:
                # 如果没有更多关联课程，随机选择
                remaining_courses = [c for c in courses if c not in selected_courses]
                if remaining_courses:
                    next_course = np.random.choice(remaining_courses)
                    selected_courses.append(next_course)
                else:
                    break
        
        user_courses.append({
            'user_id': user_id,
            'courses': selected_courses,
            'timestamp': datetime(2023, 6, 1) + timedelta(days=np.random.randint(0, 30))
        })
        user_id += 1
    
    return pd.DataFrame(user_courses)

# 数据预处理
def preprocess_data(user_courses_df):
    """数据预处理"""
    # 转换为交易格式
    transactions = user_courses_df['courses'].tolist()
    
    # 使用TransactionEncoder编码
    te = TransactionEncoder()
    te_ary = te.fit(transactions).transform(transactions)
    df_encoded = pd.DataFrame(te_ary, columns=te.columns_)
    
    return df_encoded, te

# 生成频繁项集
def generate_frequent_itemsets(df_encoded, min_support=0.1):
    """生成频繁项集"""
    frequent_itemsets = apriori(df_encoded, min_support=min_support, use_colnames=True)
    frequent_itemsets = frequent_itemsets.sort_values('support', ascending=False)
    return frequent_itemsets

# 生成关联规则
def generate_association_rules(frequent_itemsets, min_confidence=0.5):
    """生成关联规则"""
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)
    rules = rules.sort_values('confidence', ascending=False)
    return rules

# 分析频繁项集
def analyze_frequent_itemsets(frequent_itemsets):
    """分析频繁项集"""
    plt.figure(figsize=(12, 6))
    
    # 前20个频繁项集
    top_itemsets = frequent_itemsets.head(20)
    
    # 提取项集大小
    top_itemsets['itemset_size'] = top_itemsets['itemsets'].apply(lambda x: len(x))
    
    # 绘制支持度
    plt.subplot(1, 2, 1)
    sns.barplot(x=top_itemsets['itemsets'].apply(lambda x: ', '.join(x)), 
                y=top_itemsets['support'])
    plt.title('频繁项集支持度')
    plt.ylabel('支持度')
    plt.xticks(rotation=90)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # 按项集大小分析
    plt.subplot(1, 2, 2)
    size_support = top_itemsets.groupby('itemset_size')['support'].mean()
    sns.barplot(x=size_support.index, y=size_support.values)
    plt.title('不同大小项集的平均支持度')
    plt.xlabel('项集大小')
    plt.ylabel('平均支持度')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/frequent_itemsets.png')
    plt.show()
    
    print("\n频繁项集分析：")
    print(f"总频繁项集数：{len(frequent_itemsets)}")
    print("\n前10个频繁项集：")
    for i, row in frequent_itemsets.head(10).iterrows():
        items = ', '.join(row['itemsets'])
        print(f"{items}: 支持度 = {row['support']:.3f}")

# 分析关联规则
def analyze_association_rules(rules):
    """分析关联规则"""
    plt.figure(figsize=(15, 10))
    
    # 前20条规则
    top_rules = rules.head(20)
    
    # 置信度和提升度
    plt.subplot(2, 1, 1)
    sns.barplot(x=top_rules['antecedents'].apply(lambda x: ', '.join(x)) + ' → ' + top_rules['consequents'].apply(lambda x: ', '.join(x)),
                y=top_rules['confidence'])
    plt.title('关联规则置信度')
    plt.ylabel('置信度')
    plt.xticks(rotation=90)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # 提升度
    plt.subplot(2, 1, 2)
    sns.barplot(x=top_rules['antecedents'].apply(lambda x: ', '.join(x)) + ' → ' + top_rules['consequents'].apply(lambda x: ', '.join(x)),
                y=top_rules['lift'])
    plt.title('关联规则提升度')
    plt.ylabel('提升度')
    plt.xticks(rotation=90)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/association_rules.png')
    plt.show()
    
    print("\n关联规则分析：")
    print(f"总规则数：{len(rules)}")
    print("\n前10条规则：")
    for i, row in rules.head(10).iterrows():
        antecedents = ', '.join(row['antecedents'])
        consequents = ', '.join(row['consequents'])
        print(f"{antecedents} → {consequents}")
        print(f"  置信度: {row['confidence']:.3f}, 提升度: {row['lift']:.3f}")

# 生成课程推荐
def generate_course_recommendations(rules, course):
    """生成课程推荐"""
    # 找到包含该课程作为前件的规则
    course_rules = rules[rules['antecedents'].apply(lambda x: course in x)]
    
    # 按置信度排序
    course_rules = course_rules.sort_values('confidence', ascending=False)
    
    # 提取推荐课程
    recommendations = []
    for _, row in course_rules.iterrows():
        for consequent in row['consequents']:
            if consequent != course:
                recommendations.append({
                    'course': consequent,
                    'confidence': row['confidence'],
                    'lift': row['lift']
                })
    
    # 去重并按置信度排序
    recommendations = pd.DataFrame(recommendations).drop_duplicates('course').sort_values('confidence', ascending=False)
    
    return recommendations

# 分析每个课程的推荐
def analyze_course_recommendations(rules, courses):
    """分析每个课程的推荐"""
    plt.figure(figsize=(15, 20))
    
    for i, course in enumerate(courses, 1):
        recommendations = generate_course_recommendations(rules, course)
        
        if not recommendations.empty:
            plt.subplot(len(courses), 1, i)
            sns.barplot(x=recommendations['course'], y=recommendations['confidence'])
            plt.title(f'{course} 的推荐课程')
            plt.ylabel('置信度')
            plt.xticks(rotation=45)
            plt.ylim(0, 1)
            plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/course_recommendations.png')
    plt.show()
    
    # 输出推荐结果
    print("\n各课程推荐结果：")
    for course in courses:
        recommendations = generate_course_recommendations(rules, course)
        print(f"\n{course}：")
        if not recommendations.empty:
            for _, row in recommendations.head(3).iterrows():
                print(f"  → {row['course']} (置信度: {row['confidence']:.3f}, 提升度: {row['lift']:.3f})")
        else:
            print("  无推荐课程")

# 分析规则网络
def analyze_rule_network(rules, top_n=20):
    """分析规则网络"""
    import networkx as nx
    
    # 构建规则网络
    G = nx.DiGraph()
    
    # 添加前20条规则
    for _, row in rules.head(top_n).iterrows():
        antecedents = ', '.join(row['antecedents'])
        consequents = ', '.join(row['consequents'])
        G.add_edge(antecedents, consequents, weight=row['confidence'])
    
    # 绘制网络
    plt.figure(figsize=(15, 10))
    pos = nx.spring_layout(G, k=0.3)
    
    # 节点大小基于入度
    node_size = [G.in_degree(n) * 1000 for n in G.nodes()]
    
    # 边的宽度基于置信度
    edge_width = [G[u][v]['weight'] * 5 for u, v in G.edges()]
    
    nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color='lightblue')
    nx.draw_networkx_edges(G, pos, width=edge_width, alpha=0.6, edge_color='gray')
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='SimHei')
    
    plt.title('关联规则网络')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/rule_network.png')
    plt.show()

# 主函数
def main():
    print("项目7: 教育平台推荐课程关联规则分析（Apriori）")
    print("=" * 60)
    
    # 生成数据
    print("1. 生成模拟数据...")
    courses = generate_courses()
    user_courses_df = generate_user_courses(courses, num_users=1000)
    print(f"生成用户数：{len(user_courses_df)}")
    print(f"课程总数：{len(courses)}")
    
    # 数据预处理
    print("\n2. 数据预处理...")
    df_encoded, te = preprocess_data(user_courses_df)
    print(f"编码后的数据形状：{df_encoded.shape}")
    
    # 生成频繁项集
    print("\n3. 生成频繁项集...")
    frequent_itemsets = generate_frequent_itemsets(df_encoded, min_support=0.1)
    
    # 分析频繁项集
    print("\n4. 分析频繁项集...")
    analyze_frequent_itemsets(frequent_itemsets)
    
    # 生成关联规则
    print("\n5. 生成关联规则...")
    rules = generate_association_rules(frequent_itemsets, min_confidence=0.5)
    
    # 分析关联规则
    print("\n6. 分析关联规则...")
    analyze_association_rules(rules)
    
    # 分析课程推荐
    print("\n7. 分析课程推荐...")
    analyze_course_recommendations(rules, courses)
    
    # 分析规则网络
    print("\n8. 分析规则网络...")
    analyze_rule_network(rules, top_n=20)
    
    print("\n分析完成！")
    print("生成的图表保存位置：/workspace/python-projects/")

if __name__ == "__main__":
    main()
