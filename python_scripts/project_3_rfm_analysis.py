#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目3: 在线教育用户RFM价值分层分析
内容：R（最近学习）、F（学习频次）、M（学习时长/付费）用户分层
Python技能：RFM分箱、用户标签、可视化分组
业务目标：识别高价值用户、沉睡用户、潜力用户
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
def generate_user_data(num_users=1000):
    """生成用户数据"""
    users = []
    for user_id in range(1, num_users + 1):
        # 用户基本信息
        user_type = np.random.choice(['学生', '职场人士', '教师'], p=[0.6, 0.3, 0.1])
        registration_date = datetime(2023, 1, 1) + timedelta(days=np.random.randint(0, 180))
        
        users.append({
            'user_id': user_id,
            'user_type': user_type,
            'registration_date': registration_date
        })
    return pd.DataFrame(users)

# 生成学习记录数据
def generate_learning_records(users_df, start_date=datetime(2023, 1, 1), end_date=datetime(2023, 6, 30)):
    """生成学习记录数据"""
    records = []
    date_range = pd.date_range(start=start_date, end=end_date)
    
    for _, user in users_df.iterrows():
        user_id = user['user_id']
        user_type = user['user_type']
        registration_date = user['registration_date']
        
        # 基于用户类型生成学习行为
        if user_type == '学生':
            # 学生学习频率较高
            study_days = int(np.random.normal(45, 15))
            avg_study_time = int(np.random.normal(60, 20))
        elif user_type == '职场人士':
            # 职场人士学习频率中等
            study_days = int(np.random.normal(30, 10))
            avg_study_time = int(np.random.normal(45, 15))
        else:
            # 教师学习频率较低
            study_days = int(np.random.normal(20, 8))
            avg_study_time = int(np.random.normal(30, 10))
        
        study_days = max(1, min(180, study_days))
        avg_study_time = max(10, min(180, avg_study_time))
        
        # 生成学习记录
        study_dates = np.random.choice(date_range, size=study_days, replace=False)
        study_dates = sorted(study_dates)
        
        for study_date in study_dates:
            # 学习时长
            study_time = int(np.random.normal(avg_study_time, avg_study_time * 0.3))
            study_time = max(5, study_time)
            
            # 课程类型
            course_type = np.random.choice(['Python', 'Excel', '数据可视化', '统计分析', '商业智能'])
            
            # 是否付费（有一定概率）
            is_paid = np.random.random() < 0.3
            payment_amount = np.random.uniform(99, 999) if is_paid else 0
            
            records.append({
                'user_id': user_id,
                'study_date': study_date,
                'study_time': study_time,
                'course_type': course_type,
                'is_paid': is_paid,
                'payment_amount': payment_amount
            })
    
    return pd.DataFrame(records)

# 计算RFM指标
def calculate_rfm_metrics(users_df, learning_df, current_date=datetime(2023, 7, 1)):
    """计算RFM指标"""
    rfm_data = []
    
    for _, user in users_df.iterrows():
        user_id = user['user_id']
        user_data = learning_df[learning_df['user_id'] == user_id]
        
        if len(user_data) == 0:
            # 无学习记录的用户
            recency = (current_date - user['registration_date']).days
            frequency = 0
            monetary = 0
        else:
            # 计算最近学习时间（Recency）
            last_study_date = user_data['study_date'].max()
            recency = (current_date - last_study_date).days
            
            # 计算学习频次（Frequency）
            frequency = len(user_data)
            
            # 计算学习时长/付费金额（Monetary）
            total_study_time = user_data['study_time'].sum()
            total_payment = user_data['payment_amount'].sum()
            
            # 综合考虑学习时长和付费金额
            monetary = total_study_time + (total_payment * 0.1)  # 付费金额加权
        
        rfm_data.append({
            'user_id': user_id,
            'recency': recency,
            'frequency': frequency,
            'monetary': monetary
        })
    
    rfm_df = pd.DataFrame(rfm_data)
    return rfm_df

# RFM分箱
def rfm_scoring(rfm_df):
    """RFM分箱评分"""
    # 分箱（1-5分，5分最好）
    # Recency：越小越好
    rfm_df['r_score'] = pd.qcut(rfm_df['recency'], 5, labels=[5, 4, 3, 2, 1])
    rfm_df['r_score'] = rfm_df['r_score'].astype(int)
    
    # Frequency：越大越好
    rfm_df['f_score'] = pd.qcut(rfm_df['frequency'], 5, labels=[1, 2, 3, 4, 5])
    rfm_df['f_score'] = rfm_df['f_score'].astype(int)
    
    # Monetary：越大越好
    rfm_df['m_score'] = pd.qcut(rfm_df['monetary'], 5, labels=[1, 2, 3, 4, 5])
    rfm_df['m_score'] = rfm_df['m_score'].astype(int)
    
    # 计算总分
    rfm_df['rfm_score'] = rfm_df['r_score'] + rfm_df['f_score'] + rfm_df['m_score']
    
    return rfm_df

# 用户分层
def user_segmentation(rfm_df):
    """用户分层"""
    # 定义分层规则
    def get_segment(row):
        r = row['r_score']
        f = row['f_score']
        m = row['m_score']
        
        # 高价值用户
        if r >= 4 and f >= 4 and m >= 4:
            return '高价值用户'
        # 潜力用户
        elif r >= 3 and f >= 3 and m >= 3:
            return '潜力用户'
        # 一般用户
        elif r >= 2 and f >= 2 and m >= 2:
            return '一般用户'
        # 低活跃用户
        elif r <= 2 and f <= 2:
            return '低活跃用户'
        # 沉睡用户
        elif r <= 1:
            return '沉睡用户'
        # 新用户
        elif f == 1:
            return '新用户'
        else:
            return '一般用户'
    
    rfm_df['segment'] = rfm_df.apply(get_segment, axis=1)
    return rfm_df

# 分析RFM分布
def analyze_rfm_distribution(rfm_df):
    """分析RFM分布"""
    plt.figure(figsize=(15, 10))
    
    # RFM分布图
    plt.subplot(2, 2, 1)
    sns.histplot(rfm_df['recency'], bins=20)
    plt.title('Recency分布')
    plt.xlabel('最近学习天数')
    
    plt.subplot(2, 2, 2)
    sns.histplot(rfm_df['frequency'], bins=20)
    plt.title('Frequency分布')
    plt.xlabel('学习频次')
    
    plt.subplot(2, 2, 3)
    sns.histplot(rfm_df['monetary'], bins=20)
    plt.title('Monetary分布')
    plt.xlabel('学习价值')
    
    plt.subplot(2, 2, 4)
    sns.histplot(rfm_df['rfm_score'], bins=15)
    plt.title('RFM总分分布')
    plt.xlabel('RFM总分')
    
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/rfm_distribution.png')
    plt.show()

# 分析用户分层
def analyze_user_segments(rfm_df):
    """分析用户分层"""
    plt.figure(figsize=(15, 8))
    
    # 分层用户数量
    segment_counts = rfm_df['segment'].value_counts()
    segment_percentage = segment_counts / len(rfm_df) * 100
    
    # 饼图
    plt.subplot(1, 2, 1)
    plt.pie(segment_percentage, labels=segment_counts.index, autopct='%1.1f%%', startangle=90)
    plt.title('用户分层分布')
    
    # 柱状图
    plt.subplot(1, 2, 2)
    sns.barplot(x=segment_counts.index, y=segment_counts.values)
    plt.title('各分层用户数量')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/user_segments.png')
    plt.show()
    
    print("\n用户分层分析：")
    for segment, count in segment_counts.items():
        percentage = segment_percentage[segment]
        print(f"{segment}: {count}人 ({percentage:.1f}%)")

# 分析各分层的RFM特征
def analyze_segment_rfm_features(rfm_df):
    """分析各分层的RFM特征"""
    plt.figure(figsize=(15, 10))
    
    # 各分层的RFM均值
    segment_features = rfm_df.groupby('segment')[['recency', 'frequency', 'monetary']].mean()
    
    # 热力图
    plt.subplot(2, 2, 1)
    sns.heatmap(segment_features, annot=True, cmap='YlGnBu')
    plt.title('各分层RFM特征均值')
    
    # 雷达图
    plt.subplot(2, 2, 2, projection='polar')
    
    # 标准化数据
    normalized_features = (segment_features - segment_features.min()) / (segment_features.max() - segment_features.min())
    
    categories = ['recency', 'frequency', 'monetary']
    N = len(categories)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]
    
    plt.title('各分层RFM特征雷达图', size=15, y=1.1)
    
    for segment in segment_features.index:
        values = normalized_features.loc[segment].tolist()
        values += values[:1]
        plt.plot(angles, values, linewidth=2, linestyle='solid', label=segment)
        plt.fill(angles, values, alpha=0.25)
    
    plt.xticks(angles[:-1], categories)
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    
    # 各分层的RFM评分分布
    plt.subplot(2, 2, 3)
    sns.boxplot(data=rfm_df, x='segment', y='rfm_score')
    plt.title('各分层RFM总分分布')
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/segment_rfm_features.png')
    plt.show()

# 生成用户分层策略
def generate_segment_strategy():
    """生成用户分层策略"""
    strategies = {
        '高价值用户': [
            '提供专属客服',
            '推送高级课程',
            '邀请参与 beta 测试',
            '提供学习认证',
            '专属学习路径定制'
        ],
        '潜力用户': [
            '推送个性化课程推荐',
            '提供学习计划模板',
            '定期学习提醒',
            '参与学习社区活动',
            '提供学习进度分析'
        ],
        '一般用户': [
            '推送热门课程',
            '提供学习技巧指导',
            '鼓励完成课程',
            '参与基础学习活动',
            '提供学习资源包'
        ],
        '低活跃用户': [
            '发送回归激励',
            '提供学习奖励',
            '简化学习路径',
            '一对一学习咨询',
            '限时学习优惠'
        ],
        '沉睡用户': [
            '个性化唤醒邮件',
            '回归奖励活动',
            '课程内容更新通知',
            '学习计划重新制定',
            '专属优惠券'
        ],
        '新用户': [
            '新手引导',
            '入门课程推荐',
            '学习目标设定',
            '社区欢迎活动',
            '首次学习奖励'
        ]
    }
    
    print("\n用户分层运营策略：")
    for segment, strategy_list in strategies.items():
        print(f"\n{segment}：")
        for i, strategy in enumerate(strategy_list, 1):
            print(f"  {i}. {strategy}")

# 主函数
def main():
    print("项目3: 在线教育用户RFM价值分层分析")
    print("=" * 60)
    
    # 生成数据
    print("1. 生成模拟数据...")
    users_df = generate_user_data(num_users=1000)
    learning_df = generate_learning_records(users_df)
    
    print(f"生成用户数：{len(users_df)}")
    print(f"生成学习记录：{len(learning_df)}")
    
    # 计算RFM指标
    print("\n2. 计算RFM指标...")
    rfm_df = calculate_rfm_metrics(users_df, learning_df)
    
    # RFM评分
    print("\n3. RFM分箱评分...")
    rfm_df = rfm_scoring(rfm_df)
    
    # 用户分层
    print("\n4. 用户分层...")
    rfm_df = user_segmentation(rfm_df)
    
    # 分析RFM分布
    print("\n5. 分析RFM分布...")
    analyze_rfm_distribution(rfm_df)
    
    # 分析用户分层
    print("\n6. 分析用户分层...")
    analyze_user_segments(rfm_df)
    
    # 分析各分层的RFM特征
    print("\n7. 分析各分层RFM特征...")
    analyze_segment_rfm_features(rfm_df)
    
    # 生成运营策略
    print("\n8. 生成用户分层运营策略...")
    generate_segment_strategy()
    
    print("\n分析完成！")
    print("生成的图表保存位置：/workspace/python-projects/")

if __name__ == "__main__":
    main()
