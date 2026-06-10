#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目4: 课程评价NLP情感分析（好评/差评挖掘）
内容：课程评论爬取或导入 → 分词 → 情感判断 → 词云
Python技能：jieba、WordCloud、snownlp 情感分析
业务目标：自动挖掘课程优缺点
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import jieba
from wordcloud import WordCloud
from snownlp import SnowNLP
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 生成模拟课程评论数据
def generate_course_reviews():
    """生成模拟课程评论数据"""
    # 课程列表
    courses = ['Python数据分析基础', 'Excel高级应用', '数据可视化', '统计分析', '商业智能']
    
    # 正面评价模板
    positive_templates = [
        '课程内容很丰富，老师讲解很详细',
        '学习了很多实用的技能，非常推荐',
        '老师的教学方法很独特，容易理解',
        '课程结构清晰，内容循序渐进',
        '实战项目很有挑战性，收获很大',
        '视频质量很高，字幕清晰',
        '客服响应及时，服务态度好',
        '性价比很高，值得购买',
        '学习后能够立即应用到工作中',
        '课程更新及时，内容前沿'
    ]
    
    # 负面评价模板
    negative_templates = [
        '课程内容太基础，不够深入',
        '老师讲解不够清晰，难以理解',
        '视频质量差，声音模糊',
        '客服响应慢，服务态度差',
        '价格太贵，性价比不高',
        '课程更新不及时，内容过时',
        '实战项目太少，缺乏练习',
        '学习平台不稳定，经常卡顿',
        '课程结构混乱，逻辑不清晰',
        '没有提供足够的学习资料'
    ]
    
    # 中性评价模板
    neutral_templates = [
        '课程内容一般，没有特别突出的地方',
        '老师讲解中规中矩，能理解',
        '视频质量还可以，没有特别差',
        '客服态度还行，响应速度一般',
        '价格适中，符合市场水平',
        '课程内容基本符合预期',
        '学习平台基本稳定，偶尔卡顿',
        '实战项目数量一般，难度适中',
        '课程结构基本合理，有改进空间',
        '学习资料数量一般，质量还可以'
    ]
    
    # 生成评论
    reviews = []
    review_id = 1
    
    for course in courses:
        # 每个课程生成100条评论
        for _ in range(100):
            # 随机选择评价类型
            review_type = np.random.choice(['positive', 'negative', 'neutral'], p=[0.6, 0.2, 0.2])
            
            if review_type == 'positive':
                template = np.random.choice(positive_templates)
                rating = np.random.randint(4, 6)  # 4-5星
            elif review_type == 'negative':
                template = np.random.choice(negative_templates)
                rating = np.random.randint(1, 3)  # 1-2星
            else:
                template = np.random.choice(neutral_templates)
                rating = 3  # 3星
            
            # 添加一些随机变化
            variations = [
                '', '非常', '特别', '真的', '很', '超级', '相当',
                '整体来说', '个人觉得', '我认为', '感觉', '觉得'
            ]
            variation = np.random.choice(variations)
            if variation:
                if np.random.random() > 0.5:
                    template = variation + template
                else:
                    template = template + '，' + variation
            
            # 生成评论时间
            review_date = pd.date_range('2023-01-01', '2023-06-30').sample(1).iloc[0]
            
            reviews.append({
                'review_id': review_id,
                'course_name': course,
                'review_content': template,
                'rating': rating,
                'review_date': review_date
            })
            review_id += 1
    
    return pd.DataFrame(reviews)

# 情感分析
def analyze_sentiment(review_df):
    """使用SnowNLP进行情感分析"""
    # 情感分析
    review_df['sentiment'] = review_df['review_content'].apply(lambda x: SnowNLP(x).sentiments)
    
    # 情感分类
    def classify_sentiment(score):
        if score >= 0.6:
            return '正面'
        elif score <= 0.4:
            return '负面'
        else:
            return '中性'
    
    review_df['sentiment_label'] = review_df['sentiment'].apply(classify_sentiment)
    return review_df

# 分词和关键词提取
def extract_keywords(review_df):
    """分词和关键词提取"""
    # 分词
    review_df['segments'] = review_df['review_content'].apply(lambda x: list(jieba.cut(x)))
    
    # 过滤停用词
    stop_words = set([
        '的', '了', '是', '在', '我', '有', '和', '就', '不', '人', '都', '一', '一个',
        '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好',
        '自己', '这', '非常', '特别', '真的', '很', '超级', '相当', '整体来说', '个人觉得',
        '我认为', '感觉', '觉得'
    ])
    
    review_df['filtered_segments'] = review_df['segments'].apply(
        lambda x: [word for word in x if word not in stop_words and len(word) > 1]
    )
    
    # 关键词提取
    def get_top_keywords(segments, top_n=5):
        word_counts = {}
        for word in segments:
            word_counts[word] = word_counts.get(word, 0) + 1
        sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        return [word for word, _ in sorted_words[:top_n]]
    
    review_df['keywords'] = review_df['filtered_segments'].apply(get_top_keywords)
    return review_df

# 分析情感分布
def analyze_sentiment_distribution(review_df):
    """分析情感分布"""
    plt.figure(figsize=(15, 8))
    
    # 整体情感分布
    plt.subplot(1, 2, 1)
    sentiment_counts = review_df['sentiment_label'].value_counts()
    sentiment_percentage = sentiment_counts / len(review_df) * 100
    plt.pie(sentiment_percentage, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=90)
    plt.title('整体情感分布')
    
    # 各课程情感分布
    plt.subplot(1, 2, 2)
    course_sentiment = review_df.groupby(['course_name', 'sentiment_label']).size().unstack()
    course_sentiment.plot(kind='bar', stacked=True, ax=plt.gca())
    plt.title('各课程情感分布')
    plt.xticks(rotation=45)
    plt.legend(title='情感')
    
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/sentiment_distribution.png')
    plt.show()
    
    print("\n情感分布分析：")
    for sentiment, count in sentiment_counts.items():
        percentage = sentiment_percentage[sentiment]
        print(f"{sentiment}评价：{count}条 ({percentage:.1f}%)")

# 分析评分与情感关系
def analyze_rating_sentiment(review_df):
    """分析评分与情感关系"""
    plt.figure(figsize=(12, 6))
    
    # 评分分布
    plt.subplot(1, 2, 1)
    rating_counts = review_df['rating'].value_counts().sort_index()
    sns.barplot(x=rating_counts.index, y=rating_counts.values)
    plt.title('评分分布')
    plt.xlabel('评分')
    plt.ylabel('数量')
    
    # 评分与情感关系
    plt.subplot(1, 2, 2)
    rating_sentiment = review_df.groupby('rating')['sentiment'].mean()
    sns.lineplot(x=rating_sentiment.index, y=rating_sentiment.values, marker='o')
    plt.title('评分与情感得分关系')
    plt.xlabel('评分')
    plt.ylabel('平均情感得分')
    plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/rating_sentiment.png')
    plt.show()

# 生成词云
def generate_wordclouds(review_df):
    """生成词云"""
    plt.figure(figsize=(15, 10))
    
    # 正面评价词云
    positive_reviews = review_df[review_df['sentiment_label'] == '正面']
    positive_words = ' '.join([' '.join(segments) for segments in positive_reviews['filtered_segments']])
    
    # 负面评价词云
    negative_reviews = review_df[review_df['sentiment_label'] == '负面']
    negative_words = ' '.join([' '.join(segments) for segments in negative_reviews['filtered_segments']])
    
    # 正面词云
    plt.subplot(1, 2, 1)
    wc_positive = WordCloud(
        font_path='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        background_color='white',
        width=800,
        height=600,
        max_words=200
    )
    wc_positive.generate(positive_words)
    plt.imshow(wc_positive, interpolation='bilinear')
    plt.axis('off')
    plt.title('正面评价词云')
    
    # 负面词云
    plt.subplot(1, 2, 2)
    wc_negative = WordCloud(
        font_path='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        background_color='white',
        width=800,
        height=600,
        max_words=200
    )
    wc_negative.generate(negative_words)
    plt.imshow(wc_negative, interpolation='bilinear')
    plt.axis('off')
    plt.title('负面评价词云')
    
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/sentiment_wordcloud.png')
    plt.show()

# 分析各课程优缺点
def analyze_course_pros_cons(review_df):
    """分析各课程优缺点"""
    print("\n各课程优缺点分析：")
    
    for course in review_df['course_name'].unique():
        course_reviews = review_df[review_df['course_name'] == course]
        
        # 正面评价关键词
        positive_reviews = course_reviews[course_reviews['sentiment_label'] == '正面']
        positive_words = []
        for segments in positive_reviews['filtered_segments']:
            positive_words.extend(segments)
        
        # 统计正面关键词
        positive_word_counts = {}
        for word in positive_words:
            positive_word_counts[word] = positive_word_counts.get(word, 0) + 1
        top_positive = sorted(positive_word_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # 负面评价关键词
        negative_reviews = course_reviews[course_reviews['sentiment_label'] == '负面']
        negative_words = []
        for segments in negative_reviews['filtered_segments']:
            negative_words.extend(segments)
        
        # 统计负面关键词
        negative_word_counts = {}
        for word in negative_words:
            negative_word_counts[word] = negative_word_counts.get(word, 0) + 1
        top_negative = sorted(negative_word_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        print(f"\n{course}：")
        print("优点：")
        for word, count in top_positive:
            print(f"  {word}: {count}次")
        
        print("缺点：")
        for word, count in top_negative:
            print(f"  {word}: {count}次")

# 分析评价时间趋势
def analyze_review_trend(review_df):
    """分析评价时间趋势"""
    # 按月分组
    review_df['month'] = review_df['review_date'].dt.month
    
    plt.figure(figsize=(12, 6))
    
    # 每月评价数量
    monthly_reviews = review_df.groupby('month').size()
    
    # 每月平均情感得分
    monthly_sentiment = review_df.groupby('month')['sentiment'].mean()
    
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # 评价数量
    ax1.set_xlabel('月份')
    ax1.set_ylabel('评价数量', color='tab:blue')
    ax1.plot(monthly_reviews.index, monthly_reviews.values, color='tab:blue', marker='o')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    
    # 情感得分
    ax2 = ax1.twinx()
    ax2.set_ylabel('平均情感得分', color='tab:red')
    ax2.plot(monthly_sentiment.index, monthly_sentiment.values, color='tab:red', marker='s')
    ax2.tick_params(axis='y', labelcolor='tab:red')
    
    plt.title('评价时间趋势')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('/workspace/python-projects/review_trend.png')
    plt.show()

# 主函数
def main():
    print("项目4: 课程评价NLP情感分析（好评/差评挖掘）")
    print("=" * 60)
    
    # 生成数据
    print("1. 生成模拟评论数据...")
    reviews_df = generate_course_reviews()
    print(f"生成评论数：{len(reviews_df)}")
    print(f"涉及课程：{len(reviews_df['course_name'].unique())}")
    
    # 情感分析
    print("\n2. 进行情感分析...")
    reviews_df = analyze_sentiment(reviews_df)
    
    # 分词和关键词提取
    print("\n3. 分词和关键词提取...")
    reviews_df = extract_keywords(reviews_df)
    
    # 分析情感分布
    print("\n4. 分析情感分布...")
    analyze_sentiment_distribution(reviews_df)
    
    # 分析评分与情感关系
    print("\n5. 分析评分与情感关系...")
    analyze_rating_sentiment(reviews_df)
    
    # 生成词云
    print("\n6. 生成词云...")
    generate_wordclouds(reviews_df)
    
    # 分析各课程优缺点
    print("\n7. 分析各课程优缺点...")
    analyze_course_pros_cons(reviews_df)
    
    # 分析评价时间趋势
    print("\n8. 分析评价时间趋势...")
    analyze_review_trend(reviews_df)
    
    print("\n分析完成！")
    print("生成的图表保存位置：/workspace/python-projects/")

if __name__ == "__main__":
    main()
