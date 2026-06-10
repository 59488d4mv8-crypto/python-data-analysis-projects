#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目2: 课程学习完成度与dropout流失预测
内容：学习进度、退出节点、完课率、用户流失特征
Python技能：数据清洗、特征工程、漏斗图、热力图
业务目标：找出课程最容易流失的章节
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

# 生成模拟课程数据
def generate_course_data():
    """生成课程章节数据"""
    courses = [
        {
            'course_id': 1,
            'course_name': 'Python数据分析基础',
            'chapters': [
                {'chapter_id': 1, 'chapter_name': 'Python基础语法', 'duration': 60, 'difficulty': 1},
                {'chapter_id': 2, 'chapter_name': 'NumPy数组操作', 'duration': 90, 'difficulty': 2},
                {'chapter_id': 3, 'chapter_name': 'Pandas数据处理', 'duration': 120, 'difficulty': 3},
                {'chapter_id': 4, 'chapter_name': '数据可视化', 'duration': 90, 'difficulty': 2},
                {'chapter_id': 5, 'chapter_name': '实战项目', 'duration': 150, 'difficulty': 4}
            ]
        },
        {
            'course_id': 2,
            'course_name': 'Excel高级应用',
            'chapters': [
                {'chapter_id': 1, 'chapter_name': '函数与公式', 'duration': 60, 'difficulty': 2},
                {'chapter_id': 2, 'chapter_name': '数据透视表', 'duration': 90, 'difficulty': 3},
                {'chapter_id': 3, 'chapter_name': '图表制作', 'duration': 60, 'difficulty': 2},
                {'chapter_id': 4, 'chapter_name': '宏与VBA', 'duration': 120, 'difficulty': 4},
                {'chapter_id': 5, 'chapter_name': '案例分析', 'duration': 90, 'difficulty': 3}
            ]
        }
    ]
    return courses

# 生成用户学习数据
def generate_learning_data(courses, num_users=1000):
    """生成用户学习数据"""
    learning_records = []
    user_id = 1
    
    for course in courses:
        course_id = course['course_id']
        chapters = course['chapters']
        
        for _ in range(num_users):
            # 生成用户特征
            user_type = np.random.choice(['学生', '职场人士', '教师'], p=[0.6, 0.3, 0.1])
            prior_knowledge = np.random.randint(1, 5)
            
            # 模拟学习行为
            current_chapter = 0
            completed_chapters = []
            drop_out = False
            
            for chapter in chapters:
                chapter_id = chapter['chapter_id']
                difficulty = chapter['difficulty']
                
                # 计算完成概率（基于难度和用户特征）
                base_prob = 0.8
                difficulty_factor = 1 - (difficulty * 0.1)
                knowledge_factor = prior_knowledge / 5
                
                if user_type == '学生':
                    user_factor = 1.0
                elif user_type == '职场人士':
                    user_factor = 0.8
                else:
                    user_factor = 1.2
                
                completion_prob = base_prob * difficulty_factor * knowledge_factor * user_factor
                completion_prob = max(0.1, min(0.95, completion_prob))
                
                # 决定是否完成当前章节
                if np.random.random() < completion_prob:
                    completed_chapters.append(chapter_id)
                    current_chapter = chapter_id
                    
                    # 学习时长（基于章节时长）
                    study_time = int(np.random.normal(chapter['duration'], chapter['duration'] * 0.2))
                    study_time = max(1, study_time)
                    
                    # 完成时间
                    completion_time = datetime(2023, 6, 1) + timedelta(days=np.random.randint(0, 30))
                    
                    learning_records.append({
                        'user_id': user_id,
                        'course_id': course_id,
                        'course_name': course['course_name'],
                        'chapter_id': chapter_id,
                        'chapter_name': chapter['chapter_name'],
                        'completed': True,
                        'study_time': study_time,
                        'completion_time': completion_time,
                        'user_type': user_type,
                        'prior_knowledge': prior_knowledge
                    })
                else:
                    # 用户流失
                    drop_out = True
                    drop_out_chapter = chapter_id
                    
                    # 记录未完成的学习记录
                    study_time = int(np.random.normal(chapter['duration'] * 0.3, chapter['duration'] * 0.1))
                    study_time = max(1, study_time)
                    
                    drop_out_time = datetime(2023, 6, 1) + timedelta(days=np.random.randint(0, 30))
                    
                    learning_records.append({
                        'user_id': user_id,
                        'course_id': course_id,
                        'course_name': course['course_name'],
                        'chapter_id': chapter_id,
                        'chapter_name': chapter['chapter_name'],
                        'completed': False,
                        'study_time': study_time,
                        'completion_time': drop_out_time,
                        'user_type': user_type,
                        'prior_knowledge': prior_knowledge,
                        'drop_out': True
                    })
                    break
            
            # 如果用户完成了所有章节
            if not drop_out:
                learning_records.append({
                    'user_id': user_id,
                    'course_id': course_id,
                    'course_name': course['course_name'],
                    'chapter_id': 0,  # 标记为完成整个课程
                    'chapter_name': '课程完成',
                    'completed': True,
                    'study_time': 0,
                    'completion_time': datetime(2023, 6, 1) + timedelta(days=np.random.randint(0, 30)),
                    'user_type': user_type,
                    'prior_knowledge': prior_knowledge,
                    'course_completed': True
                })
            
            user_id += 1
    
    return pd.DataFrame(learning_records)

# 分析课程完成度
def analyze_course_completion(learning_df):
    """分析课程完成度"""
    plt.figure(figsize=(15, 8))
    
    # 按课程分组分析
    courses = learning_df['course_name'].unique()
    
    for i, course in enumerate(courses, 1):
        course_data = learning_df[learning_df['course_name'] == course]
        
        # 计算各章节完成率
        chapter_completion = course_data.groupby(['chapter_id', 'chapter_name'])['completed'].mean() * 100
        chapter_completion = chapter_completion.reset_index()
        
        # 按章节顺序排序
        chapter_completion = chapter_completion.sort_values('chapter_id')
        
        # 绘制漏斗图
        plt.subplot(len(courses), 1, i)
        
        # 计算累计完成率
        cumulative_completion = []
        total_users = len(course_data['user_id'].unique())
        current_users = total_users
        
        for _, row in chapter_completion.iterrows():
            chapter_users = len(course_data[course_data['chapter_id'] == row['chapter_id']]['user_id'].unique())
            current_users = int(current_users * (row['completed'] / 100))
            cumulative_completion.append(current_users)
        
        # 绘制漏斗图
        sns.barplot(x=chapter_completion['chapter_name'], y=cumulative_completion)
        plt.title(f'{course} - 学习完成漏斗')
        plt.ylabel('剩余用户数')
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/course_completion_funnel.png')
    plt.show()
    
    # 计算整体完课率
    for course in courses:
        course_data = learning_df[learning_df['course_name'] == course]
        total_users = len(course_data['user_id'].unique())
        completed_users = len(course_data[course_data.get('course_completed', False)]['user_id'].unique())
        completion_rate = (completed_users / total_users) * 100
        
        print(f"\n{course}:")
        print(f"总学习人数：{total_users}")
        print(f"完成人数：{completed_users}")
        print(f"完课率：{completion_rate:.1f}%")

# 分析流失节点
def analyze_dropout_nodes(learning_df):
    """分析流失节点"""
    plt.figure(figsize=(12, 8))
    
    # 找出流失记录
    dropout_data = learning_df[learning_df.get('drop_out', False)]
    
    # 按章节分析流失率
    dropout_by_chapter = dropout_data.groupby(['course_name', 'chapter_name']).size().reset_index(name='dropout_count')
    
    # 计算各课程的总用户数
    total_users_by_course = learning_df.groupby('course_name')['user_id'].nunique().to_dict()
    
    # 计算流失率
    dropout_by_chapter['total_users'] = dropout_by_chapter['course_name'].map(total_users_by_course)
    dropout_by_chapter['dropout_rate'] = (dropout_by_chapter['dropout_count'] / dropout_by_chapter['total_users']) * 100
    
    # 可视化
    sns.barplot(data=dropout_by_chapter, x='chapter_name', y='dropout_rate', hue='course_name')
    plt.title('各章节流失率对比')
    plt.ylabel('流失率 (%)')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/dropout_rates.png')
    plt.show()
    
    print("\n流失节点分析：")
    for course in learning_df['course_name'].unique():
        course_dropout = dropout_by_chapter[dropout_by_chapter['course_name'] == course]
        highest_dropout = course_dropout.loc[course_dropout['dropout_rate'].idxmax()]
        
        print(f"\n{course}:")
        print(f"最容易流失的章节：{highest_dropout['chapter_name']}")
        print(f"流失率：{highest_dropout['dropout_rate']:.1f}%")
        print(f"流失人数：{highest_dropout['dropout_count']}")

# 分析用户流失特征
def analyze_user_dropout_features(learning_df):
    """分析用户流失特征"""
    plt.figure(figsize=(15, 10))
    
    # 准备数据
    user_status = []
    
    for user_id in learning_df['user_id'].unique():
        user_data = learning_df[learning_df['user_id'] == user_id]
        course_name = user_data['course_name'].iloc[0]
        user_type = user_data['user_type'].iloc[0]
        prior_knowledge = user_data['prior_knowledge'].iloc[0]
        
        # 判断是否完成课程
        completed = 'course_completed' in user_data.columns and user_data['course_completed'].any()
        status = '完成' if completed else '流失'
        
        # 计算学习时长
        total_study_time = user_data['study_time'].sum()
        
        user_status.append({
            'user_id': user_id,
            'course_name': course_name,
            'user_type': user_type,
            'prior_knowledge': prior_knowledge,
            'status': status,
            'total_study_time': total_study_time
        })
    
    user_status_df = pd.DataFrame(user_status)
    
    # 用户类型分布
    plt.subplot(2, 2, 1)
    sns.countplot(data=user_status_df, x='user_type', hue='status')
    plt.title('不同用户类型的完成情况')
    plt.xticks(rotation=45)
    
    # 知识水平分布
    plt.subplot(2, 2, 2)
    sns.countplot(data=user_status_df, x='prior_knowledge', hue='status')
    plt.title('不同知识水平的完成情况')
    
    # 学习时长对比
    plt.subplot(2, 2, 3)
    sns.boxplot(data=user_status_df, x='status', y='total_study_time')
    plt.title('完成vs流失用户的学习时长对比')
    
    # 课程完成情况
    plt.subplot(2, 2, 4)
    sns.countplot(data=user_status_df, x='course_name', hue='status')
    plt.title('不同课程的完成情况')
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/user_dropout_features.png')
    plt.show()
    
    # 计算各特征的流失率
    print("\n用户特征分析：")
    
    # 按用户类型
    print("\n按用户类型：")
    for user_type in user_status_df['user_type'].unique():
        type_data = user_status_df[user_status_df['user_type'] == user_type]
        dropout_rate = (len(type_data[type_data['status'] == '流失']) / len(type_data)) * 100
        print(f"{user_type}：流失率 {dropout_rate:.1f}%")
    
    # 按知识水平
    print("\n按知识水平：")
    for knowledge in sorted(user_status_df['prior_knowledge'].unique()):
        knowledge_data = user_status_df[user_status_df['prior_knowledge'] == knowledge]
        dropout_rate = (len(knowledge_data[knowledge_data['status'] == '流失']) / len(knowledge_data)) * 100
        print(f"知识水平 {knowledge}：流失率 {dropout_rate:.1f}%")

# 生成热力图分析
def generate_heatmap_analysis(learning_df):
    """生成热力图分析"""
    # 准备数据
    heatmap_data = []
    
    for course in learning_df['course_name'].unique():
        course_data = learning_df[learning_df['course_name'] == course]
        chapters = course_data['chapter_name'].unique()
        
        for chapter in chapters:
            chapter_data = course_data[course_data['chapter_name'] == chapter]
            completion_rate = chapter_data['completed'].mean() * 100
            avg_study_time = chapter_data['study_time'].mean()
            
            # 获取章节难度（模拟数据）
            difficulty_map = {
                'Python基础语法': 1, 'NumPy数组操作': 2, 'Pandas数据处理': 3, '数据可视化': 2, '实战项目': 4,
                '函数与公式': 2, '数据透视表': 3, '图表制作': 2, '宏与VBA': 4, '案例分析': 3
            }
            difficulty = difficulty_map.get(chapter, 2)
            
            heatmap_data.append({
                'course': course,
                'chapter': chapter,
                'difficulty': difficulty,
                'completion_rate': completion_rate,
                'avg_study_time': avg_study_time
            })
    
    heatmap_df = pd.DataFrame(heatmap_data)
    
    # 创建透视表
    pivot_table = heatmap_df.pivot(index='chapter', columns='course', values='completion_rate')
    
    # 绘制热力图
    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot_table, annot=True, cmap='YlGnBu', fmt='.1f')
    plt.title('各章节完成率热力图')
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/chapter_completion_heatmap.png')
    plt.show()

# 主函数
def main():
    print("项目2: 课程学习完成度与dropout流失预测")
    print("=" * 60)
    
    # 生成数据
    print("1. 生成模拟数据...")
    courses = generate_course_data()
    learning_df = generate_learning_data(courses, num_users=500)
    
    print(f"生成学习记录：{len(learning_df)}")
    print(f"涉及课程：{len(learning_df['course_name'].unique())}")
    print(f"涉及用户：{len(learning_df['user_id'].unique())}")
    
    # 分析课程完成度
    print("\n2. 分析课程完成度...")
    analyze_course_completion(learning_df)
    
    # 分析流失节点
    print("\n3. 分析流失节点...")
    analyze_dropout_nodes(learning_df)
    
    # 分析用户流失特征
    print("\n4. 分析用户流失特征...")
    analyze_user_dropout_features(learning_df)
    
    # 生成热力图
    print("\n5. 生成热力图分析...")
    generate_heatmap_analysis(learning_df)
    
    print("\n分析完成！")
    print("生成的图表保存位置：/workspace/python-projects/")

if __name__ == "__main__":
    main()
