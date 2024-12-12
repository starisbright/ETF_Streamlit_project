import yfinance as yf
import streamlit as st

# 美股ETF
etf_symbols = ['ACWI', 'AGG', 'AOA', 'AOR', 'BIL', 'BLV', 'BND', 'BNDW', 'BNDX', 'BSV', 'DFAS', 'DFAX', 'DFCF', 
               'DFE', 'DFSD', 'DFUV', 'DUHP', 'EWT', 'HEFA', 'ICSH', 'IEFA', 'IEMG', 'IJR', 'LQD', 'SGOV', 'SHV', 
               'SHY', 'TIP', 'TLT', 'URTH', 'VB', 'VCIT', 'VEA', 'VGK', 'VNQ', 'VNQI', 'VSS', 'VT', 'VTI', 'VTIP', 'VTV']

# 下載 ETF 歷史數據
@st.cache_data
def download_etf_data(symbol):
    return yf.download(symbol, start="2013-01-01", end="2023-12-31")['Adj Close']

# 計算相對動能（過去 3 個月收益率）
@st.cache_data
def calculate_relative_momentum(etf_symbols):
    etf_3m_returns = {}
    for symbol in etf_symbols:
        etf_data = download_etf_data(symbol)
        three_month_return = (etf_data[-1] / etf_data[-63] - 1) * 100  # 過去 3 個月
        etf_3m_returns[symbol] = three_month_return
    # 依據收益率排序並取前 3 名
    top_3_etfs = sorted(etf_3m_returns, key=etf_3m_returns.get, reverse=True)[:3]
    return top_3_etfs

# 計算絕對動能（是否適合投資）
@st.cache_data
def calculate_absolute_momentum(etf_data, risk_free_rate=0.5):
    twelve_month_return = (etf_data[-1] / etf_data[-252] - 1) * 100  # 過去 12 個月
    return twelve_month_return > risk_free_rate

# 設置左側功能欄
st.sidebar.title("功能選單")
selected_option = st.sidebar.radio(
    "選擇功能：",
    ["市場趨勢", "資產預測", "帳戶餘額", "投資組合分析", "風險屬性測試", "通知"]
)

# 功能：市場趨勢
if selected_option == "市場趨勢":
    st.title("市場趨勢")
    st.write("此處展示市場趨勢相關分析與圖表（未來可擴展）。")

# 功能：資產預測
elif selected_option == "資產預測":
    st.title("資產預測")
    st.write("此處展示資產預測功能，例如未來收益預估。")

# 功能：帳戶餘額
elif selected_option == "帳戶餘額":
    st.title("帳戶餘額")
    st.write("此處顯示用戶帳戶餘額相關資訊。")

# 功能：投資組合分析
elif selected_option == "投資組合分析":
    st.title("投資組合分析")

    # 讓用戶從下拉選單中選擇特定 ETF
    selected_etf = st.selectbox("選擇ETF查看數據", etf_symbols)

    # 獲取所選 ETF 的數據
    etf_data = download_etf_data(selected_etf)
    total_return = (etf_data.iloc[-1] - etf_data.iloc[0]) / etf_data.iloc[0] * 100
    cumulative_return = (etf_data / etf_data.iloc[0]) - 1
    years = (etf_data.index[-1] - etf_data.index[0]).days / 365
    annual_return = ((etf_data.iloc[-1] / etf_data.iloc[0]) ** (1 / years) - 1) * 100

    # 顯示選擇 ETF 的相關數據
    st.write(f"### {selected_etf} ETF 數據分析")
    st.write(f"總回報率: {total_return:.2f}%")
    st.write(f"年化回報率: {annual_return:.2f}%")
    st.line_chart(cumulative_return * 100)

    # 相對動能最佳的 3 檔 ETF
    top_3_etfs = calculate_relative_momentum(etf_symbols)
    st.write("### 符合相對動能最佳的3檔ETF")
    st.write(top_3_etfs)

    # 檢查絕對動能條件
    st.write("### 符合絕對動能條件的ETF")
    investment_candidates = [etf for etf in top_3_etfs if calculate_absolute_momentum(download_etf_data(etf))]
    st.write(investment_candidates)

# 功能：風險屬性測試
elif selected_option == "風險屬性測試":
    st.title("風險屬性測試")
    st.write("此處可以放置測試問卷或相關功能，幫助用戶了解自己的風險屬性。")

# 功能：通知
elif selected_option == "通知":
    st.title("通知")
    st.write("此處顯示用戶的通知（例如重要市場變動或投資提醒）。")

# Footer 或額外說明
st.sidebar.markdown("Powered by Streamlit & YFinance")
import streamlit as st
import pandas as pd

# 模擬年化報酬率（根據不同風險屬性）
RISK_PROFILE_RETURNS = {
    "保守型": 0.03,
    "穩健型": 0.05,
    "成長型": 0.08,
    "積極型": 0.12
}

# Step 1: 評估風險屬性
def risk_assessment():
    st.subheader("Step 1: 評估自身風險屬性")
    st.write("請回答以下問題，了解您的投資風險屬性：")
    q1 = st.radio("1. 您願意承受多大的投資波動？", ("低", "中", "高"))
    q2 = st.radio("2. 投資期間的長度？", ("短期（1-3年）", "中期（3-5年）", "長期（5年以上）"))
    q3 = st.radio("3. 如果市場下跌10%，您的反應是？", ("減少投資", "保持不動", "加碼投資"))

    # 簡單邏輯判斷風險屬性
    if q1 == "低" or q2 == "短期（1-3年）":
        return "保守型"
    elif q1 == "中" or q2 == "中期（3-5年）":
        return "穩健型"
    elif q1 == "高" or (q2 == "長期（5年以上）" and q3 == "加碼投資"):
        return "積極型"
    else:
        return "成長型"

# Step 2: 選擇投資組合
def select_portfolio(risk_profile):
    st.subheader("Step 2: 選擇適合你的投資組合")
    st.write(f"根據您的風險屬性 **{risk_profile}**，推薦以下資產比例：")
    
    if risk_profile == "保守型":
        portfolio = {"債券": 70, "股票": 20, "ETF": 10}
    elif risk_profile == "穩健型":
        portfolio = {"債券": 50, "股票": 30, "ETF": 20}
    elif risk_profile == "成長型":
        portfolio = {"債券": 30, "股票": 50, "ETF": 20}
    elif risk_profile == "積極型":
        portfolio = {"債券": 10, "股票": 60, "ETF": 30}

    st.bar_chart(portfolio)
    return portfolio

# Step 3: 計算預期回報
def calculate_returns(risk_profile):
    st.subheader("Step 3: 計算預期回報")
    investment_type = st.radio("選擇投資方式", ["單筆投入", "定期定額"])
    initial_amount = st.number_input("投入金額（單位：新台幣）", min_value=0, value=100000, step=10000)
    years = st.slider("投資期間（年）", 1, 30, 5)

    # 根據風險屬性對應年化報酬率
    annual_return_rate = RISK_PROFILE_RETURNS[risk_profile]

    if investment_type == "單筆投入":
        future_value = initial_amount * ((1 + annual_return_rate) ** years)
    else:  # 定期定額假設每年投入等額
        annual_investment = initial_amount
        future_value = sum([annual_investment * ((1 + annual_return_rate) ** (years - i)) for i in range(years)])

    st.write(f"### 預期回報：{future_value:,.2f} 新台幣")
    st.success("計算完成！")

# 主程式
def main():
    st.title("智能理財三步驟")
    st.write("根據您的風險屬性，選擇最適合的投資組合，並計算未來的預期回報。")
    
    # 智能理財三步驟
    st.sidebar.title("智能理財三步驟")
    step = st.sidebar.radio("選擇步驟", ["Step 1: 評估風險屬性", "Step 2: 選擇投資組合", "Step 3: 計算預期回報"])
    
    if step == "Step 1: 評估風險屬性":
        risk_profile = risk_assessment()
        st.write(f"您的風險屬性為：**{risk_profile}**")
    elif step == "Step 2: 選擇投資組合":
        risk_profile = st.sidebar.text_input("請輸入風險屬性（例如：保守型）", value="保守型")
        portfolio = select_portfolio(risk_profile)
    elif step == "Step 3: 計算預期回報":
        risk_profile = st.sidebar.text_input("請輸入風險屬性（例如：保守型）", value="保守型")
        calculate_returns(risk_profile)

if __name__ == "__main__":
    main()


