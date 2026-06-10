#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目10: 在线教育平台用户画像与精准运营策略
内容：年龄、地域、职业、偏好、设备、学习时段
Python技能：用户画像聚合、饼图、柱状图、分层策略
业务目标：输出可直接使用的精准运营方案
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

# 生成模拟用户数据
def generate_user_profile_data(num_users=1000):
    """生成用户画像数据"""
    # 年龄分布
    age_groups = ['18-24', '25-30', '31-35', '36-40', '41-45', '46+']
    age_probs = [0.3, 0.25, 0.2, 0.15, 0.08, 0.02]
    
    # 地域分布
    regions = ['北京', '上海', '广州', '深圳', '杭州', '成都', '武汉', '西安', '其他']
    region_probs = [0.15, 0.15, 0.1, 0.1, 0.08, 0.07, 0.07, 0.06, 0.22]
    
    # 职业分布
    occupations = ['学生', '职场新人', '中层管理', '技术工程师', '教师', '自由职业', '其他']
    occupation_probs = [0.3, 0.25, 0.15, 0.15, 0.08, 0.05, 0.02]
    
    # 学习偏好
    preferences = ['Python数据分析', 'Excel高级应用', '数据可视化', '统计分析', '商业智能', '机器学习']
    
    # 设备类型
    devices = ['PC', '移动端', '平板']
    device_probs = [0.4, 0.5, 0.1]
    
    # 学习时段
    study_periods = ['早晨(6-9点)', '上午(9-12点)', '下午(12-18点)', '晚上(18-21点)', '深夜(21-24点)']
    period_probs = [0.1, 0.2, 0.25, 0.35, 0.1]
    
    # 生成数据
    users = []
    for user_id in range(1, num_users + 1):
        # 基础信息
        age = np.random.choice(age_groups, p=age_probs)
        region = np.random.choice(regions, p=region_probs)
        occupation = np.random.choice(occupations, p=occupation_probs)
        device = np.random.choice(devices, p=device_probs)
        study_period = np.random.choice(study_periods, p=period_probs)
        
        # 学习偏好（1-3个）
        num_preferences = np.random.randint(1, 4)
        user_preferences = np.random.choice(preferences, size=num_preferences, replace=False)
        
        # 学习数据
        study_hours = np.random.normal(10, 5)
        study_hours = max(1, min(50, study_hours))
        
        course_count = np.random.randint(1, 10)
        completion_rate = np.random.uniform(0.3, 0.95)
        
        # 注册时间
        registration_date = datetime(2023, 1, 1) + timedelta(days=np.random.randint(0, 180))
        
        users.append({
            'user_id': user_id,
            'age_group': age,
            'region': region,
            'occupation': occupation,
            'device': device,
            'study_period': study_period,
            'preferences': user_preferences,
            'study_hours': study_hours,
            'course_count': course_count,
            'completion_rate': completion_rate,
            'registration_date': registration_date
        })
    
    return pd.DataFrame(users)

# 分析用户基本属性
def analyze_user_basic_attributes(df):
    """分析用户基本属性"""
    plt.figure(figsize=(15, 15))
    
    # 年龄分布
    plt.subplot(3, 2, 1)
    age_counts = df['age_group'].value_counts().sort_index()
    sns.barplot(x=age_counts.index, y=age_counts.values)
    plt.title('用户年龄分布')
    plt.ylabel('人数')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # 地域分布
    plt.subplot(3, 2, 2)
    region_counts = df['region'].value_counts()
    plt.pie(region_counts, labels=region_counts.index, autopct='%1.1f%%', startangle=90)
    plt.title('用户地域分布')
    
    # 职业分布
    plt.subplot(3, 2, 3)
    occupation_counts = df['occupation'].value_counts()
    sns.barplot(x=occupation_counts.index, y=occupation_counts.values)
    plt.title('用户职业分布')
    plt.ylabel('人数')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # 设备分布
    plt.subplot(3, 2, 4)
    device_counts = df['device'].value_counts()
    plt.pie(device_counts, labels=device_counts.index, autopct='%1.1f%%', startangle=90)
    plt.title('用户设备分布')
    
    # 学习时段分布
    plt.subplot(3, 2, 5)
    period_counts = df['study_period'].value_counts()
    sns.barplot(x=period_counts.index, y=period_counts.values)
    plt.title('用户学习时段分布')
    plt.ylabel('人数')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # 学习时长分布
    plt.subplot(3, 2, 6)
    sns.histplot(df['study_hours'], bins=20)
    plt.title('用户月学习时长分布')
    plt.xlabel('月学习时长（小时）')
    plt.ylabel('人数')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/user_basic_attributes.png')
    plt.show()

# 分析学习偏好
def analyze_learning_preferences(df):
    """分析学习偏好"""
    # 提取所有偏好
    all_preferences = []
    for prefs in df['preferences']:
        all_preferences.extend(prefs)
    
    # 统计偏好
    preference_counts = pd.Series(all_preferences).value_counts()
    
    plt.figure(figsize=(12, 6))
    sns.barplot(x=preference_counts.index, y=preference_counts.values)
    plt.title('用户学习偏好分布')
    plt.ylabel('选择人数')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/learning_preferences.png')
    plt.show()
    
    print("\n学习偏好分析：")
    for pref, count in preference_counts.items():
        percentage = (count / len(df)) * 100
        print(f"{pref}: {count}人 ({percentage:.1f}%)")

# 分析不同属性的学习行为
def analyze_behavior_by_attributes(df):
    """分析不同属性的学习行为"""
    plt.figure(figsize=(15, 12))
    
    # 不同年龄组的学习时长
    plt.subplot(2, 2, 1)
    sns.boxplot(data=df, x='age_group', y='study_hours')
    plt.title('不同年龄组的学习时长')
    plt.ylabel('月学习时长（小时）')
    plt.xticks(rotation=45)
    
    # 不同职业的完课率
    plt.subplot(2, 2, 2)
    sns.boxplot(data=df, x='occupation', y='completion_rate')
    plt.title('不同职业的完课率')
    plt.ylabel('完课率')
    plt.xticks(rotation=45)
    
    # 不同设备的课程数
    plt.subplot(2, 2, 3)
    sns.boxplot(data=df, x='device', y='course_count')
    plt.title('不同设备的课程数')
    plt.ylabel('课程数')
    
    # 不同学习时段的学习时长
    plt.subplot(2, 2, 4)
    sns.boxplot(data=df, x='study_period', y='study_hours')
    plt.title('不同学习时段的学习时长')
    plt.ylabel('月学习时长（小时）')
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/behavior_by_attributes.png')
    plt.show()

# 用户分层
def user_segmentation(df):
    """用户分层"""
    # 基于学习行为分层
    segments = []
    for _, user in df.iterrows():
        study_hours = user['study_hours']
        completion_rate = user['completion_rate']
        course_count = user['course_count']
        
        if study_hours >= 15 and completion_rate >= 0.8 and course_count >= 5:
            segment = '高价值用户'
        elif study_hours >= 10 and completion_rate >= 0.6 and course_count >= 3:
            segment = '活跃用户'
        elif study_hours >= 5 and completion_rate >= 0.4 and course_count >= 2:
            segment = '潜力用户'
        else:
            segment = '普通用户'
        
        segments.append(segment)
    
    df['segment'] = segments
    return df

# 分析用户分层
def analyze_user_segments(df):
    """分析用户分层"""
    plt.figure(figsize=(12, 8))
    
    # 分层分布
    segment_counts = df['segment'].value_counts()
    plt.subplot(1, 2, 1)
    plt.pie(segment_counts, labels=segment_counts.index, autopct='%1.1f%%', startangle=90)
    plt.title('用户分层分布')
    
    # 各分层的学习指标
    plt.subplot(1, 2, 2)
    segment_metrics = df.groupby('segment').agg({
        'study_hours': 'mean',
        'completion_rate': 'mean',
        'course_count': 'mean'
    }).reset_index()
    
    metrics = ['study_hours', 'completion_rate', 'course_count']
    metric_names = ['平均学习时长', '平均完课率', '平均课程数']
    
    for i, (metric, name) in enumerate(zip(metrics, metric_names), 1):
        plt.figure(figsize=(10, 6))
        sns.barplot(data=segment_metrics, x='segment', y=metric)
        plt.title(f'各分层的{name}')
        plt.ylabel(name)
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(f'/workspace/python-projects/segment_{metric}.png')
        plt.show()
    
    print("\n用户分层分析：")
    for segment, count in segment_counts.items():
        percentage = (count / len(df)) * 100
        print(f"{segment}: {count}人 ({percentage:.1f}%)")

# 生成精准运营策略
def generate_operation_strategy(df):
    """生成精准运营策略"""
    print("\n精准运营策略：")
    
    # 按分层制定策略
    segments = df['segment'].unique()
    
    for segment in segments:
        segment_data = df[df['segment'] == segment]
        
        print(f"\n=== {segment} ===")
        print(f"用户数：{len(segment_data)}")
        
        # 分析该分层的特征
        age_dist = segment_data['age_group'].value_counts().index[0]
        occupation_dist = segment_data['occupation'].value_counts().index[0]
        device_dist = segment_data['device'].value_counts().index[0]
        period_dist = segment_data['study_period'].value_counts().index[0]
        
        # 学习偏好
        all_prefs = []
        for prefs in segment_data['preferences']:
            all_prefs.extend(prefs)
        top_pref = pd.Series(all_prefs).value_counts().index[0]
        
        print(f"主要特征：")
        print(f"  年龄：{age_dist}")
        print(f"  职业：{occupation_dist}")
        print(f"  设备：{device_dist}")
        print(f"  学习时段：{period_dist}")
        print(f"  学习偏好：{top_pref}")
        
        # 运营策略
        if segment == '高价值用户':
            print("运营策略：")
            print("  1. 提供专属客服和学习顾问")
            print("  2. 推送高级课程和VIP内容")
            print("  3. 邀请参与课程设计和测试")
            print("  4. 提供学习认证和职业推荐")
            print("  5. 定期举办线下交流活动")
        elif segment == '活跃用户':
            print("运营策略：")
            print("  1. 推送个性化课程推荐")
            print("  2. 提供学习进度分析和建议")
            print("  3. 组织学习小组和线上讨论")
            print("  4. 提供阶段性学习奖励")
            print("  5. 邀请分享学习经验")
        elif segment == '潜力用户':
            print("运营策略：")
            print("  1. 提供入门课程和学习路径")
            print("  2. 发送学习提醒和激励")
            print("  3. 提供学习技巧指导")
            print("  4. 组织新手训练营")
            print("  5. 提供首单优惠和折扣")
        else:
            print("运营策略：")
            print("  1. 简化注册和学习流程")
            print("  2. 提供免费试学内容")
            print("  3. 发送个性化课程推荐")
            print("  4. 提供学习目标设定指导")
            print("  5. 定期发送平台活动通知")

# 分析地域差异
def analyze_region_differences(df):
    """分析地域差异"""
    plt.figure(figsize=(15, 8))
    
    # 各地区的学习时长
    region_metrics = df.groupby('region').agg({
        'study_hours': 'mean',
        'completion_rate': 'mean',
        'course_count': 'mean'
    }).reset_index()
    
    # 学习时长地域差异
    plt.subplot(1, 3, 1)
    region_metrics_sorted = region_metrics.sort_values('study_hours', ascending=False)
    sns.barplot(x=region_metrics_sorted['region'], y=region_metrics_sorted['study_hours'])
    plt.title('各地区平均学习时长')
    plt.ylabel('学习时长（小时）')
    plt.xticks(rotation=45)
    
    # 完课率地域差异
    plt.subplot(1, 3, 2)
    region_metrics_sorted = region_metrics.sort_values('completion_rate', ascending=False)
    sns.barplot(x=region_metrics_sorted['region'], y=region_metrics_sorted['completion_rate'])
    plt.title('各地区平均完课率')
    plt.ylabel('完课率')
    plt.xticks(rotation=45)
    
    # 课程数地域差异
    plt.subplot(1, 3, 3)
    region_metrics_sorted = region_metrics.sort_values('course_count', ascending=False)
    sns.barplot(x=region_metrics_sorted['region'], y=region_metrics_sorted['course_count'])
    plt.title('各地区平均课程数')
    plt.ylabel('课程数')
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/region_differences.png')
    plt.show()

# 主函数
def main():
    print("项目10: 在线教育平台用户画像与精准运营策略")
    print("=" * 60)
    
    # 生成数据
    print("1. 生成模拟数据...")
    df = generate_user_profile_data(num_users=1000)
    print(f"生成用户数：{len(df)}")
    
    # 分析用户基本属性
    print("\n2. 分析用户基本属性...")
    analyze_user_basic_attributes(df)
    
    # 分析学习偏好
    print("\n3. 分析学习偏好...")
    analyze_learning_preferences(df)
    
    # 分析不同属性的学习行为
    print("\n4. 分析不同属性的学习行为...")
    analyze_behavior_by_attributes(df)
    
    # 用户分层
    print("\n5. 用户分层...")
    df = user_segmentation(df)
    
    # 分析用户分层
    print("\n6. 分析用户分层...")
    analyze_user_segments(df)
    
    # 分析地域差异
    print("\n7. 分析地域差异...")
    analyze_region_differences(df)
    
    # 生成精准运营策略
    print("\n8. 生成精准运营策略...")
    generate_operation_strategy(df)
    
    print("\n分析完成！")
    print("生成的图表保存位置：/workspace/python-projects/")

if __name__ == "__main__":
    main()
