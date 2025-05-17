import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup

# 模拟财报数据获取（实际可接入金融API）
def get_financial_data(stock_code):
    # 这里使用模拟数据，实际项目可替换为真实API调用
    data = {
        "年份": [2020, 2021, 2022, 2023],
        "营业收入(亿元)": [120, 150, 180, 200],
        "净利润(亿元)": [10, 15, 18, 22],
        "毛利率(%)": [30, 32, 35, 38],
        "资产负债率(%)": [45, 48, 50, 47]
    }
    return pd.DataFrame(data)

st.title("📊 财报速读神器")
stock_code = st.text_input("输入股票代码（如：AAPL）", "AAPL")

if st.button("生成分析报告"):
    with st.spinner("正在获取数据..."):
        df = get_financial_data(stock_code)
        
        st.subheader(f"{stock_code} 财务分析报告")
        
        # 显示数据表格
        st.dataframe(df)
        
        # 创建图表
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # 营收趋势
        axes[0, 0].plot(df['年份'], df['营业收入(亿元)'], marker='o')
        axes[0, 0].set_title('营业收入趋势')
        axes[0, 0].grid(True)
        
        # 净利润趋势
        axes[0, 1].plot(df['年份'], df['净利润(亿元)'], marker='o', color='orange')
        axes[0, 1].set_title('净利润趋势')
        axes[0, 1].grid(True)
        
        # 毛利率
        axes[1, 0].bar(df['年份'], df['毛利率(%)'], color='green')
        axes[1, 0].set_title('毛利率变化')
        axes[1, 0].grid(True)
        
        # 资产负债率
        axes[1, 1].bar(df['年份'], df['资产负债率(%)'], color='red')
        axes[1, 1].set_title('资产负债率')
        axes[1, 1].grid(True)
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # 关键指标分析
        latest_year = df['年份'].max()
        prev_year = latest_year - 1
        
        revenue_growth = ((df[df['年份'] == latest_year]['营业收入(亿元)'].values[0] / 
                          df[df['年份'] == prev_year]['营业收入(亿元)'].values[0]) - 1) * 100
        
        profit_growth = ((df[df['年份'] == latest_year]['净利润(亿元)'].values[0] / 
                         df[df['年份'] == prev_year]['净利润(亿元)'].values[0]) - 1) * 100
        
        st.subheader("📈 关键指标解读")
        st.markdown(f"- **{latest_year}年营业收入**：{df[df['年份'] == latest_year]['营业收入(亿元)'].values[0]}亿元，同比增长{revenue_growth:.2f}%")
        st.markdown(f"- **{latest_year}年净利润**：{df[df['年份'] == latest_year]['净利润(亿元)'].values[0]}亿元，同比增长{profit_growth:.2f}%")
        st.markdown(f"- **毛利率**：{df[df['年份'] == latest_year]['毛利率(%)'].values[0]}%")
        st.markdown(f"- **资产负债率**：{df[df['年份'] == latest_year]['资产负债率(%)'].values[0]}%")
        
        # 简单结论
        if revenue_growth > 10 and profit_growth > 15:
            st.success("📊 财务状况良好，营收和利润均呈现强劲增长趋势")
        elif revenue_growth > 0 and profit_growth > 0:
            st.info("📊 财务状况稳定，营收和利润持续增长")
        else:
            st.warning("📊 财务状况有待改善，建议进一步分析")
