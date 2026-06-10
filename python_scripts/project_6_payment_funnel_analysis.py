#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目6: 在线课程付费转化漏斗分析
内容：浏览 → 试学 → 加购 → 付费 → 完课
Python技能：漏斗图、转化率计算、渠道对比
业务目标：找到转化卡点，提升付费率
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

# 生成模拟用户行为数据
def generate_user_behavior_data(num_users=2000):
    """生成用户行为数据"""
    # 行为阶段
    stages = ['浏览', '试学', '加购', '付费', '完课']
    
    # 渠道
    channels = ['官网', '微信', '知乎', '抖音', '搜索引擎']
    
    # 课程
    courses = ['Python数据分析', 'Excel高级应用', '数据可视化', '统计分析', '商业智能']
    
    # 生成用户行为
    user_behaviors = []
    user_id = 1
    
    for _ in range(num_users):
        # 渠道
        channel = np.random.choice(channels, p=[0.2, 0.3, 0.15, 0.2, 0.15])
        
        # 课程
        course = np.random.choice(courses)
        
        # 基于渠道的转化概率
        channel_conversion = {
            '官网': [1.0, 0.4, 0.3, 0.25, 0.2],
            '微信': [1.0, 0.35, 0.25, 0.2, 0.15],
            '知乎': [1.0, 0.45, 0.35, 0.3, 0.25],
            '抖音': [1.0, 0.3, 0.2, 0.15, 0.1],
            '搜索引擎': [1.0, 0.38, 0.28, 0.22, 0.18]
        }
        
        conversion_rates = channel_conversion[channel]
        
        # 生成行为路径
        current_stage = 0
        
        for i, stage in enumerate(stages):
            if i == 0:
                # 所有用户都从浏览开始
                timestamp = datetime(2023, 6, 1) + timedelta(days=np.random.randint(0, 30), hours=np.random.randint(0, 24))
                user_behaviors.append({
                    'user_id': user_id,
                    'channel': channel,
                    'course': course,
                    'stage': stage,
                    'timestamp': timestamp
                })
                current_stage = i
            else:
                # 基于转化率决定是否进入下一阶段
                if np.random.random() < conversion_rates[i]:
                    # 时间间隔
                    time_gap = timedelta(hours=np.random.randint(1, 72))
                    timestamp = user_behaviors[-1]['timestamp'] + time_gap
                    
                    user_behaviors.append({
                        'user_id': user_id,
                        'channel': channel,
                        'course': course,
                        'stage': stage,
                        'timestamp': timestamp
                    })
                    current_stage = i
                else:
                    # 停止在当前阶段
                    break
        
        user_id += 1
    
    return pd.DataFrame(user_behaviors)

# 计算漏斗数据
def calculate_funnel_data(behavior_df):
    """计算漏斗数据"""
    # 各阶段用户数
    stage_counts = behavior_df.groupby('stage').size()
    
    # 转化率
    total_users = stage_counts.get('浏览', 0)
    conversion_rates = {}
    prev_count = total_users
    
    for stage in ['浏览', '试学', '加购', '付费', '完课']:
        count = stage_counts.get(stage, 0)
        if prev_count > 0:
            rate = (count / prev_count) * 100
        else:
            rate = 0
        conversion_rates[stage] = {
            'count': count,
            'conversion_rate': rate
        }
        prev_count = count
    
    return stage_counts, conversion_rates

# 绘制漏斗图
def plot_funnel(stage_counts):
    """绘制漏斗图"""
    plt.figure(figsize=(12, 8))
    
    # 漏斗阶段
    stages = ['浏览', '试学', '加购', '付费', '完课']
    values = [stage_counts.get(stage, 0) for stage in stages]
    
    # 计算宽度比例
    max_value = max(values)
    widths = [value / max_value for value in values]
    
    # 绘制漏斗
    for i, (stage, value, width) in enumerate(zip(stages, values, widths)):
        # 计算位置
        x = (1 - width) / 2
        y = i / len(stages)
        height = 1 / len(stages) - 0.05
        
        # 绘制矩形
        plt.fill_between([x, x + width], [y, y], [y + height, y + height], 
                        alpha=0.8, color=plt.cm.Blues(0.2 + i * 0.2))
        
        # 添加文字
        plt.text(0.5, y + height/2, f'{stage}\n{value}人', 
                ha='center', va='center', fontsize=12, fontweight='bold')
    
    plt.title('在线课程付费转化漏斗')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/funnel_chart.png')
    plt.show()

# 分析各阶段转化率
def analyze_conversion_rates(conversion_rates):
    """分析各阶段转化率"""
    plt.figure(figsize=(12, 6))
    
    stages = ['浏览→试学', '试学→加购', '加购→付费', '付费→完课']
    rates = []
    
    for i, stage in enumerate(['试学', '加购', '付费', '完课']):
        rates.append(conversion_rates[stage]['conversion_rate'])
    
    sns.barplot(x=stages, y=rates)
    plt.title('各阶段转化率')
    plt.ylabel('转化率 (%)')
    plt.ylim(0, 100)
    
    # 添加数值标签
    for i, rate in enumerate(rates):
        plt.text(i, rate + 2, f'{rate:.1f}%', ha='center')
    
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/conversion_rates.png')
    plt.show()
    
    print("\n各阶段转化率：")
    for stage, data in conversion_rates.items():
        if stage != '浏览':
            print(f"{stage}：{data['conversion_rate']:.1f}%")

# 渠道对比分析
def analyze_channel_funnel(behavior_df):
    """渠道对比分析"""
    plt.figure(figsize=(15, 10))
    
    channels = behavior_df['channel'].unique()
    stages = ['浏览', '试学', '加购', '付费', '完课']
    
    # 计算各渠道的漏斗数据
    channel_funnels = {}
    for channel in channels:
        channel_data = behavior_df[behavior_df['channel'] == channel]
        stage_counts, _ = calculate_funnel_data(channel_data)
        channel_funnels[channel] = [stage_counts.get(stage, 0) for stage in stages]
    
    # 绘制堆叠柱状图
    plt.subplot(2, 1, 1)
    df_funnel = pd.DataFrame(channel_funnels, index=stages)
    df_funnel.plot(kind='bar', stacked=True, ax=plt.gca())
    plt.title('各渠道转化漏斗')
    plt.ylabel('用户数')
    plt.legend(title='渠道')
    
    # 计算各渠道的付费转化率
    plt.subplot(2, 1, 2)
    channel_conversion = {}
    for channel in channels:
        channel_data = behavior_df[behavior_df['channel'] == channel]
        total_users = len(channel_data[channel_data['stage'] == '浏览'])
        paid_users = len(channel_data[channel_data['stage'] == '付费'])
        if total_users > 0:
            conversion_rate = (paid_users / total_users) * 100
        else:
            conversion_rate = 0
        channel_conversion[channel] = conversion_rate
    
    sns.barplot(x=list(channel_conversion.keys()), y=list(channel_conversion.values()))
    plt.title('各渠道付费转化率')
    plt.ylabel('付费转化率 (%)')
    
    # 添加数值标签
    for i, rate in enumerate(channel_conversion.values()):
        plt.text(i, rate + 1, f'{rate:.1f}%', ha='center')
    
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/channel_analysis.png')
    plt.show()
    
    print("\n各渠道付费转化率：")
    for channel, rate in sorted(channel_conversion.items(), key=lambda x: x[1], reverse=True):
        print(f"{channel}：{rate:.1f}%")

# 课程对比分析
def analyze_course_funnel(behavior_df):
    """课程对比分析"""
    plt.figure(figsize=(15, 8))
    
    courses = behavior_df['course'].unique()
    
    # 计算各课程的付费转化率
    course_conversion = {}
    for course in courses:
        course_data = behavior_df[behavior_df['course'] == course]
        total_users = len(course_data[course_data['stage'] == '浏览'])
        paid_users = len(course_data[course_data['stage'] == '付费'])
        if total_users > 0:
            conversion_rate = (paid_users / total_users) * 100
        else:
            conversion_rate = 0
        course_conversion[course] = conversion_rate
    
    # 绘制课程转化率
    sns.barplot(x=list(course_conversion.keys()), y=list(course_conversion.values()))
    plt.title('各课程付费转化率')
    plt.ylabel('付费转化率 (%)')
    plt.xticks(rotation=45)
    
    # 添加数值标签
    for i, rate in enumerate(course_conversion.values()):
        plt.text(i, rate + 1, f'{rate:.1f}%', ha='center')
    
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/course_analysis.png')
    plt.show()
    
    print("\n各课程付费转化率：")
    for course, rate in sorted(course_conversion.items(), key=lambda x: x[1], reverse=True):
        print(f"{course}：{rate:.1f}%")

# 时间趋势分析
def analyze_time_trend(behavior_df):
    """时间趋势分析"""
    # 按天分组
    behavior_df['date'] = behavior_df['timestamp'].dt.date
    
    # 计算每天的各阶段用户数
    daily_data = behavior_df.groupby(['date', 'stage']).size().unstack(fill_value=0)
    
    # 计算每天的付费转化率
    daily_data['付费转化率'] = (daily_data.get('付费', 0) / daily_data.get('浏览', 1)) * 100
    
    plt.figure(figsize=(15, 6))
    
    # 绘制付费转化率趋势
    plt.plot(daily_data.index, daily_data['付费转化率'])
    plt.title('付费转化率时间趋势')
    plt.xlabel('日期')
    plt.ylabel('付费转化率 (%)')
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/time_trend.png')
    plt.show()

# 识别转化卡点
def identify_conversion_issues(conversion_rates):
    """识别转化卡点"""
    print("\n转化卡点分析：")
    
    # 设定阈值
    thresholds = {
        '浏览→试学': 35,
        '试学→加购': 25,
        '加购→付费': 20,
        '付费→完课': 15
    }
    
    stages = ['试学', '加购', '付费', '完课']
    stage_names = ['浏览→试学', '试学→加购', '加购→付费', '付费→完课']
    
    for i, (stage, stage_name) in enumerate(zip(stages, stage_names)):
        rate = conversion_rates[stage]['conversion_rate']
        threshold = thresholds[stage_name]
        
        if rate < threshold:
            print(f"⚠️  {stage_name}转化率偏低：{rate:.1f}%（低于阈值{threshold}%）")
            # 给出改进建议
            if stage_name == '浏览→试学':
                print("  建议：优化课程预览、增加免费试学内容、提升页面加载速度")
            elif stage_name == '试学→加购':
                print("  建议：优化课程详情页、增加课程价值展示、提供试学反馈")
            elif stage_name == '加购→付费':
                print("  建议：优化支付流程、提供优惠活动、增加支付方式")
            elif stage_name == '付费→完课':
                print("  建议：优化学习体验、增加学习激励、提供学习支持")
        else:
            print(f"✅  {stage_name}转化率正常：{rate:.1f}%")

# 主函数
def main():
    print("项目6: 在线课程付费转化漏斗分析")
    print("=" * 60)
    
    # 生成数据
    print("1. 生成模拟数据...")
    behavior_df = generate_user_behavior_data(num_users=2000)
    print(f"生成行为记录：{len(behavior_df)}")
    print(f"涉及用户：{len(behavior_df['user_id'].unique())}")
    print(f"涉及渠道：{len(behavior_df['channel'].unique())}")
    print(f"涉及课程：{len(behavior_df['course'].unique())}")
    
    # 计算漏斗数据
    print("\n2. 计算漏斗数据...")
    stage_counts, conversion_rates = calculate_funnel_data(behavior_df)
    
    # 绘制漏斗图
    print("\n3. 绘制漏斗图...")
    plot_funnel(stage_counts)
    
    # 分析各阶段转化率
    print("\n4. 分析各阶段转化率...")
    analyze_conversion_rates(conversion_rates)
    
    # 渠道对比分析
    print("\n5. 渠道对比分析...")
    analyze_channel_funnel(behavior_df)
    
    # 课程对比分析
    print("\n6. 课程对比分析...")
    analyze_course_funnel(behavior_df)
    
    # 时间趋势分析
    print("\n7. 时间趋势分析...")
    analyze_time_trend(behavior_df)
    
    # 识别转化卡点
    print("\n8. 识别转化卡点...")
    identify_conversion_issues(conversion_rates)
    
    print("\n分析完成！")
    print("生成的图表保存位置：/workspace/python-projects/")

if __name__ == "__main__":
    main()
