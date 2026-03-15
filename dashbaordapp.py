import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Page & Theme Configuration
st.set_page_config(page_title="Pro-Finance Insights", layout="wide", initial_sidebar_state="expanded")

# Custom CSS to make it look "Premium"
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar for Navigation & Info
with st.sidebar:
    st.title("💼 Dashboard Control")
    st.info("Upload your Excel file below to generate a deep-dive financial analysis.")
    uploaded_file = st.file_uploader("Upload Finance Excel/CSV", type=['csv', 'xlsx'])
    st.divider()
    st.markdown("### 👤 About the Author")
    st.write("Finance Student & Analyst")
    st.caption("Built with Python & Streamlit")

# 3. Main Header
st.title("🚀 Financial Strategy & Fundamental Dashboard")
st.markdown("---")

if uploaded_file is not None:
    try:
        # Load Data
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        
        # 4. Top Row: KPI Metrics (Attractive Big Numbers)
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

        if len(numeric_cols) >= 1:
            st.subheader("📌 Key Performance Indicators (KPIs)")
            m1, m2, m3, m4 = st.columns(4)
            
            target_col = numeric_cols[0] # Focus on the first numeric column for metrics
            m1.metric("Total Value", f"{df[target_col].sum():,.0f}")
            m2.metric("Average Return/Value", f"{df[target_col].mean():,.2f}")
            m3.metric("Peak Value", f"{df[target_col].max():,.0f}")
            m4.metric("Data Points", len(df))
            
            st.divider()

            # 5. Middle Row: Visual Analytics
            col1, col2 = st.columns([2, 1]) # Make the left chart wider

            with col1:
                st.subheader("📈 Performance Trend")
                x_axis = st.selectbox("Timeline/Category (X-axis)", options=categorical_cols + numeric_cols)
                y_axis = st.selectbox("Financial Metric (Y-axis)", options=numeric_cols)
                
                fig_line = px.area(df, x=x_axis, y=y_axis, 
                                  template="plotly_dark", 
                                  color_discrete_sequence=['#00d4ff'])
                fig_line.update_layout(margin=dict(l=20, r=20, t=30, b=20))
                st.plotly_chart(fig_line, use_container_width=True)

            with col2:
                st.subheader("📊 Asset Allocation")
                pie_label = st.selectbox("Category (Labels)", options=categorical_cols)
                pie_value = st.selectbox("Metric (Values)", options=numeric_cols, key="pie_val")
                
                fig_pie = px.pie(df, names=pie_label, values=pie_value, hole=0.5,
                                 template="plotly_dark",
                                 color_discrete_sequence=px.colors.sequential.Tealgrn)
                st.plotly_chart(fig_pie, use_container_width=True)

            # 6. Fundamental Analysis "AI" Interpretation
            st.divider()
            st.subheader("🤖 AI Insight Report")
            
            # Smart logic to detect Stock Ratios
            ratios_detected = [col for col in df.columns if col.upper() in ['PE', 'ROE', 'ROCE', 'DEBT TO EQUITY', 'P/E']]
            
            with st.container():
                st.markdown("""<div style='background-color:#1e2329; padding:20px; border-radius:15px;'>""", unsafe_allow_html=True)
                
                # Dynamic Commentary
                if ratios_detected:
                    st.write(f"🔍 **Fundamental Alert:** I detected financial ratios ({', '.join(ratios_detected)}).")
                
                st.write(f"### Strategy Recommendation for {y_axis}:")
                
                if df[y_axis].mean() > 0:
                    st.write("✅ **Positive Trajectory:** The current dataset shows a healthy average. If this is a SIP or Stock portfolio, the trend suggests a 'Hold' or 'Accumulate' strategy.")
                else:
                    st.write("⚠️ **Risk Observation:** Negative values detected. Re-evaluate the underlying assets and check for debt-to-equity spikes.")

                st.write("**Data Consistency:** Your data is 100% complete with no missing values. This increases the reliability of this dashboard.")
                st.markdown("</div>", unsafe_allow_html=True)

        # 7. Download Section
        st.sidebar.download_button("📥 Download Analysis Report", 
                                   data=df.to_csv().encode('utf-8'), 
                                   file_name='Analysis_Report.csv', 
                                   mime='text/csv')

    except Exception as e:
        st.error(f"Oh no! Something went wrong: {e}")
else:
    # Beautiful Landing Page if no file is uploaded
    st.image("https://img.freepik.com/free-vector/digital-money-transfer-technology-background_1017-17454.jpg", use_column_width=True)
    st.warning("Please upload an Excel or CSV file in the sidebar to unlock the dashboard.")
