import streamlit as st
import yfinance as yf
import pandas as pd
from fuzzywuzzy import process

# 预设公司数据库（实际应用中可替换为更完整的数据库）
COMPANY_DATABASE = {
    "腾讯控股": "0700.HK",
    "阿里巴巴": "9988.HK",
    "贵州茅台": "600519.SS",
    "宁德时代": "300750.SZ",
    "苹果": "AAPL",
    "微软": "MSFT",
    "谷歌": "GOOGL",
    "亚马逊": "AMZN",
    "特斯拉": "TSLA",
    "美团": "3690.HK",
    "京东": "9618.HK",
    "拼多多": "PDD",
    "比亚迪": "1211.HK",
    "小米集团": "1810.HK",
    "中国平安": "601318.SS"
}

# 页面设置
st.set_page_config(
    page_title="财报分析助手",
    page_icon="📊",
    layout="centered"
)

# 主界面
st.title("📊 财报分析助手")
st.write("输入公司名称，获取智能财报分析")

# 模糊搜索功能
def fuzzy_search_companies(query, choices, limit=5):
    results = process.extract(query, choices, limit=limit)
    return [result[0] for result in results if result[1] > 50]

# 公司搜索
company_query = st.text_input("输入公司名称", placeholder="例如：腾讯、苹果...")

if company_query:
    matches = fuzzy_search_companies(company_query, list(COMPANY_DATABASE.keys()))
    if matches:
        selected_company = st.selectbox("选择公司", matches)
        
        if st.button("生成财报分析"):
            with st.spinner("正在分析财报数据..."):
                try:
                    # 获取股票代码
                    ticker = COMPANY_DATABASE[selected_company]
                    stock = yf.Ticker(ticker)
                    
                    # 获取财务数据
                    balance_sheet = stock.balance_sheet
                    income_stmt = stock.income_stmt
                    cash_flow = stock.cashflow
                    
                    # 显示公司基本信息
                    st.subheader(f"{selected_company} ({ticker}) 财报分析")
                    
                    # 关键财务指标
                    st.divider()
                    st.subheader("关键财务指标")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        try:
                            revenue = income_stmt.loc["Total Revenue"].iloc[0]/1e9
                            st.metric("营业收入", f"{revenue:.2f} B")
                        except:
                            pass
                        
                        try:
                            net_income = income_stmt.loc["Net Income"].iloc[0]/1e9
                            st.metric("净利润", f"{net_income:.2f} B")
                        except:
                            pass
                    
                    with col2:
                        try:
                            assets = balance_sheet.loc["Total Assets"].iloc[0]/1e9
                            st.metric("总资产", f"{assets:.2f} B")
                        except:
                            pass
                        
                        try:
                            debt = balance_sheet.loc["Total Debt"].iloc[0]/1e9
                            st.metric("总负债", f"{debt:.2f} B")
                        except:
                            pass
                    
                    with col3:
                        try:
                            operating_cash = cash_flow.loc["Operating Cash Flow"].iloc[0]/1e9
                            st.metric("经营现金流", f"{operating_cash:.2f} B")
                        except:
                            pass
                        
                        try:
                            roe = (income_stmt.loc["Net Income"].iloc[0]/balance_sheet.loc["Total Stockholder Equity"].iloc[0])*100
                            st.metric("ROE", f"{roe:.2f}%")
                        except:
                            pass
                    
                    # 财务健康度分析
                    st.divider()
                    st.subheader("财务健康度分析")
                    
                    try:
                        current_ratio = balance_sheet.loc["Total Current Assets"].iloc[0]/balance_sheet.loc["Total Current Liabilities"].iloc[0]
                        st.write(f"**流动比率**: {current_ratio:.2f} (理想值>1.5)")
                    except:
                        pass
                    
                    try:
                        debt_to_equity = balance_sheet.loc["Total Debt"].iloc[0]/balance_sheet.loc["Total Stockholder Equity"].iloc[0]
                        st.write(f"**负债权益比**: {debt_to_equity:.2f} (理想值<1)")
                    except:
                        pass
                    
                    # 盈利能力分析
                    st.divider()
                    st.subheader("盈利能力分析")
                    
                    try:
                        gross_margin = (income_stmt.loc["Gross Profit"].iloc[0]/income_stmt.loc["Total Revenue"].iloc[0])*100
                        st.write(f"**毛利率**: {gross_margin:.2f}%")
                    except:
                        pass
                    
                    try:
                        net_margin = (income_stmt.loc["Net Income"].iloc[0]/income_stmt.loc["Total Revenue"].iloc[0])*100
                        st.write(f"**净利率**: {net_margin:.2f}%")
                    except:
                        pass
                    
                    # 生成AI分析总结
                    st.divider()
                    st.subheader("AI分析总结")
                    
                    # 这里可以接入真正的AI分析，以下为模拟示例
                    analysis_text = f"""
                    **{selected_company}**最新财报分析：
                    
                    1. **营收规模**: 公司年营收达{revenue:.2f}十亿美元，在行业中处于{'领先' if revenue > 50 else '中等'}水平。
                    
                    2. **盈利能力**: 净利率{net_margin:.2f}%，表明公司{'盈利能力强劲' if net_margin > 15 else '盈利能力一般'}。
                    
                    3. **财务健康**: 流动比率{current_ratio:.2f}，{'财务结构稳健' if current_ratio > 1.5 else '需关注短期偿债能力'}。
                    
                    4. **投资回报**: ROE{roe:.2f}%，为股东创造{'优异' if roe > 20 else '一般'}的回报。
                    """
                    
                    st.write(analysis_text)
                    
                except Exception as e:
                    st.error(f"获取财报数据失败: {str(e)}")
    else:
        st.warning("没有找到匹配的公司")

# 侧边栏说明
st.sidebar.title("使用说明")
st.sidebar.write("1. 输入公司名称（支持模糊搜索）")
st.sidebar.write("2. 从下拉列表选择准确公司")
st.sidebar.write("3. 点击按钮生成财报分析")
st.sidebar.write("4. 查看关键指标和AI分析")
