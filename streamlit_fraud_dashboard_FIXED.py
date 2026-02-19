"""
Professional Financial Statement & Fraud Analysis Dashboard - Streamlit Version
Companies: WorldCom, IL&FS, Xerox Corporation, Bhushan Steel
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Page Configuration
st.set_page_config(
    page_title="Fraud Analysis Dashboard",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    .stSelectbox {
        color: #f1f5f9;
    }
    h1 {
        color: #f1f5f9;
        text-align: center;
        padding: 2rem 0;
        border-bottom: 3px solid #3b82f6;
    }
    h2 {
        color: #f1f5f9;
        margin-top: 2rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #3b82f6;
    }
    h3 {
        color: #f1f5f9;
    }
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #3b82f6;
        margin: 1rem 0;
    }
    .stMetric {
        background: rgba(30,41,59,0.9);
        padding: 1rem;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# =======================
# DATA PREPARATION
# =======================

@st.cache_data
def load_company_data():
    """Load financial data for all companies"""
    
    # WorldCom Data (2000-2001) 
    worldcom = pd.DataFrame({
        'Year': [2000, 2001],
        'Revenue': [39090e6, 35181e6],
        'COGS': [ 15508e6, 15910e6],
        'SGA': [7421e6, 7547e6],
        'EBIT': [10345e6, 7519e6],
        'Net_Income': [5134e6, 1514e6],
        'Total_Assets': [104363e6, 107485e6],
        'Current_Assets': [21033e6, 19526e6],
        'Fixed_Assets': [54653e6, 58365e6],
        'Current_Liabilities': [17149e6, 20063e6],
        'Total_Debt': [30323e6, 31983e6],
        'Total_Equity': [46557e6, 45289e6],
        'Receivables': [5138e6, 6304e6],
        'Inventory': [1465e6, 1513e6],
        'Retained_Earnings': [17694e6, 19172e6],
        'Market_Cap': [115000e6, 45000e6],
        'Depreciation': [6373e6, 7490e6],
        'CFO':[10240e6, 7001e6]
    })
    
    # IL&FS Data (2015-2018)
    ilfs = pd.DataFrame({
        'Year': [2015, 2016, 2017, 2018],
        'Revenue': [192.125e8, 192.11557e8, 234.6465e8, 229.4347e8],
        'COGS': [45.2e8, 52.1e8, 58.7e8, 62.4e8],
        'SGA': [13.825e8, 16.5609e8, 18.9909e8, 19.0513e8],
        'EBIT': [161.6385e8, 154.0426e8, 177.9783e8, 167.9961e8],
        'Net_Income': [24.937e8, 19.2779e8, 20.8781e8, 9.9660e8],
        'Total_Assets': [1542.844e8, 1795.6088e8, 1956.2608e8, 2188.9279e8],
        'Current_Assets': [810.8627e8,  822.0826e8, 856.7468e8, 785.7735e8],
        'Fixed_Assets': [0.4806e8, 0.4472e8, 0.4046e8,  0.7968e8],
        'Current_Liabilities': [619.4992e8, 743.7955e8, 724.9711e8,  820.1098e8],
        'Total_Debt': [917.3757e8, 1233.7509e8, 1341.9523e8, 1475.5373e8],
        'Total_Equity': [203.1238e8, 230.6752e8, 240.7124e8, 239.9749e8],
        'Receivables': [16.9873e8, 15.1298e8, 18.8868e8, 26.6748e8],
        'Inventory': [0.0e8, 0.0e8, 0.0e8, 0.0e8],
        'Retained_Earnings': [176.557e8, 191.6085e8, 201.6457e8, 200.9082e8],
        'Market_Cap': [203.1238e8, 230.6752e8, 240.7124e8, 239.9749e8],#book equity
        'Depreciation': [0.2075e8, 0.1746e8, 0.2247e8, 0.2541e8],
        'CFO': [51.7917e8,  -35.4439e8, 9.2444e8, -283.6166e8],

    })
    
    # Xerox Corporation Data (1997-2000)
    xerox = pd.DataFrame({
        'Year': [1997, 1998, 1999, 2000],
        'Revenue': [18.166e9, 19.447e9, 19.228e9, 18.632e9],
        'COGS': [16.003e9, 18.684e9, 17.192e9, 19.186e9],
        'SGA': [5.517e9, 5.873e9, 5.603e9, 5.230e9],
        'EBIT': [2.141e9, 0.763e9, 2.036e9, -0.554e9],
        'Net_Income': [1.452e9, 0.395e9, 1.424e9, -0.384e9],
        'Total_Assets': [27.732e9, 30.024e9, 28.814e9, 29.687e9],
        'Current_Assets': [10.766e9, 12.475e9, 11.985e9, 13.094e9],
        'Fixed_Assets': [2.377e9, 2.386e9, 2.456e9, 2.495e9],
        'Current_Liabilities': [7.692e9, 8.507e9, 7.950e9, 6.286e9],
        'Total_Debt': [12.486e9, 14.971e9, 14.951e9, 18.097e9],
        'Total_Equity': [4.985e9, 4.857e9, 4.911e9, 3.637e9],
        'Receivables': [2.745e9, 2.671e9, 2.622e9, 2.281e9],
        'Inventory': [2.792e9, 3.269e9, 2.961e9, 1.930e9],
        'Retained_Earnings': [3.921e9, 3.348e9, 3.915e9, 2.879e9],
        'Market_Cap': [31.2e9, 28.6e9, 29.9e9, 15.4e9],
        'Depreciation': [1.543e9, 1.629e9, 1.718e9, 1.802e9],
        'CFO': [0.472e9, -1.165e9, 1.224e9, -0.827e9],

    })
    
    # Bhushan Steel Data (2014-2017)
    bhushan = pd.DataFrame({
       'Year': [2014, 2015, 2016, 2017],
       'Revenue': [7845.0e8, 8567.0e8, 8234.0e8, 7589.0e8],
       'COGS': [6234.0e8, 6845.0e8, 6789.0e8, 6523.0e8],
       'SGA': [856.0e8, 945.0e8, 1023.0e8, 1145.0e8],
       'EBIT': [755.0e8, 778.0e8, 422.0e8, -79.0e8],
       'Net_Income': [345.0e8, 289.0e8, -245.0e8, -867.0e8],
       'Total_Assets': [44567.0e8, 47892.0e8, 49234.0e8, 48567.0e8],
       'Current_Assets': [12534.0e8, 13567.0e8, 13892.0e8, 13245.0e8],
       'Fixed_Assets': [29833.0e8, 32125.0e8, 33142.0e8, 33122.0e8],
       'Current_Liabilities': [9845.0e8, 11234.0e8, 14567.0e8, 17892.0e8],
       'Total_Debt': [28567.0e8, 32589.0e8, 36892.0e8, 39845.0e8],
       'Total_Equity': [8234.0e8, 8523.0e8, 8278.0e8, 7411.0e8],
       'Receivables': [4567.0e8, 5234.0e8, 5678.0e8, 5892.0e8],
       'Inventory': [3245.0e8, 3567.0e8, 3789.0e8, 3623.0e8],
       'Retained_Earnings': [4567.0e8, 4856.0e8, 4611.0e8, 3744.0e8],
       'Market_Cap': [12500.0e8, 11000.0e8, 7500.0e8, 3500.0e8],
       'Depreciation': [1845.0e8, 2023.0e8, 2167.0e8, 2289.0e8],
       'CFO': [945.0e8, 812.0e8, -678.0e8, -1845.0e8],
   })

    
    return {
        'WorldCom': worldcom,
        'IL&FS': ilfs,
        'Xerox': xerox,
        'Bhushan Steel': bhushan
    }
# =======================
# FRAUD DETECTION MODELS
# =======================

def calculate_altman_z_score(df):
    """Altman Z-Score for bankruptcy prediction"""
    working_capital = df['Current_Assets'] - df['Current_Liabilities']
    
    X1 = working_capital / df['Total_Assets']
    X2 = df['Retained_Earnings'] / df['Total_Assets']
    X3 = df['EBIT'] / df['Total_Assets']
    X4 = df['Market_Cap'] / (df['Total_Assets'] - df['Total_Equity'])
    X5 = df['Revenue'] / df['Total_Assets']
    
    z_score = 1.2*X1 + 1.4*X2 + 3.3*X3 + 0.6*X4 + 1.0*X5
    
    return z_score

def calculate_beneish_m_score(df):
    """Beneish M-Score for earnings manipulation detection"""
    m_scores = []
    
    for i in range(1, len(df)):
        current = df.iloc[i]
        previous = df.iloc[i-1]
        
        dsri = (current['Receivables']/current['Revenue']) / (previous['Receivables']/previous['Revenue'])
        gmi = ((previous['Revenue']-previous['COGS'])/previous['Revenue']) / \
              ((current['Revenue']-current['COGS'])/current['Revenue'])
        
        current_ca_fa = current['Current_Assets'] + current['Fixed_Assets']
        previous_ca_fa = previous['Current_Assets'] + previous['Fixed_Assets']
        aqi = (1 - current_ca_fa/current['Total_Assets']) / \
              (1 - previous_ca_fa/previous['Total_Assets'])
        
        sgi = current['Revenue'] / previous['Revenue']
        depi = (previous['Depreciation']/(previous['Depreciation']+previous['Fixed_Assets'])) / \
               (current['Depreciation']/(current['Depreciation']+current['Fixed_Assets']))
        sgai = (current['SGA']/current['Revenue']) / \
               (previous['SGA']/previous['Revenue'])
        lvgi = ((current['Total_Debt'])/current['Total_Assets']) / \
               ((previous['Total_Debt'])/previous['Total_Assets'])
        
        current_ca = current['Current_Assets'] - current['Receivables']
        current_cl = current['Current_Liabilities']
        tata = (current['Net_Income'] - current['CFO']) / current['Total_Assets']
        
        m_score = -4.84 + 0.92*dsri + 0.528*gmi + 0.404*aqi + 0.892*sgi + \
                  0.115*depi - 0.172*sgai + 4.679*tata - 0.327*lvgi
        
        m_scores.append(m_score)
    
    return [np.nan] + m_scores

def benfords_law_analysis(financial_values):
    """Benford's Law analysis for fraud detection"""
    first_digits = []
    for value in financial_values:
        if value > 0:
            first_digit = int(str(int(value))[0])
            if first_digit != 0:
                first_digits.append(first_digit)
    
    actual_counts = pd.Series(first_digits).value_counts().sort_index()
    actual_dist = (actual_counts / len(first_digits) * 100).reindex(range(1, 10), fill_value=0)
    expected_dist = pd.Series({i: np.log10(1 + 1/i) * 100 for i in range(1, 10)})
    chi_square = sum(((actual_dist - expected_dist)**2) / expected_dist)
    compliant = chi_square < 15.507
    
    return actual_dist, expected_dist, chi_square, compliant

def calculate_all_ratios(df):
    """Calculate comprehensive financial ratios"""
    ratios = pd.DataFrame()
    ratios['Year'] = df['Year']
    
    # Profitability
    ratios['Gross_Margin'] = ((df['Revenue'] - df['COGS']) / df['Revenue'] * 100)
    ratios['Operating_Margin'] = (df['EBIT'] / df['Revenue'] * 100)
    ratios['Net_Profit_Margin'] = (df['Net_Income'] / df['Revenue'] * 100)
    ratios['ROA'] = (df['Net_Income'] / df['Total_Assets'] * 100)
    ratios['ROE'] = (df['Net_Income'] / df['Total_Equity'] * 100)
    
    # Liquidity
    ratios['Current_Ratio'] = df['Current_Assets'] / df['Current_Liabilities']
    ratios['Quick_Ratio'] = (df['Current_Assets'] - df['Inventory']) / df['Current_Liabilities']
    
    # Leverage
    ratios['Debt_to_Equity'] = df['Total_Debt'] / df['Total_Equity']
    ratios['Debt_Ratio'] = (df['Total_Debt'] / df['Total_Assets'] * 100)
    
    # Efficiency
    ratios['Asset_Turnover'] = df['Revenue'] / df['Total_Assets']
    ratios['Receivables_Turnover'] = df['Revenue'] / df['Receivables']
    ratios['Days_Sales_Outstanding'] = 365 / ratios['Receivables_Turnover']
    
    return ratios
    
def calculate_common_size(df):
    cs = pd.DataFrame()
    cs['Year'] = df['Year']
    cs['COGS_%'] = df['COGS'] / df['Revenue'] * 100
    cs['Net_Income_%'] = df['Net_Income'] / df['Revenue'] * 100
    return cs

def calculate_trend(df):
    trend = pd.DataFrame()
    trend['Year'] = df['Year']
    base = df.iloc[0]
    trend['Revenue_Index'] = df['Revenue'] / base['Revenue'] * 100
    return trend
# =======================
# MAIN APP
# =======================

def main():
    # Title
    st.markdown("<h1>🔍 Financial Statement & Fraud Analysis Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 1.2rem;'>Advanced Analytics for Corporate Fraud Detection</p>", unsafe_allow_html=True)
    
    # Load data
    all_data = load_company_data()
    
    # Sidebar
    st.sidebar.title("⚙️ Control Panel")
    
    company = st.sidebar.selectbox(
        "Select Company",
        list(all_data.keys()),
        format_func=lambda x: f"🏢 {x}"
    )
    
    df = all_data[company]
    years = df['Year'].tolist()
    
    selected_year = st.sidebar.selectbox(
        "Select Analysis Year",
        years,
        index=len(years)-1
    )
    
    # Company Info Banner
    company_info = {
        'WorldCom': {
            'fraud': 'Accounting Fraud - $11 billion',
            'period': '2000-2002',
            'description': 'WorldCom inflated assets by booking operating expenses as capital expenditures, leading to one of the largest accounting frauds in history.'
        },
        'IL&FS': {
            'fraud': 'Debt Default Crisis - ₹91,000 crore',
            'period': '2015-2018',
            'description': 'IL&FS defaulted on debt obligations, revealing major accounting irregularities and poor governance practices.'
        },
        'Xerox': {
            'fraud': 'Revenue Recognition Fraud - $6 billion',
            'period': '1997-2000',
            'description': 'Xerox manipulated revenue recognition by accelerating lease revenue and improperly accounting for equipment sales.'
        },
        'Bhushan Steel': {
            'fraud': 'Bank Fraud & Debt Default - ₹47,000 crore',
            'period': '2014-2017',
            'description': 'Bhushan Steel was involved in fraudulent loans and fund diversion, leading to insolvency proceedings.'
        }
    }
    
    info = company_info[company]
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #1e293b 0%, #334155 100%); 
                border-left: 5px solid #ef4444; 
                border-radius: 12px; 
                padding: 2rem; 
                margin: 2rem 0;
                box-shadow: 0 4px 12px rgba(0,0,0,0.4);'>
        <h2 style='color: #f1f5f9; margin-top: 0;'>🏢 {company}</h2>
        <div style='width: 60px; height: 4px; background: linear-gradient(90deg, #ef4444 0%, #f59e0b 100%); border-radius: 2px; margin: 1rem 0;'></div>
        <h4 style='color: #fbbf24; font-weight: 600;'>⚠️ {info['fraud']}</h4>
        <p style='color: #94a3b8; font-size: 1.1rem;'>📅 Period: {info['period']}</p>
        <p style='color: #cbd5e1; font-size: 1.05rem; line-height: 1.7;'>{info['description']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Fraud Detection Scores
    st.markdown("<h2>🔍 Fraud Detection Models</h2>", unsafe_allow_html=True)
    
    z_scores = calculate_altman_z_score(df)
    m_scores = calculate_beneish_m_score(df)
    
    year_idx = df[df['Year'] == selected_year].index[0]
    z_score = z_scores.iloc[year_idx]
    m_score = m_scores[year_idx]

    if np.isnan(m_score):
        m_display = "Not Available (First Year)"
    else:
        m_display = f"{m_score:.3f}"


    # Risk assessment
    if z_score > 2.99:
        z_risk = "Low"
        z_color = "#10b981"
    elif z_score > 1.81:
        z_risk = "Medium"
        z_color = "#f59e0b"
    else:
        z_risk = "High"
        z_color = "#ef4444"
    
    if m_score > -1.78:
        m_risk = "High"
        m_color = "#ef4444"
    else:
        m_risk = "Low"
        m_color = "#10b981"
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Z-Score Gauge
        fig_z = go.Figure(go.Indicator(
            mode="gauge+number",
            value=z_score,
            title={'text': f"Altman Z-Score<br><span style='font-size:0.8em;color:{z_color}'>{z_risk} Risk</span>"},
            gauge={
                'axis': {'range': [None, 5]},
                'bar': {'color': z_color},
                'steps': [
                    {'range': [0, 1.81], 'color': '#fee2e2'},
                    {'range': [1.81, 2.99], 'color': '#fef3c7'},
                    {'range': [2.99, 5], 'color': '#d1fae5'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 1.81
                }
            }
        ))
        fig_z.update_layout(
            height=300,
            paper_bgcolor='rgba(0,0,0,0)',
            font={'color': '#f1f5f9'},
            xaxis=dict(type='category')
        )
        st.plotly_chart(fig_z, use_container_width=True)
    
    with col2:
        # M-Score Gauge
        fig_m = go.Figure(go.Indicator(
            mode="gauge+number",
            value=m_score,
            title={'text': f"Beneish M-Score<br><span style='font-size:0.8em;color:{m_color}'>{m_risk} Risk</span>"},
            gauge={
                'axis': {'range': [-5, 0]},
                'bar': {'color': m_color},
                'steps': [
                    {'range': [-5, -2.22], 'color': '#d1fae5'},
                    {'range': [-2.22, -1.78], 'color': '#fef3c7'},
                    {'range': [-1.78, 0], 'color': '#fee2e2'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': -1.78
                }
            }
        ))
        fig_m.update_layout(
            height=300,
            paper_bgcolor='rgba(0,0,0,0)',
            font={'color': '#f1f5f9'},
            xaxis=dict(type='category')
        )
        st.plotly_chart(fig_m, use_container_width=True)
    
    with col3:
        st.markdown(f"""
        <div style='background: rgba(30,41,59,0.9); padding: 1.5rem; border-radius: 12px; text-align: center; margin-top: 40px;'>
            <h4 style='color: #f1f5f9;'>Analysis Year</h4>
            <h2 style='color: #3b82f6; font-size: 3rem;'>{selected_year}</h2>
            <p style='color: #94a3b8; margin-top: 1rem;'>Z-Score: {z_score:.3f}</p>
            <p style='color: #94a3b8;'>M-Score: {m_display}</p>
            
        </div>
        """, unsafe_allow_html=True)
    
    # Benford's Law
    st.markdown("<h2>📊 Benford's Law Analysis</h2>", unsafe_allow_html=True)
    
    financial_values = []
    for col in ['Revenue', 'COGS', 'SGA', 'Total_Assets', 'Current_Assets', 
                'Current_Liabilities', 'Total_Debt', 'Receivables']:
        financial_values.extend(df[col].tolist())
    
    actual_dist, expected_dist, chi_square, compliant = benfords_law_analysis(financial_values)
    
    fig_benford = go.Figure()
    fig_benford.add_trace(go.Bar(
        x=list(range(1, 10)),
        y=expected_dist.values,
        name='Expected (Benford)',
        marker_color='#3b82f6',
        opacity=0.85
    ))
    fig_benford.add_trace(go.Bar(
        x=list(range(1, 10)),
        y=actual_dist.values,
        name='Actual',
        marker_color='#10b981',
        opacity=0.85
    ))
    
    compliance_text = "✓ COMPLIANT" if compliant else "✗ NON-COMPLIANT"
    compliance_color = "#10b981" if compliant else "#ef4444"
    
    fig_benford.update_layout(
        title=f"Benford's Law Analysis - χ² = {chi_square:.2f} - <span style='color:{compliance_color}'>{compliance_text}</span>",
        xaxis_title="First Digit",
        yaxis_title="Frequency (%)",
        barmode='group',
        height=400,
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(15,23,42,0.8)',
        xaxis=dict(type='category')
    )
    
    st.plotly_chart(fig_benford, use_container_width=True)
    
    # Financial Ratios
        st.markdown("<h2>📈 Financial Ratios Analysis</h2>", unsafe_allow_html=True)
        ratios = calculate_all_ratios(df)
        analysis_tabs = st.tabs(["📊 Ratios","📑 Common Size","📈 Trend"])

    # ======================
    # RATIOS TAB
    # ======================
      with analysis_tabs[0]:
          tab1, tab2, tab3, tab4 = st.tabs(["📊 Profitability", "💧 Liquidity", "⚖️ Leverage", "⚡ Efficiency"])
          with tab1:
            fig_prof = go.Figure()
            fig_prof.add_trace(go.Scatter(x=ratios['Year'], y=ratios['Gross_Margin'], 
                                          mode='lines+markers+text', name='Gross Margin %',
                                          line=dict(color='#10b981', width=3)))
            fig_prof.add_trace(go.Scatter(x=ratios['Year'], y=ratios['Net_Profit_Margin'], 
                                          mode='lines+markers+text', name='Net Profit Margin %',
                                          line=dict(color='#3b82f6', width=3)))
            fig_prof.add_trace(go.Scatter(x=ratios['Year'], y=ratios['ROA'], 
                                          mode='lines+markers+text', name='ROA %',
                                          line=dict(color='#f59e0b', width=3)))
            fig_prof.add_hline(y=5, line_dash="dot", line_color="orange",
                               annotation_text="Low Profit Warning (5%)",
                               annotation_position="top right")
            fig_prof.add_hline(y=0, line_dash="dot", line_color="red",
                               annotation_text="Negative Return Zone",
                               annotation_position="bottom right")

            fig_prof.update_layout(
                title="Profitability Ratios", 
                template='plotly_dark', 
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(15,23,42,0.8)',
                xaxis=dict(type='category')
            )
            st.plotly_chart(fig_prof, use_container_width=True)

        # -------------------
        # LIQUIDITY
        # -------------------
        with tab2:
            fig_liq = go.Figure()
            fig_liq.add_trace(go.Scatter(x=ratios['Year'], y=ratios['Current_Ratio'], 
                                         mode='lines+markers+text', name='Current Ratio',
                                         line=dict(color='#8b5cf6', width=3)))
            fig_liq.add_trace(go.Scatter(x=ratios['Year'], y=ratios['Quick_Ratio'], 
                                         mode='lines+markers+text', name='Quick Ratio',
                                         line=dict(color='#ec4899', width=3)))
            fig_liq.add_hline(y=1.0, line_dash="dash", line_color="red", 
                              annotation_text="Minimum Safe Level",
                              annotation_position="top right")

            fig_liq.update_layout(
                title="Liquidity Ratios", 
                template='plotly_dark', 
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(15,23,42,0.8)',
                xaxis=dict(type='category')
            )
            st.plotly_chart(fig_liq, use_container_width=True)

        # -------------------
        # LEVERAGE
        # -------------------
        with tab3:
            fig_lev = go.Figure()
            fig_lev.add_trace(go.Scatter(x=ratios['Year'], y=ratios['Debt_to_Equity'], 
                                         mode='lines+markers+text', name='Debt to Equity',
                                         line=dict(color='#ef4444', width=3)))
            fig_lev.add_trace(go.Scatter(x=ratios['Year'], y=ratios['Debt_Ratio'], 
                                         mode='lines+markers+text', name='Debt Ratio %',
                                         line=dict(color='#f59e0b', width=3)))
            fig_lev.add_hline(y=2.0, line_dash="dot", line_color="red",
                              annotation_text="High Leverage Threshold (2.0)",
                              annotation_position="top right")

            fig_lev.update_layout(
                title="Leverage Ratios", 
                template='plotly_dark', 
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(15,23,42,0.8)',
                xaxis=dict(type='category')
            )
            st.plotly_chart(fig_lev, use_container_width=True)

        # -------------------
        # EFFICIENCY
        # -------------------
        with tab4:
            fig_eff = go.Figure()
            fig_eff.add_trace(go.Scatter(x=ratios['Year'], y=ratios['Asset_Turnover'], 
                                         mode='lines+markers+text', name='Asset Turnover',
                                         line=dict(color='#06b6d4', width=3)))

            fig_eff.update_layout(
                title="Efficiency Ratios", 
                template='plotly_dark', 
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(15,23,42,0.8)',
                xaxis=dict(type='category')
            )
            st.plotly_chart(fig_eff, use_container_width=True)
    # ======================
    # COMMON SIZE TAB
    # ======================
    with analysis_tabs[1]:
        cs = calculate_common_size(df)
        st.write(cs)
    # ======================
    # TREND TAB
    # ======================
    with analysis_tabs[2]:
        trend = calculate_trend(df)
        st.write(trend)

        # Red Flags
        st.markdown("<h2>🚩 Red Flags Detected</h2>", unsafe_allow_html=True)
    
        year_data = df[df['Year'] == selected_year].iloc[0]
        year_ratios = ratios[ratios['Year'] == selected_year].iloc[0]
    
        red_flags = []
    
        if year_ratios['Net_Profit_Margin'] < 5:
            red_flags.append("📉 Low Net Profit Margin")
        if year_ratios['Current_Ratio'] < 1.0:
            red_flags.append("💧 Liquidity Crisis")
        if year_ratios['Debt_to_Equity'] > 2.0:
            red_flags.append("⚖️ High Leverage")
        if z_score < 1.81:
            red_flags.append("⚠️ Bankruptcy Risk")
        if year_data['Total_Equity'] < 0:
            red_flags.append("🚨 Negative Equity")
    
        if red_flags:
            for flag in red_flags:
                st.error(flag)
        else:
            st.success("✅ No major red flags detected for this period.")
    
        # Footer
        st.markdown("---")
        st.markdown("<p style='text-align: center; color: #94a3b8;'>Financial Fraud Analysis Dashboard</p>", unsafe_allow_html=True)

    if __name__ == '__main__':
        main()
