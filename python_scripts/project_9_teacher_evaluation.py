#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目9: 教师授课质量多维度综合评分模型
内容：评分、完课率、互动率、复购率 → 构建综合评分
Python技能：权重计算、标准化、综合指标、雷达图
业务目标：客观评价教师教学效果
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 生成模拟教师数据
def generate_teacher_data():
    """生成教师数据"""
    teachers = [
        {'teacher_id': 1, 'teacher_name': '张老师', 'subject': 'Python数据分析'},
        {'teacher_id': 2, 'teacher_name': '李老师', 'subject': 'Excel高级应用'},
        {'teacher_id': 3, 'teacher_name': '王老师', 'subject': '数据可视化'},
        {'teacher_id': 4, 'teacher_name': '刘老师', 'subject': '统计分析'},
        {'teacher_id': 5, 'teacher_name': '陈老师', 'subject': '商业智能'},
        {'teacher_id': 6, 'teacher_name': '赵老师', 'subject': '机器学习'},
        {'teacher_id': 7, 'teacher_name': '钱老师', 'subject': '深度学习'},
        {'teacher_id': 8, 'teacher_name': '孙老师', 'subject': '大数据分析'}
    ]
    return pd.DataFrame(teachers)

# 生成教师评价数据
def generate_evaluation_data(teachers_df):
    """生成教师评价数据"""
    evaluation_data = []
    
    for _, teacher in teachers_df.iterrows():
        teacher_id = teacher['teacher_id']
        
        # 基础评分（4.0-5.0之间）
        base_rating = np.random.uniform(4.0, 5.0)
        
        # 完课率（70%-95%之间）
        completion_rate = np.random.uniform(0.7, 0.95)
        
        # 互动率（30%-80%之间）
        interaction_rate = np.random.uniform(0.3, 0.8)
        
        # 复购率（10%-40%之间）
        repurchase_rate = np.random.uniform(0.1, 0.4)
        
        # 学生人数
        student_count = np.random.randint(100, 1000)
        
        # 课程数
        course_count = np.random.randint(1, 5)
        
        # 教学年限
        teaching_years = np.random.randint(1, 10)
        
        evaluation_data.append({
            'teacher_id': teacher_id,
            'rating': base_rating,
            'completion_rate': completion_rate,
            'interaction_rate': interaction_rate,
            'repurchase_rate': repurchase_rate,
            'student_count': student_count,
            'course_count': course_count,
            'teaching_years': teaching_years
        })
    
    return pd.DataFrame(evaluation_data)

# 数据预处理和标准化
def preprocess_data(evaluation_df):
    """数据预处理和标准化"""
    # 复制数据
    df = evaluation_df.copy()
    
    # 标准化处理（0-1之间）
    for col in ['rating', 'completion_rate', 'interaction_rate', 'repurchase_rate']:
        min_val = df[col].min()
        max_val = df[col].max()
        df[col + '_norm'] = (df[col] - min_val) / (max_val - min_val)
    
    # 学生人数标准化（对数处理）
    df['student_count_norm'] = np.log(df['student_count']) / np.log(df['student_count'].max())
    
    return df

# 计算综合评分
def calculate_comprehensive_score(df, weights=None):
    """计算综合评分"""
    if weights is None:
        # 默认权重
        weights = {
            'rating_norm': 0.3,
            'completion_rate_norm': 0.25,
            'interaction_rate_norm': 0.2,
            'repurchase_rate_norm': 0.15,
            'student_count_norm': 0.1
        }
    
    # 计算加权得分
    df['comprehensive_score'] = 0
    for feature, weight in weights.items():
        df['comprehensive_score'] += df[feature] * weight
    
    # 转换为0-100分制
    df['comprehensive_score'] = df['comprehensive_score'] * 100
    
    # 排序
    df = df.sort_values('comprehensive_score', ascending=False)
    
    return df, weights

# 分析各维度得分
def analyze_dimension_scores(df):
    """分析各维度得分"""
    plt.figure(figsize=(15, 10))
    
    # 各维度得分对比
    dimensions = ['rating', 'completion_rate', 'interaction_rate', 'repurchase_rate']
    dimension_names = ['评分', '完课率', '互动率', '复购率']
    
    # 转换为百分比
    df['completion_rate_pct'] = df['completion_rate'] * 100
    df['interaction_rate_pct'] = df['interaction_rate'] * 100
    df['repurchase_rate_pct'] = df['repurchase_rate'] * 100
    
    # 绘制雷达图
    plt.subplot(2, 2, 1)
    for i, teacher_id in enumerate(df['teacher_id']):
        teacher_data = df[df['teacher_id'] == teacher_id]
        values = [
            teacher_data['rating'].iloc[0] * 20,  # 转换为0-100
            teacher_data['completion_rate_pct'].iloc[0],
            teacher_data['interaction_rate_pct'].iloc[0],
            teacher_data['repurchase_rate_pct'].iloc[0]
        ]
        values += values[:1]  # 闭合
        
        angles = np.linspace(0, 2 * np.pi, 4, endpoint=False).tolist()
        angles += angles[:1]
        
        plt.plot(angles, values, linewidth=2, linestyle='solid', label=f'教师{teacher_id}')
        plt.fill(angles, values, alpha=0.1)
    
    plt.title('各教师多维度得分雷达图')
    plt.xticks(angles[:-1], dimension_names)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # 各维度平均分
    plt.subplot(2, 2, 2)
    avg_scores = [
        df['rating'].mean() * 20,
        df['completion_rate_pct'].mean(),
        df['interaction_rate_pct'].mean(),
        df['repurchase_rate_pct'].mean()
    ]
    sns.barplot(x=dimension_names, y=avg_scores)
    plt.title('各维度平均得分')
    plt.ylabel('得分')
    plt.ylim(0, 100)
    
    # 综合评分分布
    plt.subplot(2, 1, 2)
    sns.barplot(x=df['teacher_id'], y=df['comprehensive_score'])
    plt.title('教师综合评分')
    plt.ylabel('综合评分')
    plt.ylim(0, 100)
    
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/teacher_evaluation.png')
    plt.show()

# 分析教师排名
def analyze_teacher_ranking(df, teachers_df):
    """分析教师排名"""
    # 合并教师信息
    merged_df = df.merge(teachers_df, on='teacher_id')
    
    # 排名
    merged_df['rank'] = merged_df['comprehensive_score'].rank(ascending=False, method='first').astype(int)
    
    # 排序
    merged_df = merged_df.sort_values('rank')
    
    # 可视化
    plt.figure(figsize=(12, 6))
    sns.barplot(x='teacher_name', y='comprehensive_score', data=merged_df)
    plt.title('教师综合评分排名')
    plt.ylabel('综合评分')
    plt.xticks(rotation=45)
    plt.ylim(0, 100)
    
    # 添加排名标签
    for i, row in merged_df.iterrows():
        plt.text(i, row['comprehensive_score'] + 2, f'第{row["rank"]}名', ha='center')
    
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/teacher_ranking.png')
    plt.show()
    
    # 输出排名结果
    print("\n教师综合评分排名：")
    for _, row in merged_df.iterrows():
        print(f"第{row['rank']}名: {row['teacher_name']} ({row['subject']}) - 综合评分: {row['comprehensive_score']:.2f}")

# 分析各因素相关性
def analyze_correlations(df):
    """分析各因素相关性"""
    # 选择相关列
    corr_cols = ['rating', 'completion_rate', 'interaction_rate', 'repurchase_rate', 'comprehensive_score']
    corr_matrix = df[corr_cols].corr()
    
    # 热力图
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('各因素相关性热力图')
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/correlation_analysis.png')
    plt.show()
    
    # 分析影响因素
    print("\n各因素与综合评分的相关性：")
    for col in corr_cols[:-1]:
        corr = corr_matrix.loc[col, 'comprehensive_score']
        print(f"{col}: {corr:.3f}")

# 敏感性分析（权重调整）
def sensitivity_analysis(df):
    """敏感性分析"""
    # 不同权重组合
    weight_combinations = [
        {'name': '默认权重', 'weights': {'rating_norm': 0.3, 'completion_rate_norm': 0.25, 'interaction_rate_norm': 0.2, 'repurchase_rate_norm': 0.15, 'student_count_norm': 0.1}},
        {'name': '评分权重增加', 'weights': {'rating_norm': 0.4, 'completion_rate_norm': 0.2, 'interaction_rate_norm': 0.15, 'repurchase_rate_norm': 0.15, 'student_count_norm': 0.1}},
        {'name': '完课率权重增加', 'weights': {'rating_norm': 0.25, 'completion_rate_norm': 0.35, 'interaction_rate_norm': 0.15, 'repurchase_rate_norm': 0.15, 'student_count_norm': 0.1}},
        {'name': '互动率权重增加', 'weights': {'rating_norm': 0.25, 'completion_rate_norm': 0.2, 'interaction_rate_norm': 0.3, 'repurchase_rate_norm': 0.15, 'student_count_norm': 0.1}},
        {'name': '复购率权重增加', 'weights': {'rating_norm': 0.25, 'completion_rate_norm': 0.2, 'interaction_rate_norm': 0.15, 'repurchase_rate_norm': 0.3, 'student_count_norm': 0.1}}
    ]
    
    # 计算不同权重下的评分
    results = []
    for combo in weight_combinations:
        weighted_df, _ = calculate_comprehensive_score(df.copy(), combo['weights'])
        for _, row in weighted_df.iterrows():
            results.append({
                'teacher_id': row['teacher_id'],
                'weight_scenario': combo['name'],
                'comprehensive_score': row['comprehensive_score']
            })
    
    # 可视化
    results_df = pd.DataFrame(results)
    plt.figure(figsize=(15, 8))
    sns.lineplot(data=results_df, x='weight_scenario', y='comprehensive_score', hue='teacher_id', marker='o')
    plt.title('不同权重组合下的教师评分')
    plt.ylabel('综合评分')
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/sensitivity_analysis.png')
    plt.show()

# 生成教师评价报告
def generate_teacher_report(merged_df):
    """生成教师评价报告"""
    print("\n教师评价详细报告：")
    
    for _, row in merged_df.iterrows():
        print(f"\n=== {row['teacher_name']} ({row['subject']}) ===")
        print(f"综合评分: {row['comprehensive_score']:.2f} (排名: 第{row['rank']}名)")
        print(f"评分: {row['rating']:.2f}")
        print(f"完课率: {row['completion_rate']:.2f} ({row['completion_rate']*100:.1f}%)")
        print(f"互动率: {row['interaction_rate']:.2f} ({row['interaction_rate']*100:.1f}%)")
        print(f"复购率: {row['repurchase_rate']:.2f} ({row['repurchase_rate']*100:.1f}%)")
        print(f"学生人数: {row['student_count']}")
        print(f"课程数: {row['course_count']}")
        print(f"教学年限: {row['teaching_years']}年")
        
        # 优势分析
        strengths = []
        if row['rating'] > merged_df['rating'].mean():
            strengths.append('评分较高')
        if row['completion_rate'] > merged_df['completion_rate'].mean():
            strengths.append('完课率较高')
        if row['interaction_rate'] > merged_df['interaction_rate'].mean():
            strengths.append('互动率较高')
        if row['repurchase_rate'] > merged_df['repurchase_rate'].mean():
            strengths.append('复购率较高')
        
        if strengths:
            print(f"优势: {', '.join(strengths)}")
        
        # 改进建议
        improvements = []
        if row['rating'] < merged_df['rating'].mean():
            improvements.append('提升教学质量，提高学生评分')
        if row['completion_rate'] < merged_df['completion_rate'].mean():
            improvements.append('优化课程内容，提高完课率')
        if row['interaction_rate'] < merged_df['interaction_rate'].mean():
            improvements.append('增加课堂互动，提高互动率')
        if row['repurchase_rate'] < merged_df['repurchase_rate'].mean():
            improvements.append('提升课程价值，提高复购率')
        
        if improvements:
            print(f"改进建议: {', '.join(improvements)}")

# 主函数
def main():
    print("项目9: 教师授课质量多维度综合评分模型")
    print("=" * 60)
    
    # 生成数据
    print("1. 生成模拟数据...")
    teachers_df = generate_teacher_data()
    evaluation_df = generate_evaluation_data(teachers_df)
    print(f"生成教师数：{len(teachers_df)}")
    
    # 数据预处理
    print("\n2. 数据预处理和标准化...")
    processed_df = preprocess_data(evaluation_df)
    
    # 计算综合评分
    print("\n3. 计算综合评分...")
    scored_df, weights = calculate_comprehensive_score(processed_df)
    print("使用的权重：")
    for feature, weight in weights.items():
        print(f"  {feature}: {weight}")
    
    # 分析各维度得分
    print("\n4. 分析各维度得分...")
    analyze_dimension_scores(scored_df)
    
    # 分析教师排名
    print("\n5. 分析教师排名...")
    analyze_teacher_ranking(scored_df, teachers_df)
    
    # 分析各因素相关性
    print("\n6. 分析各因素相关性...")
    analyze_correlations(scored_df)
    
    # 敏感性分析
    print("\n7. 敏感性分析...")
    sensitivity_analysis(processed_df)
    
    # 生成教师评价报告
    print("\n8. 生成教师评价报告...")
    merged_df = scored_df.merge(teachers_df, on='teacher_id')
    merged_df['rank'] = merged_df['comprehensive_score'].rank(ascending=False, method='first').astype(int)
    merged_df = merged_df.sort_values('rank')
    generate_teacher_report(merged_df)
    
    print("\n分析完成！")
    print("生成的图表保存位置：/workspace/python-projects/")

if __name__ == "__main__":
    main()
