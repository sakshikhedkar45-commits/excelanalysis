import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf # For live stock data

# 1. Page & Aesthetic Config
st.set_page_config(page_title="Ultra Finance Dashboard", layout="wide", page_icon="💰")

# Premium Dark Theme CSS
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #0e1117; border-right: 1px solid #30363d; }
    .stMetric { border: 1px solid #00d4ff; border-radius: 12px; padding: 20px; box-shadow: 2px 2px 10px rgba(0,212,255,0.1); }
    div.stButton > button:first-child { background-color: #00d4ff; color: black; border-radius: 8px; font-weight: bold; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar with Live Stock Ticker
with st.sidebar:
    st.header("📈 Live Market Watch")
    ticker = st.text_input("Enter Stock Ticker (e.g., RELIANCE.NS, TSLA, AAPL)", value="RELIANCE.NS")
    if st.button("Get Live Price"):
        try:
            stock = yf.Ticker(ticker)
            price = stock.history(period="1d")['Close'].iloc[-1]
            currency = stock.info.get('currency', '$')
            st.metric(f"Current {ticker}", f"{currency} {price:,.2f}")
        except:
            st.error("Ticker not found. Use .NS for Indian stocks.")
    
    st.divider()
    uploaded_file = st.file_uploader("📂 Upload Excel/CSV Report", type=['csv', 'xlsx'])
    st.caption("Perfect for SIP tracking, fundamental analysis, or portfolio reports.")

# 3. Main Dashboard Header
st.title("💎 Premium Finance Analytics")
st.markdown("Automated insights for your financial reports.")

if uploaded_file is not None:
    try:
        # Load Data
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        num_cols = df.select_dtypes(include=['number']).columns.tolist()
        cat_cols = df.select_dtypes(include=['object']).columns.tolist()

        if num_cols:
            # 4. Top Row: Key Intelligence
            st.subheader("📊 High-Level Summary")
            k1, k2, k3, k4 = st.columns(4)
            
            # Simple "Financial Health" logic based on growth or totals
            total = df[num_cols[0]].sum()
            avg = df[num_cols[0]].mean()
            
            k1.metric("Portfolio Total", f"{total:,.0f}")
            k2.metric("Mean Value", f"{avg:,.2f}")
            k3.metric("Max Impact", f"{df[num_cols[0]].max():,.0f}")
            
            # Interactive Score
            score = 85 if avg > 0 else 40
            k4.metric("Health Score", f"{score}/100", delta="Excellent" if score > 70 else "Warning")

            st.divider()

            # 5. Visualizations
            c1, c2 = st.columns([1.5, 1])

            with c1:
                st.subheader("🔥 Growth Visualization")
                y_var = st.selectbox("Select Metric for Chart", num_cols)
                x_var = st.selectbox("Select Category/Date", cat_cols + num_cols)
                
                fig = px.bar(df, x=x_var, y=y_var, text_auto='.2s',
                             color=y_var, color_continuous_scale='Tealgrn',
                             template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)

            with c2:
                st.subheader("🎯 Share Distribution")
                pie_var = st.selectbox("Select Dimension", cat_cols)
                fig_pie = px.sunburst(df, path=[pie_var], values=y_var,
                                     color_discrete_sequence=px.colors.qualitative.Prism,
                                     template="plotly_dark")
                st.plotly_chart(fig_pie, use_container_width=True)

            # 6. AI Narrative Section
            st.subheader("🧠 Automated Narrative Report")
            with st.expander("Click to read the AI-generated analysis", expanded=True):
                st.write(f"""
                ### Executive Summary:
                * **Market Concentration:** Your highest performing category is **{df.loc[df[y_var].idxmax(), x_var]}**, contributing significantly to the total volume.
                * **Sustainability:** With an average of **{avg:,.2f}**, the data indicates a {"stable" if avg > 0 else "volatile"} financial environment.
                * **Recommendation:** Focus on assets that fall within the top 10% of your max value ({df[y_var].max() * 0.9:,.0f}) to ensure consistent compounding growth.
                """)
        
        else:
            st.warning("Please ensure your Excel has columns with numbers.")

    except Exception as e:
        st.error(f"Error reading file: {e}")

else:
    # Attractive Placeholder
    st.info("👋 Welcome! Please upload your data in the sidebar to begin your professional analysis.")
    st.image("https://images.unsplash.com/photo-1611974717482-98252c6a4932?q=80&w=2070&auto=format&fit=crop", caption="Data-Driven Decisions")
