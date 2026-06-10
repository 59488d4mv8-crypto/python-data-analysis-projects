#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目1: 教育平台用户注册与活跃行为分析
内容：注册渠道、注册时段、日活/周活/月活、留存率
Python技能：Pandas、Matplotlib、Seaborn、时间序列
业务目标：判断哪些渠道获客质量最高
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

# 生成模拟数据
def generate_user_data():
    """生成用户注册和活跃数据"""
    # 注册渠道
    channels = ['官网', '微信', '知乎', '抖音', '朋友推荐', '搜索引擎']
    
    # 生成2023年1月到2023年6月的数据
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 6, 30)
    date_range = pd.date_range(start=start_date, end=end_date)
    
    # 生成用户数据
    users = []
    user_id = 1
    
    for date in date_range:
        # 每天注册用户数
        daily_reg = np.random.randint(50, 200)
        
        for _ in range(daily_reg):
            # 注册时间（随机小时）
            register_hour = np.random.randint(0, 24)
            register_time = date.replace(hour=register_hour, minute=np.random.randint(0, 60))
            
            # 注册渠道
            channel = np.random.choice(channels, p=[0.2, 0.3, 0.15, 0.2, 0.1, 0.05])
            
            # 活跃天数（基于渠道质量）
            channel_activity_map = {
                '官网': 20,
                '微信': 15,
                '知乎': 25,
                '抖音': 10,
                '朋友推荐': 30,
                '搜索引擎': 12
            }
            base_activity = channel_activity_map[channel]
            activity_days = int(np.random.normal(base_activity, 5))
            activity_days = max(1, min(60, activity_days))
            
            users.append({
                'user_id': user_id,
                'register_time': register_time,
                'register_channel': channel,
                'activity_days': activity_days
            })
            user_id += 1
    
    return pd.DataFrame(users)

# 生成活跃数据
def generate_active_data(users_df):
    """生成用户活跃数据"""
    active_records = []
    
    for _, user in users_df.iterrows():
        register_date = user['register_time'].date()
        activity_days = user['activity_days']
        
        # 生成活跃日期
        for i in range(activity_days):
            active_date = register_date + timedelta(days=i)
            # 有一定概率当天不活跃
            if np.random.random() > 0.3:
                active_records.append({
                    'user_id': user['user_id'],
                    'active_date': pd.to_datetime(active_date)
                })
    
    return pd.DataFrame(active_records)

# 分析注册渠道分布
def analyze_registration_channels(users_df):
    """分析注册渠道分布"""
    plt.figure(figsize=(12, 6))
    channel_counts = users_df['register_channel'].value_counts()
    channel_percentage = channel_counts / len(users_df) * 100
    
    # 饼图
    plt.subplot(1, 2, 1)
    plt.pie(channel_percentage, labels=channel_counts.index, autopct='%1.1f%%', startangle=90)
    plt.title('注册渠道分布')
    
    # 柱状图
    plt.subplot(1, 2, 2)
    sns.barplot(x=channel_counts.index, y=channel_counts.values)
    plt.title('各渠道注册用户数')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/registration_channels.png')
    plt.show()
    
    print("注册渠道分析：")
    for channel, count in channel_counts.items():
        print(f"{channel}: {count}人 ({channel_percentage[channel]:.1f}%)")

# 分析注册时段分布
def analyze_registration_hours(users_df):
    """分析注册时段分布"""
    users_df['register_hour'] = users_df['register_time'].dt.hour
    
    plt.figure(figsize=(12, 6))
    hour_counts = users_df['register_hour'].value_counts().sort_index()
    
    sns.barplot(x=hour_counts.index, y=hour_counts.values)
    plt.title('注册时段分布')
    plt.xlabel('小时')
    plt.ylabel('注册用户数')
    plt.xticks(range(0, 24))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/registration_hours.png')
    plt.show()
    
    print("\n注册时段分析：")
    peak_hour = hour_counts.idxmax()
    print(f"注册高峰时段：{peak_hour}:00-{(peak_hour+1)%24}:00，注册人数：{hour_counts.max()}")

# 计算日活、周活、月活
def calculate_activity_metrics(active_df):
    """计算日活、周活、月活"""
    # 日活
    daily_active = active_df.groupby('active_date')['user_id'].nunique()
    
    # 周活
    weekly_active = active_df.copy()
    weekly_active['week'] = weekly_active['active_date'].dt.isocalendar().week
    weekly_active = weekly_active.groupby('week')['user_id'].nunique()
    
    # 月活
    monthly_active = active_df.copy()
    monthly_active['month'] = monthly_active['active_date'].dt.month
    monthly_active = monthly_active.groupby('month')['user_id'].nunique()
    
    # 可视化
    plt.figure(figsize=(15, 5))
    
    # 日活
    plt.subplot(1, 3, 1)
    daily_active.plot(kind='line')
    plt.title('日活跃用户数')
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # 周活
    plt.subplot(1, 3, 2)
    weekly_active.plot(kind='bar')
    plt.title('周活跃用户数')
    plt.xticks(rotation=0)
    
    # 月活
    plt.subplot(1, 3, 3)
    monthly_active.plot(kind='bar')
    plt.title('月活跃用户数')
    plt.xticks(rotation=0)
    
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/activity_metrics.png')
    plt.show()
    
    print("\n活跃用户分析：")
    print(f"平均日活：{daily_active.mean():.1f}")
    print(f"平均周活：{weekly_active.mean():.1f}")
    print(f"平均月活：{monthly_active.mean():.1f}")

# 计算留存率
def calculate_retention_rate(users_df, active_df):
    """计算留存率"""
    # 按渠道计算留存率
    retention_data = []
    
    # 确保active_date是日期类型
    active_df['active_date'] = active_df['active_date'].dt.date
    
    for channel in users_df['register_channel'].unique():
        channel_users = users_df[users_df['register_channel'] == channel]
        total_users = len(channel_users)
        
        # 计算7日留存
        day7_retention = 0
        for _, user in channel_users.iterrows():
            register_date = user['register_time'].date()
            day7_date = register_date + timedelta(days=7)
            # 检查用户是否在7天后活跃
            user_active_dates = active_df[active_df['user_id'] == user['user_id']]['active_date'].tolist()
            if day7_date in user_active_dates:
                day7_retention += 1
        
        # 计算30日留存
        day30_retention = 0
        for _, user in channel_users.iterrows():
            register_date = user['register_time'].date()
            day30_date = register_date + timedelta(days=30)
            # 检查用户是否在30天后活跃
            user_active_dates = active_df[active_df['user_id'] == user['user_id']]['active_date'].tolist()
            if day30_date in user_active_dates:
                day30_retention += 1
        
        retention_data.append({
            'channel': channel,
            'total_users': total_users,
            '7_day_retention': day7_retention / total_users * 100 if total_users > 0 else 0,
            '30_day_retention': day30_retention / total_users * 100 if total_users > 0 else 0
        })
    
    retention_df = pd.DataFrame(retention_data)
    
    # 可视化
    plt.figure(figsize=(12, 6))
    retention_df.plot(x='channel', y=['7_day_retention', '30_day_retention'], kind='bar')
    plt.title('各渠道留存率对比')
    plt.ylabel('留存率 (%)')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/retention_rates.png')
    plt.show()
    
    print("\n留存率分析：")
    print(retention_df.sort_values('30_day_retention', ascending=False))
    
    # 找出最佳渠道
    best_channel = retention_df.loc[retention_df['30_day_retention'].idxmax()]
    print(f"\n最佳获客渠道：{best_channel['channel']}")
    print(f"30日留存率：{best_channel['30_day_retention']:.1f}%")
    print(f"总注册用户：{best_channel['total_users']}人")

# 主函数
def main():
    print("项目1: 教育平台用户注册与活跃行为分析")
    print("=" * 60)
    
    # 生成数据
    print("1. 生成模拟数据...")
    users_df = generate_user_data()
    active_df = generate_active_data(users_df)
    
    print(f"生成用户数：{len(users_df)}")
    print(f"生成活跃记录：{len(active_df)}")
    
    # 分析注册渠道
    print("\n2. 分析注册渠道分布...")
    analyze_registration_channels(users_df)
    
    # 分析注册时段
    print("\n3. 分析注册时段分布...")
    analyze_registration_hours(users_df)
    
    # 计算活跃指标
    print("\n4. 计算活跃用户指标...")
    calculate_activity_metrics(active_df)
    
    # 计算留存率
    print("\n5. 计算留存率...")
    calculate_retention_rate(users_df, active_df)
    
    print("\n分析完成！")
    print("生成的图表保存位置：/workspace/python-projects/")

if __name__ == "__main__":
    main()
