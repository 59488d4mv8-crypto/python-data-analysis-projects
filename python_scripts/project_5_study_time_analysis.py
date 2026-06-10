#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目5: 学生学习时长与成绩相关性分析
内容：学习时长、暂停次数、快进次数、章节测验分数
Python技能：相关性分析、散点图、箱线图、回归分析
业务目标：判断哪些行为影响成绩最大
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 生成模拟学生数据
def generate_student_data(num_students=500):
    """生成学生数据"""
    students = []
    for student_id in range(1, num_students + 1):
        # 学生基本信息
        student_type = np.random.choice(['学霸', '普通学生', '学渣'], p=[0.2, 0.6, 0.2])
        prior_knowledge = np.random.randint(1, 5)
        
        students.append({
            'student_id': student_id,
            'student_type': student_type,
            'prior_knowledge': prior_knowledge
        })
    return pd.DataFrame(students)

# 生成学习行为数据
def generate_learning_behavior(students_df, num_courses=5):
    """生成学习行为数据"""
    courses = ['Python数据分析', 'Excel高级应用', '数据可视化', '统计分析', '商业智能']
    behavior_data = []
    
    for _, student in students_df.iterrows():
        student_id = student['student_id']
        student_type = student['student_type']
        prior_knowledge = student['prior_knowledge']
        
        for course in courses:
            # 基于学生类型生成学习行为
            if student_type == '学霸':
                # 学习时长较长，暂停和快进较少
                total_study_time = int(np.random.normal(1200, 200))  # 分钟
                pause_count = int(np.random.normal(10, 3))
                fast_forward_count = int(np.random.normal(5, 2))
                # 成绩较高
                score = np.random.normal(85, 8)
            elif student_type == '普通学生':
                # 学习时长中等，暂停和快进适中
                total_study_time = int(np.random.normal(800, 150))
                pause_count = int(np.random.normal(15, 5))
                fast_forward_count = int(np.random.normal(10, 3))
                # 成绩中等
                score = np.random.normal(70, 10)
            else:
                # 学习时长较短，暂停和快进较多
                total_study_time = int(np.random.normal(400, 100))
                pause_count = int(np.random.normal(20, 5))
                fast_forward_count = int(np.random.normal(15, 4))
                # 成绩较低
                score = np.random.normal(55, 10)
            
            # 加入知识水平的影响
            knowledge_factor = prior_knowledge / 4
            total_study_time = int(total_study_time * (0.8 + knowledge_factor * 0.4))
            score = score * (0.8 + knowledge_factor * 0.4)
            
            # 确保数值合理
            total_study_time = max(100, total_study_time)
            pause_count = max(0, pause_count)
            fast_forward_count = max(0, fast_forward_count)
            score = max(0, min(100, score))
            
            # 生成学习开始时间
            start_date = datetime(2023, 1, 1) + timedelta(days=np.random.randint(0, 180))
            
            behavior_data.append({
                'student_id': student_id,
                'course': course,
                'total_study_time': total_study_time,
                'pause_count': pause_count,
                'fast_forward_count': fast_forward_count,
                'score': score,
                'start_date': start_date,
                'student_type': student_type,
                'prior_knowledge': prior_knowledge
            })
    
    return pd.DataFrame(behavior_data)

# 分析学习时长与成绩关系
def analyze_study_time_score(behavior_df):
    """分析学习时长与成绩关系"""
    plt.figure(figsize=(15, 8))
    
    # 散点图
    plt.subplot(1, 2, 1)
    sns.scatterplot(data=behavior_df, x='total_study_time', y='score', alpha=0.6)
    plt.title('学习时长与成绩关系')
    plt.xlabel('学习时长（分钟）')
    plt.ylabel('成绩')
    
    # 回归线
    x = behavior_df['total_study_time'].values.reshape(-1, 1)
    y = behavior_df['score'].values
    model = LinearRegression()
    model.fit(x, y)
    y_pred = model.predict(x)
    plt.plot(behavior_df['total_study_time'], y_pred, color='red', linewidth=2, label=f'R² = {model.score(x, y):.2f}')
    plt.legend()
    
    # 学习时长分布
    plt.subplot(1, 2, 2)
    sns.histplot(behavior_df['total_study_time'], bins=30)
    plt.title('学习时长分布')
    plt.xlabel('学习时长（分钟）')
    plt.ylabel('频数')
    
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/study_time_score.png')
    plt.show()
    
    # 计算相关性
    correlation = behavior_df['total_study_time'].corr(behavior_df['score'])
    print(f"\n学习时长与成绩的相关系数：{correlation:.3f}")

# 分析暂停次数与成绩关系
def analyze_pause_score(behavior_df):
    """分析暂停次数与成绩关系"""
    plt.figure(figsize=(15, 8))
    
    # 散点图
    plt.subplot(1, 2, 1)
    sns.scatterplot(data=behavior_df, x='pause_count', y='score', alpha=0.6)
    plt.title('暂停次数与成绩关系')
    plt.xlabel('暂停次数')
    plt.ylabel('成绩')
    
    # 箱线图
    plt.subplot(1, 2, 2)
    sns.boxplot(data=behavior_df, x=pd.cut(behavior_df['pause_count'], bins=[0, 10, 20, 30, 40]), y='score')
    plt.title('不同暂停次数区间的成绩分布')
    plt.xlabel('暂停次数区间')
    plt.ylabel('成绩')
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/pause_score.png')
    plt.show()
    
    # 计算相关性
    correlation = behavior_df['pause_count'].corr(behavior_df['score'])
    print(f"暂停次数与成绩的相关系数：{correlation:.3f}")

# 分析快进次数与成绩关系
def analyze_fast_forward_score(behavior_df):
    """分析快进次数与成绩关系"""
    plt.figure(figsize=(15, 8))
    
    # 散点图
    plt.subplot(1, 2, 1)
    sns.scatterplot(data=behavior_df, x='fast_forward_count', y='score', alpha=0.6)
    plt.title('快进次数与成绩关系')
    plt.xlabel('快进次数')
    plt.ylabel('成绩')
    
    # 箱线图
    plt.subplot(1, 2, 2)
    sns.boxplot(data=behavior_df, x=pd.cut(behavior_df['fast_forward_count'], bins=[0, 5, 10, 15, 20, 25]), y='score')
    plt.title('不同快进次数区间的成绩分布')
    plt.xlabel('快进次数区间')
    plt.ylabel('成绩')
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/fast_forward_score.png')
    plt.show()
    
    # 计算相关性
    correlation = behavior_df['fast_forward_count'].corr(behavior_df['score'])
    print(f"快进次数与成绩的相关系数：{correlation:.3f}")

# 多变量相关性分析
def analyze_multivariate_correlation(behavior_df):
    """多变量相关性分析"""
    # 选择数值型变量
    numeric_cols = ['total_study_time', 'pause_count', 'fast_forward_count', 'score', 'prior_knowledge']
    corr_matrix = behavior_df[numeric_cols].corr()
    
    # 热力图
    plt.figure(figsize=(12, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('多变量相关性热力图')
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/correlation_heatmap.png')
    plt.show()
    
    print("\n多变量相关性分析：")
    print(corr_matrix)

# 回归分析
def regression_analysis(behavior_df):
    """回归分析"""
    # 准备数据
    X = behavior_df[['total_study_time', 'pause_count', 'fast_forward_count', 'prior_knowledge']]
    y = behavior_df['score']
    
    # 线性回归
    model = LinearRegression()
    model.fit(X, y)
    
    # 计算R²
    r2 = model.score(X, y)
    
    # 系数
    coefficients = pd.DataFrame({
        '变量': X.columns,
        '系数': model.coef_,
        '绝对值': abs(model.coef_)
    })
    coefficients = coefficients.sort_values('绝对值', ascending=False)
    
    print(f"\n回归分析结果：")
    print(f"R² = {r2:.3f}")
    print("\n变量重要性排序：")
    print(coefficients)
    
    # 可视化系数
    plt.figure(figsize=(12, 6))
    sns.barplot(x='变量', y='系数', data=coefficients)
    plt.title('各变量对成绩的影响系数')
    plt.xticks(rotation=45)
    plt.axhline(y=0, color='r', linestyle='--')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/regression_coefficients.png')
    plt.show()

# 分析不同学生类型的学习行为
def analyze_student_type_behavior(behavior_df):
    """分析不同学生类型的学习行为"""
    plt.figure(figsize=(15, 10))
    
    # 学习时长
    plt.subplot(2, 2, 1)
    sns.boxplot(data=behavior_df, x='student_type', y='total_study_time')
    plt.title('不同学生类型的学习时长')
    
    # 暂停次数
    plt.subplot(2, 2, 2)
    sns.boxplot(data=behavior_df, x='student_type', y='pause_count')
    plt.title('不同学生类型的暂停次数')
    
    # 快进次数
    plt.subplot(2, 2, 3)
    sns.boxplot(data=behavior_df, x='student_type', y='fast_forward_count')
    plt.title('不同学生类型的快进次数')
    
    # 成绩
    plt.subplot(2, 2, 4)
    sns.boxplot(data=behavior_df, x='student_type', y='score')
    plt.title('不同学生类型的成绩')
    
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/student_type_behavior.png')
    plt.show()
    
    # 统计分析
    print("\n不同学生类型的统计分析：")
    for student_type in behavior_df['student_type'].unique():
        type_data = behavior_df[behavior_df['student_type'] == student_type]
        print(f"\n{student_type}：")
        print(f"  平均学习时长：{type_data['total_study_time'].mean():.1f}分钟")
        print(f"  平均暂停次数：{type_data['pause_count'].mean():.1f}次")
        print(f"  平均快进次数：{type_data['fast_forward_count'].mean():.1f}次")
        print(f"  平均成绩：{type_data['score'].mean():.1f}分")

# 分析知识水平的影响
def analyze_prior_knowledge(behavior_df):
    """分析知识水平的影响"""
    plt.figure(figsize=(12, 6))
    
    # 知识水平与成绩关系
    sns.boxplot(data=behavior_df, x='prior_knowledge', y='score')
    plt.title('不同知识水平的成绩分布')
    plt.xlabel('知识水平')
    plt.ylabel('成绩')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/prior_knowledge_score.png')
    plt.show()

# 主函数
def main():
    print("项目5: 学生学习时长与成绩相关性分析")
    print("=" * 60)
    
    # 生成数据
    print("1. 生成模拟数据...")
    students_df = generate_student_data(num_students=500)
    behavior_df = generate_learning_behavior(students_df)
    
    print(f"生成学生数：{len(students_df)}")
    print(f"生成学习记录：{len(behavior_df)}")
    print(f"涉及课程：{len(behavior_df['course'].unique())}")
    
    # 分析学习时长与成绩关系
    print("\n2. 分析学习时长与成绩关系...")
    analyze_study_time_score(behavior_df)
    
    # 分析暂停次数与成绩关系
    print("\n3. 分析暂停次数与成绩关系...")
    analyze_pause_score(behavior_df)
    
    # 分析快进次数与成绩关系
    print("\n4. 分析快进次数与成绩关系...")
    analyze_fast_forward_score(behavior_df)
    
    # 多变量相关性分析
    print("\n5. 多变量相关性分析...")
    analyze_multivariate_correlation(behavior_df)
    
    # 回归分析
    print("\n6. 回归分析...")
    regression_analysis(behavior_df)
    
    # 分析不同学生类型的学习行为
    print("\n7. 分析不同学生类型的学习行为...")
    analyze_student_type_behavior(behavior_df)
    
    # 分析知识水平的影响
    print("\n8. 分析知识水平的影响...")
    analyze_prior_knowledge(behavior_df)
    
    print("\n分析完成！")
    print("生成的图表保存位置：/workspace/python-projects/")

if __name__ == "__main__":
    main()
