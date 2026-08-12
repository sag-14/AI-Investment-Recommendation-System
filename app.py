import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(
    page_title="AI Investment Recommendation System",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)
stock_symbol = st.sidebar.selectbox(
    "Select Stock",
    ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ITC.NS"]
)
# ---------------- Sidebar ----------------

st.sidebar.title("📈 AI Investment Recommendation System")

page = st.sidebar.selectbox(
    "Navigation",
    [
        "Dashboard",
        "Investment Analysis",
        "AI Recommendation",
        "Portfolio",
        "Market Analysis",
        "Reports",
        "Risk Analysis",
        "Stock Comparison",
        "Portfolio Optimization",
        "About Project"
    ]
)

# ==========================================
# Stock Selection
# ==========================================

st.sidebar.header("📈 Stock Selection")

stock_symbol = st.sidebar.selectbox(
    "Select Stock",
    ["RELIANCE.NS","TCS.NS","INFY.NS","HDFCBANK.NS","ITC.NS"]
)

st.sidebar.success(f"Selected: {stock_symbol}")

# ==========================================
# Download Live Stock Data
# ==========================================

try:

    data = yf.download(
        stock_symbol,
        period="1y",
        interval="1d"
    )

    st.write("Current Stock:", stock_symbol)

    data = data.reset_index()
    if hasattr(data.columns, "levels"):
       data.columns = [
         col[0] if isinstance(col, tuple) else col
         for col in data.columns
    ]

    # Moving Averages
    data["MA20"] = data["Close"].rolling(20).mean()
    data["MA50"] = data["Close"].rolling(50).mean()

    # Daily Return
    data["Daily Return (%)"] = (
        data["Close"].pct_change() * 100
    )

    # Cumulative Return
    data["Cumulative Return (%)"] = (
        (data["Close"] / data["Close"].iloc[0] - 1)
        * 100
    )

except Exception as e:

    st.error(f"Unable to download stock data.\n\n{e}")

    st.stop()

# ---------------- Dashboard ----------------

if page == "Dashboard":

    st.title("📊 AI Investment Dashboard")

    # ===============================
    # Load Data
    # ===============================

    # Download latest stock data
    prediction = pd.read_csv(
    "data/latest_prediction.csv"
    )

    latest = data.iloc[-1]

    current_price = float(latest["Close"])

    daily_return = float(latest["Daily Return (%)"])

    recommendation = prediction["Prediction"].iloc[0]

    confidence = prediction["Confidence (%)"].iloc[0] 

    # ===============================
    # KPI Cards
    # ===============================

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "💰 Current Price",
        f"₹ {current_price:.2f}"
    )

    c2.metric(
        "📈 Daily Return",
        f"{daily_return:.2f}%"
    )

    c3.metric(
        "🤖 Recommendation",
        recommendation
    )

    c4.metric(
        "🎯 Confidence",
        f"{confidence:.2f}%"
    )

    st.divider()

    # ===============================
    # Stock Price Chart
    # ===============================

    st.subheader("📈 Stock Price Trend")

    fig = px.line(
        data,
        x="Date",
        y="Close",
        markers=True,
        title=f"{stock_symbol} Price"
    )

    fig.update_layout(
        template="plotly_white",
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ===============================
    # Daily Return Chart
    # ===============================

    st.subheader("📊 Daily Return")

    fig2 = px.bar(
        data,
        x="Date",
        y="Daily Return (%)"
    )

    fig2.update_layout(
        template="plotly_white",
        height=400
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

elif page == "Investment Analysis":

    st.title("📈 Investment Analysis")

    latest = data.iloc[-1]

    # ==========================================
    # Load Data
    # ==========================================

   
    latest = data.iloc[-1]

    # ==========================================
    # KPI Cards
    # ==========================================
    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
       "Current Price",
       f"₹ {latest['Close']:.2f}"
   )   

    c2.metric(
       "MA20",
       f"₹ {latest['MA20']:.2f}"
    )

    c3.metric(
       "MA50",
       f"₹ {latest['MA50']:.2f}"
    )

    c4.metric(
       "Daily Return",
       f"{latest['Daily Return (%)']:.2f}%"
    )

    # ==========================================
    # Closing Price Chart
    # ==========================================

    st.subheader("📈 Closing Price Trend")

    fig = px.line(
    data,
    x="Date",
    y="Close",
    title=f"{stock_symbol} Closing Price"
)

    fig.update_layout(
        template="plotly_white",
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ==========================================
    # Moving Average Chart
    # ==========================================

    st.subheader("📊 Moving Averages")

    fig2 = px.line(
    data,
    x="Date",
    y=["MA20","MA50"]
)

    fig2.update_layout(
        template="plotly_white",
        height=450
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    # ==========================================
    # Daily Return Chart
    # ==========================================

    st.subheader("📉 Daily Return")

    fig3 = px.bar(
    data,
    x="Date",
    y="Daily Return (%)",
    title="Daily Returns"
)

    fig3.update_layout(
        template="plotly_white",
        height=400
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    # ==========================================
    # Risk Summary
    # ==========================================
    
    st.subheader("⚠ Risk Analysis")

    volatility = data["Daily Return (%)"].std()

    if volatility < 1:
        risk_level = "Low Risk"
    elif volatility < 2:
        risk_level = "Medium Risk"
    else:
        risk_level = "High Risk"

    st.metric(
        "Risk Level",
        risk_level
    )

    st.metric(
       "Volatility",
       f"{volatility:.2f}%"
    )
elif page == "AI Recommendation":

    st.title("🤖 AI Investment Recommendation")

    # ==============================
    # Latest Stock Data
    # ==============================

    latest = data.iloc[-1]

    close_price = float(latest["Close"])
    ma20 = float(latest["MA20"])
    ma50 = float(latest["MA50"])

    # ==============================
    # Recommendation Logic
    # ==============================

    score = 0

    # Trend
    if close_price > ma20:
        score += 20

    if close_price > ma50:
        score += 20

    # MA Crossover
    if ma20 > ma50:
        score += 20

    # Momentum (use safe indexing)
    if len(data) >= 6:
        last_5_return = ((data["Close"].iloc[-1] / data["Close"].iloc[-6] - 1) * 100)
    else:
        last_5_return = 0

    if last_5_return > 3:
        score += 20

    # Volatility
    volatility = data["Daily Return (%)"].std()

    if volatility < 2:
        score += 20

    # Derive recommendation, confidence and market trend
    confidence = float(score)

    if score >= 70:
        recommendation = "BUY"
    elif score >= 40:
        recommendation = "HOLD"
    else:
        recommendation = "SELL"

    if ma20 > ma50:
        market_trend = "Bullish"
    elif ma20 < ma50:
        market_trend = "Bearish"
    else:
        market_trend = "Neutral"

    # ==============================
    # Risk Analysis
    # ==============================

    if volatility < 1:
        risk_level = "Low"
    elif volatility < 2:
        risk_level = "Medium"
    else:
        risk_level = "High"

    # ==============================
    # KPI Cards
    # ==============================

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "🤖 Recommendation",
        recommendation
    )

    c2.metric(
        "🎯 Confidence",
        f"{confidence:.2f}%"
    )

    c3.metric(
        "⚠ Risk Level",
        risk_level
    )

    c4.metric(
        "📈 Market Trend",
        market_trend
    )

    st.divider()

    # ==============================
    # Confidence Meter
    # ==============================

    st.subheader("🎯 AI Confidence")

    st.progress(confidence / 100)

    st.write(
        f"Confidence Score: {confidence:.2f}%"
    )

    st.divider()

    st.write("### Decision Factors")

    st.write(f"Close Price: ₹{close_price:.2f}")
    st.write(f"20 Day MA: ₹{ma20:.2f}")
    st.write(f"50 Day MA: ₹{ma50:.2f}")
    st.write(f"5 Day Momentum: {last_5_return:.2f}%")
    st.write(f"Volatility: {volatility:.2f}%")
    st.write(f"AI Score: {score}/100")
    # ==============================
    # AI Explanation
    # ==============================

    st.subheader("🧠 AI Explanation")

    st.write(
        f"""
The AI analysed:

• Current Price = ₹{close_price:.2f}

• 20-Day MA = ₹{ma20:.2f}

• 50-Day MA = ₹{ma50:.2f}

• Market Trend = {market_trend}

• Risk Level = {risk_level}
"""
    )

    if recommendation == "BUY":

        st.success(
            "The stock is trading above both moving averages. Momentum is positive."
        )

    elif recommendation == "SELL":

        st.error(
            "The stock is trading below important moving averages. Momentum is weak."
        )

    else:

        st.warning(
            "The stock is in a neutral zone. Wait for stronger confirmation."
        )

elif page == "Portfolio":

    st.title("💼 Portfolio Analysis")

    try:
        portfolio = pd.read_csv("data/portfolio_analysis.csv")

    except Exception as e:
        st.error(f"Unable to load portfolio data: {e}")
        st.stop()

    # ==========================================
    # Portfolio Metrics
    # ==========================================

    investment = portfolio["Investment"].sum()
    current_value = portfolio["Current Value"].sum()

    profit = current_value - investment

    return_percent = (
        (profit / investment) * 100
        if investment > 0 else 0
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "💰 Investment",
        f"₹ {investment:,.2f}"
    )

    c2.metric(
        "💼 Current Value",
        f"₹ {current_value:,.2f}"
    )

    c3.metric(
        "📈 Profit",
        f"₹ {profit:,.2f}"
    )

    c4.metric(
        "📊 Return %",
        f"{return_percent:.2f}%"
    )

    st.divider()

    # ==========================================
    # Portfolio Allocation
    # ==========================================

    st.subheader("🥧 Portfolio Allocation")

    if len(portfolio) > 0:

        fig = px.pie(
            portfolio,
            names="Stock",
            values="Current Value",
            hole=0.45
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.warning("Portfolio data is empty.")

    st.divider()

    # ==========================================
    # Portfolio Performance
    # ==========================================

    st.subheader("📊 Portfolio Performance")

    fig2 = px.bar(
        portfolio,
        x="Stock",
        y="Return (%)",
        color="Return (%)",
        text="Return (%)"
    )

    fig2.update_layout(
        template="plotly_white",
        height=450
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.divider()

    # ==========================================
    # Portfolio Table
    # ==========================================

    st.subheader("📋 Portfolio Details")

    st.dataframe(
        portfolio,
        use_container_width=True
    )

elif page == "Market Analysis":

    st.title("🌍 Market Analysis")

    # ======================================
    # Load Data
    # ======================================

    try:
       market = pd.read_csv(
          "data/market_trends.csv",
           skiprows=[1,2]
    )

       market.rename(
           columns={"Price": "Date"},
           inplace=True
       )

       summary = pd.read_csv(
            "data/market_movement_summary.csv")

    except Exception as e:
        st.error(f"Unable to load market data: {e}")
        st.stop()

    market["Open"] = pd.to_numeric(
      market["Open"],
      errors="coerce"
   )

    market["Close"] = pd.to_numeric(
      market["Close"],
    errors="coerce"
   )

    market["High"] = pd.to_numeric(
      market["High"],
      errors="coerce"
    )

    market["Low"] = pd.to_numeric(
      market["Low"],
      errors="coerce"
    )

    market["Volume"] = pd.to_numeric(
       market["Volume"],
       errors="coerce"
    )

    latest = market.iloc[-1]

    # ======================================
    # KPI Cards
    # ======================================

    c1, c2, c3, c4 = st.columns(4)

    open_price = float(latest["Open"])
    close_price = float(latest["Close"])
    high_price = float(latest["High"])
    low_price = float(latest["Low"])

    c1.metric(
      "Open",
      f"₹ {open_price:.2f}"
    )

    c2.metric(
      "Close",
      f"₹ {close_price:.2f}"
    )

    c3.metric(
       "High",
       f"₹ {high_price:.2f}"
    )

    c4.metric(
      "Low",
       f"₹ {low_price:.2f}"
    )
    st.divider()

    # ======================================
    # Closing Price Chart
    # ======================================

    st.subheader("📈 Market Closing Price")

    fig = px.line(
        market,
        x="Date",
        y="Close",
        markers=True
    )

    fig.update_layout(
        template="plotly_white",
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # ======================================
    # Trading Volume
    # ======================================

    st.subheader("📊 Trading Volume")

    fig2 = px.bar(
        market,
        x="Date",
        y="Volume"
    )

    fig2.update_layout(
        template="plotly_white",
        height=400
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.divider()

    # ======================================
    # Market Summary
    # ======================================

    st.subheader("📋 Market Summary")

    st.dataframe(
        summary,
        use_container_width=True
    )

elif page == "Reports":

    st.title("📄 AI Investment Report")

    latest = data.iloc[-1]

    close_price = float(latest["Close"])
    daily_return = float(latest["Daily Return (%)"])
    cumulative_return = float(latest["Cumulative Return (%)"])

    # Recommendation Logic
# Calculate AI Score
score = 0

ma20 = float(latest["MA20"])
ma50 = float(latest["MA50"])

# Trend
if close_price > ma20:
    score += 20

if close_price > ma50:
    score += 20

# Moving Average Trend
if ma20 > ma50:
    score += 20

# Momentum
last_5_return = (
    (data["Close"].iloc[-1] /
     data["Close"].iloc[-6] - 1)
    * 100
)

if last_5_return > 3:
    score += 20

# Volatility
volatility = data["Daily Return (%)"].std()

if volatility < 2:
    score += 20
    
    if score >= 80:
        recommendation = "STRONG BUY"
    elif score >= 60:
        recommendation = "BUY"
    elif score >= 40:
        recommendation = "HOLD"
    elif score >= 20:
        recommendation = "SELL"
    else:
        recommendation = "STRONG SELL"

    confidence = score

    # Risk

    volatility = data["Daily Return (%)"].std()

    if volatility < 1:
        risk_level = "Low"
    elif volatility < 2:
        risk_level = "Medium"
    else:
        risk_level = "High"

    # ==========================
    # Report Preview
    # ==========================

    st.subheader("📋 Report Preview")

    st.write("### Stock Summary")

    st.write(f"Current Price : ₹ {close_price:.2f}")
    st.write(f"Daily Return : {daily_return:.2f}%")
    st.write(f"Cumulative Return : {cumulative_return:.2f}%")

    st.divider()

    st.write("### AI Recommendation")

    st.success(recommendation)

    st.write(f"Confidence : {confidence:.2f}%")

    st.divider()

    st.write("### Risk Summary")

    st.write(risk_level)

    st.divider()

    # ==========================
    # Generate PDF
    # ==========================

    if st.button("Generate PDF Report"):

        styles = getSampleStyleSheet()

        pdf = SimpleDocTemplate(
            "Investment_Report.pdf"
        )

        story = []

        story.append(
            Paragraph(
                "AI Investment Recommendation Report",
                styles["Heading1"]
            )
        )

        story.append(
            Paragraph(
                f"Generated : {datetime.now()}",
                styles["Normal"]
            )
        )

        story.append(
            Paragraph(
                f"Current Price : ₹ {close_price:.2f}",
                styles["Normal"]
            )
        )

        story.append(
            Paragraph(
                f"Daily Return : {daily_return:.2f}%",
                styles["Normal"]
            )
        )

        story.append(
            Paragraph(
                f"Recommendation : {recommendation}",
                styles["Normal"]
            )
        )

        story.append(
            Paragraph(
                f"Confidence : {confidence:.2f}%",
                styles["Normal"]
            )
        )

        story.append(
            Paragraph(
                f"Risk Level : {risk_level}",
                styles["Normal"]
            )
        )

        pdf.build(story)

        st.success("PDF Generated Successfully!")

        with open(
            "Investment_Report.pdf",
            "rb"
        ) as file:

            st.download_button(
                label="⬇ Download PDF",
                data=file,
                file_name="Investment_Report.pdf",
                mime="application/pdf"
            )

elif page == "Risk Analysis":

    st.title("⚠️ Risk Analysis")

    returns = data["Daily Return (%)"].dropna()

    volatility = returns.std()

    risk_score = min(
        round(volatility * 10, 2),
        100
    )

    if risk_score < 20:
        risk_category = "Low Risk"
    elif risk_score < 50:
        risk_category = "Medium Risk"
    else:
        risk_category = "High Risk"

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Risk Score",
        risk_score
    )

    c2.metric(
        "Volatility",
        f"{volatility:.2f}"
    )

    c3.metric(
        "Risk Category",
        risk_category
    )

    st.divider()

    st.subheader("📊 Return Distribution")

    fig = px.histogram(
        data,
        x="Daily Return (%)",
        nbins=40
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    st.subheader("📈 Rolling Volatility")

    data["Rolling Risk"] = (
        data["Daily Return (%)"]
        .rolling(20)
        .std()
    )

    fig2 = px.line(
        data,
        x="Date",
        y="Rolling Risk"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.divider()

    st.subheader("🧠 AI Risk Summary")

    if risk_category == "Low Risk":

        st.success(
            "Low volatility stock."
        )

    elif risk_category == "Medium Risk":

        st.warning(
            "Moderate volatility stock."
        )

    else:

        st.error(
            "High volatility stock."
        )

elif page == "Stock Comparison":

    st.title("📊 Stock Comparison")

    stock1 = st.selectbox(
        "Stock 1",
        [
            "RELIANCE.NS",
            "TCS.NS",
            "INFY.NS",
            "HDFCBANK.NS"
        ]
    )

    stock2 = st.selectbox(
        "Stock 2",
        [
            "RELIANCE.NS",
            "TCS.NS",
            "INFY.NS",
            "HDFCBANK.NS"
        ]
    )

    data1 = yf.download(
        stock1,
        period="1y"
    )

    data2 = yf.download(
        stock2,
        period="1y"
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data1.index,
            y=data1["Close"],
            name=stock1
        )
    )

    fig.add_trace(
        go.Scatter(
            x=data2.index,
            y=data2["Close"],
            name=stock2
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

elif page == "Portfolio Optimization":

    st.title("🎯 Portfolio Optimization")

    portfolio = pd.read_csv(
        "data/portfolio_analysis.csv"
    )

    total_value = portfolio[
        "Current Value"
    ].sum()

    portfolio["Weight (%)"] = (
        portfolio["Current Value"]
        / total_value
        * 100
    )

    st.subheader(
        "Current Allocation"
    )

    st.dataframe(
        portfolio,
        use_container_width=True
    )

    st.divider()

    st.subheader(
        "AI Suggestions"
    )

    for _, row in portfolio.iterrows():

        if row["Weight (%)"] > 50:

            st.warning(
                f"Reduce allocation in {row['Stock']}."
            )

        else:

            st.success(
                f"{row['Stock']} allocation looks healthy."
            )

    diversification_score = (
        100
        - portfolio["Weight (%)"].max()
    )

    st.metric(
        "Diversification Score",
        f"{diversification_score:.2f}"
    )

elif page == "About Project":

    st.title("📘 About AI Investment Recommendation System")

    st.markdown("""
    ## Project Objective

    This AI-powered platform helps investors:

    - Analyze stock performance
    - Compare stocks
    - Evaluate portfolio performance
    - Understand market trends
    - Receive AI-based recommendations
    - Generate investment reports

    ## Technologies Used

    - Python
    - Streamlit
    - Pandas
    - Plotly
    - Yahoo Finance API
    - ReportLab

    ## Features

    ✅ Dashboard

    ✅ Investment Analysis

    ✅ AI Recommendation

    ✅ Portfolio Analysis

    ✅ Market Analysis

    ✅ PDF Reports

    ✅ Stock Comparison

    ## Developed By

    AI Investment Recommendation System
    """)

st.markdown("---")

st.caption(
    "AI Investment Recommendation System | Streamlit + Python + AI Analytics"
)