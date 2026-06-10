#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目8: 每日访问量与课程销量时间序列预测
内容：按小时/天/周流量趋势、节假日波动、短期预测
Python技能：时间序列、滑动窗口、简单预测模型
业务目标：预测流量高峰，用于服务器/运营排期
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

# 生成模拟时间序列数据
def generate_time_series_data(start_date='2023-01-01', end_date='2023-12-31'):
    """生成时间序列数据"""
    # 生成日期范围
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # 基础趋势
    base_visits = 1000
    base_sales = 50
    
    # 季节性因素
    # 周季节性（周末流量高）
    weekday_effect = np.array([0.8, 0.9, 1.0, 1.0, 1.1, 1.3, 1.2])  # 周一到周日
    
    # 月季节性（月初和月中流量高）
    monthly_effect = np.array([1.2, 1.1, 1.0, 0.9, 0.9, 1.0, 1.1, 1.2, 1.1, 1.0, 0.9, 0.8])  # 1-12月
    
    # 节假日效应
    holidays = [
        '2023-01-01',  # 元旦
        '2023-02-14',  # 春节
        '2023-04-05',  # 清明节
        '2023-05-01',  # 劳动节
        '2023-06-22',  # 端午节
        '2023-09-29',  # 中秋节
        '2023-10-01',  # 国庆节
        '2023-12-25'   # 圣诞节
    ]
    holiday_dates = pd.to_datetime(holidays)
    
    # 生成数据
    data = []
    for date in date_range:
        # 基础值
        visits = base_visits
        sales = base_sales
        
        # 时间趋势（增长）
        day_of_year = date.dayofyear
        trend_factor = 1 + (day_of_year / 365) * 0.3  # 30%年增长
        
        # 周季节性
        weekday = date.weekday()
        weekday_factor = weekday_effect[weekday]
        
        # 月季节性
        month = date.month - 1
        month_factor = monthly_effect[month]
        
        # 节假日效应
        holiday_factor = 1.5 if date.date() in holiday_dates.date else 1.0
        
        # 随机波动
        random_factor = np.random.normal(1, 0.1)
        
        # 计算最终值
        final_visits = int(visits * trend_factor * weekday_factor * month_factor * holiday_factor * random_factor)
        final_sales = int(sales * trend_factor * weekday_factor * month_factor * holiday_factor * random_factor)
        
        # 确保值为正
        final_visits = max(500, final_visits)
        final_sales = max(20, final_sales)
        
        data.append({
            'date': date,
            'visits': final_visits,
            'sales': final_sales,
            'weekday': date.weekday(),
            'month': date.month,
            'is_holiday': 1 if date.date() in holiday_dates.date else 0
        })
    
    return pd.DataFrame(data)

# 分析时间序列趋势
def analyze_time_series_trends(df):
    """分析时间序列趋势"""
    plt.figure(figsize=(15, 10))
    
    # 每日访问量和销量趋势
    plt.subplot(2, 1, 1)
    plt.plot(df['date'], df['visits'], label='访问量')
    plt.title('每日访问量趋势')
    plt.ylabel('访问量')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    plt.subplot(2, 1, 2)
    plt.plot(df['date'], df['sales'], label='销量', color='red')
    plt.title('每日课程销量趋势')
    plt.ylabel('销量')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/time_series_trends.png')
    plt.show()

# 分析周季节性
def analyze_weekly_seasonality(df):
    """分析周季节性"""
    plt.figure(figsize=(15, 6))
    
    # 按周几分组
    weekly_data = df.groupby('weekday').agg({'visits': 'mean', 'sales': 'mean'}).reset_index()
    weekdays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    weekly_data['weekday_name'] = weekly_data['weekday'].map(dict(enumerate(weekdays)))
    
    # 周访问量
    plt.subplot(1, 2, 1)
    sns.barplot(x='weekday_name', y='visits', data=weekly_data)
    plt.title('周访问量模式')
    plt.ylabel('平均访问量')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # 周销量
    plt.subplot(1, 2, 2)
    sns.barplot(x='weekday_name', y='sales', data=weekly_data)
    plt.title('周销量模式')
    plt.ylabel('平均销量')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/weekly_seasonality.png')
    plt.show()

# 分析月季节性
def analyze_monthly_seasonality(df):
    """分析月季节性"""
    plt.figure(figsize=(15, 6))
    
    # 按月分组
    monthly_data = df.groupby('month').agg({'visits': 'mean', 'sales': 'mean'}).reset_index()
    months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
    monthly_data['month_name'] = monthly_data['month'].map(dict(enumerate(months, 1)))
    
    # 月访问量
    plt.subplot(1, 2, 1)
    sns.barplot(x='month_name', y='visits', data=monthly_data)
    plt.title('月访问量模式')
    plt.ylabel('平均访问量')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # 月销量
    plt.subplot(1, 2, 2)
    sns.barplot(x='month_name', y='sales', data=monthly_data)
    plt.title('月销量模式')
    plt.ylabel('平均销量')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/monthly_seasonality.png')
    plt.show()

# 分析节假日效应
def analyze_holiday_effect(df):
    """分析节假日效应"""
    plt.figure(figsize=(12, 6))
    
    # 节假日 vs 非节假日
    holiday_data = df.groupby('is_holiday').agg({'visits': 'mean', 'sales': 'mean'}).reset_index()
    holiday_data['type'] = holiday_data['is_holiday'].map({0: '非节假日', 1: '节假日'})
    
    # 访问量对比
    plt.subplot(1, 2, 1)
    sns.barplot(x='type', y='visits', data=holiday_data)
    plt.title('节假日 vs 非节假日访问量')
    plt.ylabel('平均访问量')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # 销量对比
    plt.subplot(1, 2, 2)
    sns.barplot(x='type', y='sales', data=holiday_data)
    plt.title('节假日 vs 非节假日销量')
    plt.ylabel('平均销量')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/holiday_effect.png')
    plt.show()
    
    # 计算增长率
    non_holiday_visits = holiday_data[holiday_data['is_holiday'] == 0]['visits'].iloc[0]
    holiday_visits = holiday_data[holiday_data['is_holiday'] == 1]['visits'].iloc[0]
    visits_growth = ((holiday_visits - non_holiday_visits) / non_holiday_visits) * 100
    
    non_holiday_sales = holiday_data[holiday_data['is_holiday'] == 0]['sales'].iloc[0]
    holiday_sales = holiday_data[holiday_data['is_holiday'] == 1]['sales'].iloc[0]
    sales_growth = ((holiday_sales - non_holiday_sales) / non_holiday_sales) * 100
    
    print(f"\n节假日效应：")
    print(f"访问量增长率：{visits_growth:.1f}%")
    print(f"销量增长率：{sales_growth:.1f}%")

# 移动平均预测
def moving_average_prediction(df, window=7, forecast_days=7):
    """移动平均预测"""
    # 计算移动平均
    df['visits_ma'] = df['visits'].rolling(window=window).mean()
    df['sales_ma'] = df['sales'].rolling(window=window).mean()
    
    # 预测未来7天
    last_visits = df['visits'].tail(window).mean()
    last_sales = df['sales'].tail(window).mean()
    
    # 生成预测日期
    last_date = df['date'].iloc[-1]
    forecast_dates = [last_date + timedelta(days=i+1) for i in range(forecast_days)]
    
    # 生成预测数据
    forecast_data = []
    for date in forecast_dates:
        # 考虑周季节性
        weekday = date.weekday()
        weekday_factor = df[df['weekday'] == weekday]['visits'].mean() / df['visits'].mean()
        
        forecast_visits = int(last_visits * weekday_factor)
        forecast_sales = int(last_sales * weekday_factor)
        
        forecast_data.append({
            'date': date,
            'visits': forecast_visits,
            'sales': forecast_sales,
            'is_forecast': True
        })
    
    return pd.DataFrame(forecast_data), df

# 简单线性回归预测
def linear_regression_prediction(df, forecast_days=7):
    """简单线性回归预测"""
    # 准备数据
    df['day_index'] = range(len(df))
    X = df['day_index'].values.reshape(-1, 1)
    y_visits = df['visits'].values
    y_sales = df['sales'].values
    
    # 简单线性回归
    from sklearn.linear_model import LinearRegression
    model_visits = LinearRegression()
    model_visits.fit(X, y_visits)
    
    model_sales = LinearRegression()
    model_sales.fit(X, y_sales)
    
    # 预测未来
    last_index = df['day_index'].iloc[-1]
    future_indices = np.array([[last_index + i + 1] for i in range(forecast_days)])
    
    forecast_visits = model_visits.predict(future_indices)
    forecast_sales = model_sales.predict(future_indices)
    
    # 生成预测日期
    last_date = df['date'].iloc[-1]
    forecast_dates = [last_date + timedelta(days=i+1) for i in range(forecast_days)]
    
    # 生成预测数据
    forecast_data = []
    for date, visits, sales in zip(forecast_dates, forecast_visits, forecast_sales):
        forecast_data.append({
            'date': date,
            'visits': int(visits),
            'sales': int(sales),
            'is_forecast': True
        })
    
    return pd.DataFrame(forecast_data)

# 预测结果可视化
def visualize_predictions(df, ma_forecast, lr_forecast):
    """预测结果可视化"""
    plt.figure(figsize=(15, 10))
    
    # 访问量预测
    plt.subplot(2, 1, 1)
    plt.plot(df['date'], df['visits'], label='实际访问量')
    plt.plot(df['date'], df['visits_ma'], label='移动平均', linestyle='--')
    plt.plot(ma_forecast['date'], ma_forecast['visits'], label='移动平均预测', linestyle='--', color='green')
    plt.plot(lr_forecast['date'], lr_forecast['visits'], label='线性回归预测', linestyle='--', color='orange')
    plt.title('访问量预测')
    plt.ylabel('访问量')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    # 销量预测
    plt.subplot(2, 1, 2)
    plt.plot(df['date'], df['sales'], label='实际销量', color='red')
    plt.plot(df['date'], df['sales_ma'], label='移动平均', linestyle='--', color='red')
    plt.plot(ma_forecast['date'], ma_forecast['sales'], label='移动平均预测', linestyle='--', color='green')
    plt.plot(lr_forecast['date'], lr_forecast['sales'], label='线性回归预测', linestyle='--', color='orange')
    plt.title('销量预测')
    plt.ylabel('销量')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/forecast_results.png')
    plt.show()

# 分析预测误差
def analyze_forecast_error(df, forecast_df, actual_col, forecast_col):
    """分析预测误差"""
    # 计算误差
    errors = df[actual_col].tail(len(forecast_df)) - forecast_df[forecast_col]
    mae = np.mean(np.abs(errors))
    rmse = np.sqrt(np.mean(errors**2))
    mape = np.mean(np.abs(errors / df[actual_col].tail(len(forecast_df)))) * 100
    
    return mae, rmse, mape

# 主函数
def main():
    print("项目8: 每日访问量与课程销量时间序列预测")
    print("=" * 60)
    
    # 生成数据
    print("1. 生成模拟数据...")
    df = generate_time_series_data()
    print(f"生成数据时间范围：{df['date'].min().date()} 到 {df['date'].max().date()}")
    print(f"总数据量：{len(df)} 天")
    
    # 分析时间序列趋势
    print("\n2. 分析时间序列趋势...")
    analyze_time_series_trends(df)
    
    # 分析周季节性
    print("\n3. 分析周季节性...")
    analyze_weekly_seasonality(df)
    
    # 分析月季节性
    print("\n4. 分析月季节性...")
    analyze_monthly_seasonality(df)
    
    # 分析节假日效应
    print("\n5. 分析节假日效应...")
    analyze_holiday_effect(df)
    
    # 移动平均预测
    print("\n6. 移动平均预测...")
    ma_forecast, df_with_ma = moving_average_prediction(df)
    print(f"移动平均预测未来7天访问量：{ma_forecast['visits'].tolist()}")
    print(f"移动平均预测未来7天销量：{ma_forecast['sales'].tolist()}")
    
    # 线性回归预测
    print("\n7. 线性回归预测...")
    lr_forecast = linear_regression_prediction(df)
    print(f"线性回归预测未来7天访问量：{lr_forecast['visits'].tolist()}")
    print(f"线性回归预测未来7天销量：{lr_forecast['sales'].tolist()}")
    
    # 可视化预测结果
    print("\n8. 可视化预测结果...")
    visualize_predictions(df_with_ma, ma_forecast, lr_forecast)
    
    # 分析预测误差（使用历史数据进行回测）
    print("\n9. 分析预测误差...")
    # 回测：使用前30天预测后7天
    test_df = df.tail(37)
    test_ma_forecast, _ = moving_average_prediction(test_df.head(30))
    test_lr_forecast = linear_regression_prediction(test_df.head(30))
    
    # 计算误差
    ma_mae_visits, ma_rmse_visits, ma_mape_visits = analyze_forecast_error(test_df.tail(7), test_ma_forecast, 'visits', 'visits')
    lr_mae_visits, lr_rmse_visits, lr_mape_visits = analyze_forecast_error(test_df.tail(7), test_lr_forecast, 'visits', 'visits')
    
    ma_mae_sales, ma_rmse_sales, ma_mape_sales = analyze_forecast_error(test_df.tail(7), test_ma_forecast, 'sales', 'sales')
    lr_mae_sales, lr_rmse_sales, lr_mape_sales = analyze_forecast_error(test_df.tail(7), test_lr_forecast, 'sales', 'sales')
    
    print("\n访问量预测误差：")
    print(f"移动平均 - MAE: {ma_mae_visits:.2f}, RMSE: {ma_rmse_visits:.2f}, MAPE: {ma_mape_visits:.2f}%")
    print(f"线性回归 - MAE: {lr_mae_visits:.2f}, RMSE: {lr_rmse_visits:.2f}, MAPE: {lr_mape_visits:.2f}%")
    
    print("\n销量预测误差：")
    print(f"移动平均 - MAE: {ma_mae_sales:.2f}, RMSE: {ma_rmse_sales:.2f}, MAPE: {ma_mape_sales:.2f}%")
    print(f"线性回归 - MAE: {lr_mae_sales:.2f}, RMSE: {lr_rmse_sales:.2f}, MAPE: {lr_mape_sales:.2f}%")
    
    print("\n分析完成！")
    print("生成的图表保存位置：/workspace/python-projects/")

if __name__ == "__main__":
    main()
