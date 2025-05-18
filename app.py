import streamlit as st
import yfinance as yf
import pandas as pd
from fuzzywuzzy import process

# 预设公司数据库（包含更多公司）
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
    "中国平安": "601318.SS",
    "工商银行": "601398.SS",
    "建设银行": "601939.SS",
    "茅台": "600519.SS",
    "五粮液": "000858.SZ",
    "中国移动": "0941.HK"
}

# 页面设置
st.set_page_config(
    page_title="财报数据查询工具",
    page_icon="📊",
    layout="wide"
)

# 主界面
st.title("📊 财报数据查询工具")
st.write("输入公司名称，获取详细财务数据")

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
        
        if st.button("查询财务数据"):
            with st.spinner("正在获取财务数据..."):
                try:
                    # 获取股票代码
                    ticker = COMPANY_DATABASE[selected_company]
                    stock = yf.Ticker(ticker)
                    
                    # 获取财务数据
                    balance_sheet = stock.balance_sheet
                    income_stmt = stock.income_stmt
                    cash_flow = stock.cashflow
                    
                    # 显示公司基本信息
                    st.subheader(f"{selected_company} ({ticker}) 财务数据")
                    
                    # 资产负债表
                    st.divider()
                    st.subheader("资产负债表 (最近4个季度)")
                    if not balance_sheet.empty:
                        st.dataframe(balance_sheet.iloc[:, :4].style.format("{:.2f}"))
                    else:
                        st.warning("无资产负债表数据")
                    
                    # 利润表
                    st.divider()
                    st.subheader("利润表 (最近4个季度)")
                    if not income_stmt.empty:
                        st.dataframe(income_stmt.iloc[:, :4].style.format("{:.2f}"))
                    else:
                        st.warning("无利润表数据")
                    
                    # 现金流量表
                    st.divider()
                    st.subheader("现金流量表 (最近4个季度)")
                    if not cash_flow.empty:
                        st.dataframe(cash_flow.iloc[:, :4].style.format("{:.2f}"))
                    else:
                        st.warning("无现金流量表数据")
                    
                    # 关键财务比率
                    st.divider()
                    st.subheader("关键财务比率")
                    
                    ratios = pd.DataFrame()
                    
                    try:
                        # 盈利能力比率
                        if "Total Revenue" in income_stmt.index and "Net Income" in income_stmt.index:
                            ratios["毛利率(%)"] = [(income_stmt.loc["Gross Profit"] / income_stmt.loc["Total Revenue"] * 100).iloc[0]]
                            ratios["净利率(%)"] = [(income_stmt.loc["Net Income"] / income_stmt.loc["Total Revenue"] * 100).iloc[0]]
                        
                        # 偿债能力比率
                        if "Total Current Assets" in balance_sheet.index and "Total Current Liabilities" in balance_sheet.index:
                            ratios["流动比率"] = [balance_sheet.loc["Total Current Assets"].iloc[0] / balance_sheet.loc["Total Current Liabilities"].iloc[0]]
                        
                        if "Total Debt" in balance_sheet.index and "Total Stockholder Equity" in balance_sheet.index:
                            ratios["负债权益比"] = [balance_sheet.loc["Total Debt"].iloc[0] / balance_sheet.loc["Total Stockholder Equity"].iloc[0]]
                        
                        # 运营效率比率
                        if "Total Revenue" in income_stmt.index and "Total Assets" in balance_sheet.index:
                            ratios["资产周转率"] = [income_stmt.loc["Total Revenue"].iloc[0] / balance_sheet.loc["Total Assets"].iloc[0]]
                        
                        # 投资回报比率
                        if "Net Income" in income_stmt.index and "Total Stockholder Equity" in balance_sheet.index:
                            ratios["ROE(%)"] = [(income_stmt.loc["Net Income"].iloc[0] / balance_sheet.loc["Total Stockholder Equity"].iloc[0] * 100)]
                        
                        if not ratios.empty:
                            st.dataframe(ratios.T.style.format("{:.2f}"), use_container_width=True)
                        else:
                            st.warning("无法计算财务比率")
                    
                    except Exception as e:
                        st.warning(f"计算财务比率时出错: {str(e)}")
                    
                except Exception as e:
                    st.error(f"获取财务数据失败: {str(e)}")
    else:
        st.warning("没有找到匹配的公司")

# 侧边栏说明
st.sidebar.title("使用说明")
st.sidebar.write("1. 输入公司名称（支持模糊搜索）")
st.sidebar.write("2. 从下拉列表选择准确公司")
st.sidebar.write("3. 点击按钮查询财务数据")
st.sidebar.write("4. 查看完整财务报表和关键比率")

# 页脚
st.divider()
st.caption("数据来源: Yahoo Finance | 更新时间: " + pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"))
