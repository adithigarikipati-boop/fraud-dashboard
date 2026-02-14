"""
Professional Financial Statement & Fraud Analysis Dashboard
Companies: WorldCom, IL&FS, Xerox Corporation, Bhushan Steel
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# =======================
# DATA PREPARATION
# =======================

def load_company_data():
    """Load financial data for all companies"""
    
    # WorldCom Data (2000-2002) - Accounting Fraud
    worldcom = pd.DataFrame({
        'Year': [2000, 2001, 2002],
        'Revenue': [39.090e9, 35.179e9, 30.360e9],
        'COGS': [23.854e9, 20.663e9, 17.842e9],
        'Operating_Expenses': [8.644e9, 10.586e9, 11.046e9],
        'EBIT': [6.592e9, 3.930e9, 1.472e9],
        'Net_Income': [7.577e9, 1.501e9, -3.852e9],
        'Total_Assets': [103.279e9, 164.496e9, 107.036e9],
        'Current_Assets': [14.931e9, 18.301e9, 12.047e9],
        'Fixed_Assets': [85.348e9, 143.195e9, 92.989e9],
        'Current_Liabilities': [19.803e9, 24.983e9, 29.896e9],
        'Total_Debt': [28.079e9, 41.838e9, 45.358e9],
        'Total_Equity': [39.838e9, 35.267e9, 15.296e9],
        'Receivables': [7.874e9, 9.468e9, 6.815e9],
        'Inventory': [0.5e9, 0.6e9, 0.4e9],
        'Retained_Earnings': [15.0e9, 16.5e9, 12.6e9],
        'Market_Cap': [115.0e9, 45.0e9, 0.15e9],
        'Depreciation': [6.5e9, 7.2e9, 8.1e9]
    })
    
    # IL&FS Data (2015-2018) - Infrastructure Lending Crisis
    ilfs = pd.DataFrame({
        'Year': [2015, 2016, 2017, 2018],
        'Revenue': [120.5e8, 135.2e8, 148.9e8, 142.3e8],
        'COGS': [45.2e8, 52.1e8, 58.7e8, 62.4e8],
        'Operating_Expenses': [32.4e8, 38.5e8, 42.6e8, 48.9e8],
        'EBIT': [42.9e8, 44.6e8, 47.6e8, 31.0e8],
        'Net_Income': [24.8e8, 26.5e8, 28.3e8, -18.2e8],
        'Total_Assets': [920.5e8, 1045.8e8, 1189.4e8, 1150.6e8],
        'Current_Assets': [185.4e8, 210.6e8, 245.8e8, 220.3e8],
        'Fixed_Assets': [675.1e8, 755.2e8, 843.6e8, 830.3e8],
        'Current_Liabilities': [245.6e8, 298.7e8, 356.4e8, 425.8e8],
        'Total_Debt': [685.4e8, 798.5e8, 925.6e8, 989.4e8],
        'Total_Equity': [145.2e8, 152.3e8, 165.8e8, 85.2e8],
        'Receivables': [95.4e8, 108.2e8, 125.6e8, 115.8e8],
        'Inventory': [12.4e8, 14.5e8, 16.2e8, 14.8e8],
        'Retained_Earnings': [85.4e8, 95.2e8, 105.8e8, 62.4e8],
        'Market_Cap': [180.0e8, 195.0e8, 210.0e8, 45.0e8],
        'Depreciation': [38.5e8, 42.3e8, 46.8e8, 51.2e8]
    })
    
    # Xerox Corporation Data (1997-2000) - Revenue Recognition Fraud
    xerox = pd.DataFrame({
        'Year': [1997, 1998, 1999, 2000],
        'Revenue': [18.166e9, 19.447e9, 19.228e9, 18.632e9],
        'COGS': [9.456e9, 10.234e9, 10.128e9, 9.845e9],
        'Operating_Expenses': [5.234e9, 5.678e9, 6.012e9, 6.234e9],
        'EBIT': [3.476e9, 3.535e9, 3.088e9, 2.553e9],
        'Net_Income': [1.452e9, 1.392e9, 1.424e9, 1.264e9],
        'Total_Assets': [31.489e9, 32.567e9, 34.872e9, 35.456e9],
        'Current_Assets': [11.234e9, 12.456e9, 13.567e9, 13.892e9],
        'Fixed_Assets': [18.255e9, 18.111e9, 19.305e9, 19.564e9],
        'Current_Liabilities': [9.567e9, 10.234e9, 11.456e9, 12.234e9],
        'Total_Debt': [15.234e9, 16.456e9, 18.234e9, 19.456e9],
        'Total_Equity': [9.255e9, 9.111e9, 8.638e9, 8.000e9],
        'Receivables': [5.234e9, 6.123e9, 7.234e9, 7.892e9],
        'Inventory': [2.456e9, 2.567e9, 2.678e9, 2.734e9],
        'Retained_Earnings': [6.234e9, 6.892e9, 7.456e9, 7.892e9],
        'Market_Cap': [25.5e9, 28.4e9, 22.6e9, 18.2e9],
        'Depreciation': [1.567e9, 1.678e9, 1.789e9, 1.892e9]
    })
    
    # Bhushan Steel Data (2014-2017) - Debt Default & Fraud
    bhushan = pd.DataFrame({
        'Year': [2014, 2015, 2016, 2017],
        'Revenue': [78.45e8, 85.67e8, 82.34e8, 75.89e8],
        'COGS': [62.34e8, 68.45e8, 67.89e8, 65.23e8],
        'Operating_Expenses': [8.56e8, 9.45e8, 10.23e8, 11.45e8],
        'EBIT': [7.55e8, 7.77e8, 4.22e8, -0.79e8],
        'Net_Income': [3.45e8, 2.89e8, -2.45e8, -8.67e8],
        'Total_Assets': [445.67e8, 478.92e8, 492.34e8, 485.67e8],
        'Current_Assets': [125.34e8, 135.67e8, 138.92e8, 132.45e8],
        'Fixed_Assets': [298.33e8, 321.25e8, 331.42e8, 331.22e8],
        'Current_Liabilities': [98.45e8, 112.34e8, 145.67e8, 178.92e8],
        'Total_Debt': [285.67e8, 325.89e8, 368.92e8, 398.45e8],
        'Total_Equity': [82.34e8, 85.23e8, 82.78e8, 74.11e8],
        'Receivables': [45.67e8, 52.34e8, 56.78e8, 58.92e8],
        'Inventory': [32.45e8, 35.67e8, 37.89e8, 36.23e8],
        'Retained_Earnings': [45.67e8, 48.56e8, 46.11e8, 37.44e8],
        'Market_Cap': [125.0e8, 110.0e8, 75.0e8, 35.0e8],
        'Depreciation': [18.45e8, 20.23e8, 21.67e8, 22.89e8]
    })
    
    return {
        'worldcom': worldcom,
        'ilfs': ilfs,
        'xerox': xerox,
        'bhushan': bhushan
    }

# =======================
# FRAUD DETECTION MODELS
# =======================

def calculate_altman_z_score(df):
    """
    Altman Z-Score for bankruptcy prediction
    Z = 1.2*X1 + 1.4*X2 + 3.3*X3 + 0.6*X4 + 1.0*X5
    
    Interpretation:
    Z > 2.99: Safe Zone
    1.81 < Z < 2.99: Grey Zone
    Z < 1.81: Distress Zone
    """
    working_capital = df['Current_Assets'] - df['Current_Liabilities']
    
    X1 = working_capital / df['Total_Assets']
    X2 = df['Retained_Earnings'] / df['Total_Assets']
    X3 = df['EBIT'] / df['Total_Assets']
    X4 = df['Market_Cap'] / (df['Total_Assets'] - df['Total_Equity'])
    X5 = df['Revenue'] / df['Total_Assets']
    
    z_score = 1.2*X1 + 1.4*X2 + 3.3*X3 + 0.6*X4 + 1.0*X5
    
    return z_score

def calculate_beneish_m_score(df):
    """
    Beneish M-Score for earnings manipulation detection
    M-Score > -1.78: Likely Manipulator
    M-Score < -1.78: Unlikely Manipulator
    """
    m_scores = []
    
    for i in range(1, len(df)):
        current = df.iloc[i]
        previous = df.iloc[i-1]
        
        # DSRI - Days Sales in Receivables Index
        dsri = (current['Receivables']/current['Revenue']) / (previous['Receivables']/previous['Revenue'])
        
        # GMI - Gross Margin Index
        gmi = ((previous['Revenue']-previous['COGS'])/previous['Revenue']) / \
              ((current['Revenue']-current['COGS'])/current['Revenue'])
        
        # AQI - Asset Quality Index
        current_ca_fa = current['Current_Assets'] + current['Fixed_Assets']
        previous_ca_fa = previous['Current_Assets'] + previous['Fixed_Assets']
        aqi = (1 - current_ca_fa/current['Total_Assets']) / \
              (1 - previous_ca_fa/previous['Total_Assets'])
        
        # SGI - Sales Growth Index
        sgi = current['Revenue'] / previous['Revenue']
        
        # DEPI - Depreciation Index
        depi = (previous['Depreciation']/(previous['Depreciation']+previous['Fixed_Assets'])) / \
               (current['Depreciation']/(current['Depreciation']+current['Fixed_Assets']))
        
        # SGAI - Sales General and Administrative Expenses Index
        sgai = (current['Operating_Expenses']/current['Revenue']) / \
               (previous['Operating_Expenses']/previous['Revenue'])
        
        # LVGI - Leverage Index
        lvgi = ((current['Total_Debt'])/current['Total_Assets']) / \
               ((previous['Total_Debt'])/previous['Total_Assets'])
        
        # TATA - Total Accruals to Total Assets
        current_ca = current['Current_Assets'] - current['Receivables']
        current_cl = current['Current_Liabilities']
        tata = (current['Net_Income'] - (current_ca - current_cl)) / current['Total_Assets']
        
        # M-Score calculation
        m_score = -4.84 + 0.92*dsri + 0.528*gmi + 0.404*aqi + 0.892*sgi + \
                  0.115*depi - 0.172*sgai + 4.679*tata - 0.327*lvgi
        
        m_scores.append(m_score)
    
    return [np.nan] + m_scores

def benfords_law_analysis(financial_values):
    """
    Benford's Law analysis for fraud detection
    Returns actual vs expected distribution and chi-square statistic
    """
    # Extract first digits
    first_digits = []
    for value in financial_values:
        if value > 0:
            first_digit = int(str(int(value))[0])
            if first_digit != 0:
                first_digits.append(first_digit)
    
    # Calculate actual distribution
    actual_counts = pd.Series(first_digits).value_counts().sort_index()
    actual_dist = (actual_counts / len(first_digits) * 100).reindex(range(1, 10), fill_value=0)
    
    # Benford's expected distribution
    expected_dist = pd.Series({i: np.log10(1 + 1/i) * 100 for i in range(1, 10)})
    
    # Chi-square statistic
    chi_square = sum(((actual_dist - expected_dist)**2) / expected_dist)
    
    # Critical value at 95% confidence for 8 degrees of freedom is 15.507
    compliant = chi_square < 15.507
    
    return actual_dist, expected_dist, chi_square, compliant

# =======================
# FINANCIAL RATIOS
# =======================

def calculate_all_ratios(df):
    """Calculate comprehensive financial ratios"""
    ratios = pd.DataFrame()
    ratios['Year'] = df['Year']
    
    # Profitability Ratios
    ratios['Gross_Margin'] = ((df['Revenue'] - df['COGS']) / df['Revenue'] * 100)
    ratios['Operating_Margin'] = (df['EBIT'] / df['Revenue'] * 100)
    ratios['Net_Profit_Margin'] = (df['Net_Income'] / df['Revenue'] * 100)
    ratios['ROA'] = (df['Net_Income'] / df['Total_Assets'] * 100)
    ratios['ROE'] = (df['Net_Income'] / df['Total_Equity'] * 100)
    
    # Liquidity Ratios
    ratios['Current_Ratio'] = df['Current_Assets'] / df['Current_Liabilities']
    ratios['Quick_Ratio'] = (df['Current_Assets'] - df['Inventory']) / df['Current_Liabilities']
    
    # Leverage Ratios
    ratios['Debt_to_Equity'] = df['Total_Debt'] / df['Total_Equity']
    ratios['Debt_Ratio'] = (df['Total_Debt'] / df['Total_Assets'] * 100)
    ratios['Equity_Ratio'] = (df['Total_Equity'] / df['Total_Assets'] * 100)
    
    # Efficiency Ratios
    ratios['Asset_Turnover'] = df['Revenue'] / df['Total_Assets']
    ratios['Receivables_Turnover'] = df['Revenue'] / df['Receivables']
    ratios['Days_Sales_Outstanding'] = 365 / ratios['Receivables_Turnover']
    
    return ratios

def common_size_analysis(df):
    """Vertical analysis - express items as % of revenue"""
    common_size = pd.DataFrame()
    common_size['Year'] = df['Year']
    common_size['Revenue'] = 100.0
    common_size['COGS'] = (df['COGS'] / df['Revenue'] * 100)
    common_size['Operating_Expenses'] = (df['Operating_Expenses'] / df['Revenue'] * 100)
    common_size['EBIT'] = (df['EBIT'] / df['Revenue'] * 100)
    common_size['Net_Income'] = (df['Net_Income'] / df['Revenue'] * 100)
    
    return common_size

def trend_analysis(df):
    """Horizontal analysis - calculate % change year over year"""
    trend = pd.DataFrame()
    trend['Year'] = df['Year'][1:]
    
    for col in ['Revenue', 'Net_Income', 'Total_Assets', 'Total_Debt', 'Total_Equity']:
        trend[f'{col}_Change_%'] = df[col].pct_change() * 100
    
    return trend[1:]

def comparative_analysis(all_data, year, metric):
    """Compare all companies for a specific metric"""
    comparison = {}
    for company, df in all_data.items():
        if year in df['Year'].values:
            comparison[company.upper()] = df[df['Year'] == year][metric].values[0]
    
    return comparison

# =======================
# VISUALIZATION FUNCTIONS
# =======================

def create_fraud_score_gauge(score, threshold_low, threshold_high, title, color_scheme):
    """Create a professional gauge chart for fraud scores"""

    if score > threshold_high:
        color = '#10b981'  # Green - Safe
        status = "Low Risk"
    elif score > threshold_low:
        color = '#f59e0b'  # Orange - Warning
        status = "Medium Risk"
    else:
        color = '#ef4444'  # Red - High Risk
        status = "High Risk"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        title={'text': f"{title}<br><span style='font-size:0.8em;color:{color}'>{status}</span>"},
        gauge={
            'axis': {'range': [None, threshold_high * 1.5]},
            'bar': {'color': color},
            'steps': [
                {'range': [threshold_low * -2, threshold_low], 'color': '#d1fae5'},
                {'range': [threshold_low, threshold_high], 'color': '#fef3c7'},
                {'range': [threshold_high, threshold_high * 1.5], 'color': '#fee2e2'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': threshold_high
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': color_scheme['text'], 'family': 'Inter, sans-serif'}
    )
    
    return fig

def create_benfords_chart(actual_dist, expected_dist, chi_square, compliant):
    """Create Benford's Law comparison chart"""
    
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=list(range(1, 10)),
        y=expected_dist.values,
        name='Expected (Benford)',
        marker_color='#3b82f6',  # Professional Blue
        opacity=0.85,
        marker_line=dict(color='#1e40af', width=1.5)
    ))

    fig.add_trace(go.Bar(
        x=list(range(1, 10)),
        y=actual_dist.values,
        name='Actual',
        marker_color='#10b981',  # Green (less alarming than red)
        opacity=0.85,
        marker_line=dict(color='#065f46', width=1.5)
    ))
    
    compliance_text = "✓ COMPLIANT" if compliant else "✗ NON-COMPLIANT"
    compliance_color = "#10b981" if compliant else "#ef4444"
    
    fig.update_layout(
        title={
            'text': f"Benford's Law Analysis<br><sub>χ² = {chi_square:.2f} - <span style='color:{compliance_color}'>{compliance_text}</span></sub>",
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title="First Digit",
        yaxis_title="Frequency (%)",
        barmode='group',
        height=400,
        hovermode='x unified',
        template='plotly_dark',
        paper_bgcolor = 'rgba(0,0,0,0)',
        plot_bgcolor = 'rgba(30,41,59,0.5)'
    )
    
    return fig

def create_ratio_spider_chart(ratios_df, selected_years):
    """Create spider/radar chart for ratio analysis"""
    
    categories = ['Gross_Margin', 'Net_Profit_Margin', 'ROA', 'ROE', 
                  'Current_Ratio', 'Asset_Turnover']
    
    fig = go.Figure()
    
    colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444']
    
    for idx, year in enumerate(selected_years):
        year_data = ratios_df[ratios_df['Year'] == year]
        if not year_data.empty:
            values = [year_data[cat].values[0] for cat in categories]
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name=str(year),
                line_color=colors[idx % len(colors)]
            ))

    fig.update_layout(
        polar=dict(
            bgcolor='rgba(15,23,42,0.8)',
            radialaxis=dict(
                visible=True,
                range=[0, max(100, ratios_df[categories].max().max())],
                gridcolor='rgba(100,116,139,0.3)',
                linecolor='rgba(148,163,184,0.3)',
                tickfont=dict(color='#f1f5f9')
            ),
            angularaxis=dict(
                gridcolor='rgba(100,116,139,0.3)',
                linecolor='rgba(148,163,184,0.3)',
                tickfont=dict(color='#f1f5f9')
            )
        ),
        showlegend=True,
        title={
            'text': "Financial Ratios - Multi-Year Comparison",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#f1f5f9'}
        },
        height=500,
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(15,23,42,0.8)',
        font={'color': '#f1f5f9'},
        legend=dict(
            font=dict(color='#f1f5f9'),
            bgcolor='rgba(30,41,59,0.8)',
            bordercolor='rgba(148,163,184,0.3)',
            borderwidth=1
        )
    )
    
    return fig

def create_waterfall_chart(df, year):
    """Create waterfall chart for income statement"""
    
    year_data = df[df['Year'] == year].iloc[0]
    
    fig = go.Figure(go.Waterfall(
        name="Income Statement",
        orientation="v",
        measure=["relative", "relative", "relative", "total"],
        x=["Revenue", "COGS", "Operating Expenses", "EBIT"],
        textposition="outside",
        text=[f"${year_data['Revenue']/1e9:.2f}B",
              f"-${year_data['COGS']/1e9:.2f}B",
              f"-${year_data['Operating_Expenses']/1e9:.2f}B",
              f"${year_data['EBIT']/1e9:.2f}B"],
        y=[year_data['Revenue'], 
           -year_data['COGS'],
           -year_data['Operating_Expenses'],
           year_data['EBIT']],
        connector={"line": {"color": "rgb(63, 63, 63)"}},
    ))

    fig.update_layout(
        title={
            'text': f"Income Statement Breakdown - {year}",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#f1f5f9'}
        },
        showlegend=False,
        height=400,
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',  # Fully transparent
        plot_bgcolor='rgba(0,0,0,0)',  # Fully transparent
        font={'color': '#f1f5f9'},
        xaxis=dict(color='#f1f5f9', showgrid=False),
        yaxis=dict(color='#f1f5f9', gridcolor='rgba(100,116,139,0.2)')
    )
    
    return fig

# =======================
# DASHBOARD APP
# =======================

# Initialize the Dash app with Bootstrap theme
app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# Load all company data
all_company_data = load_company_data()

# Define color schemes
COLOR_SCHEME = {
    'bg': '#0f172a',
    'card': '#1e293b',
    'accent': '#3b82f6',
    'success': '#10b981',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    'text': '#f1f5f9'
}

# Custom CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Financial Fraud Analysis Dashboard</title>
        {%favicon%}
        {%css%}
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Inter', sans-serif;
                background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
                margin: 0;
                padding: 0;
            }
            .dashboard-header {
                background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
                padding: 2rem;
                border-bottom: 3px solid #3b82f6;
                box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            }
            .dashboard-title {
                font-size: 2.5rem;
                font-weight: 700;
                color: #f1f5f9;
                margin: 0;
                text-align: center;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            }
            .dashboard-subtitle {
                text-align: center;
                color: #94a3b8;
                margin-top: 0.5rem;
                font-size: 1.1rem;
            }
            .metric-card {
                background: #1e293b;
                border-radius: 12px;
                padding: 1.5rem;
                margin: 1rem 0;
                box-shadow: 0 4px 6px rgba(0,0,0,0.3);
                border-left: 4px solid #3b82f6;
                transition: transform 0.2s;
            }
            .metric-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 6px 12px rgba(59,130,246,0.4);
            }
            .section-header {
                font-size: 1.8rem;
                font-weight: 600;
                color: #f1f5f9;
                margin: 2rem 0 1rem 0;
                padding-bottom: 0.5rem;
                border-bottom: 2px solid #3b82f6;
            }
            .fraud-indicator {
                padding: 1rem;
                border-radius: 8px;
                margin: 0.5rem 0;
                font-weight: 600;
            }
            .fraud-high {
                background: #7f1d1d;
                color: #fecaca;
                border-left: 4px solid #ef4444;
            }
            .fraud-medium {
                background: #78350f;
                color: #fed7aa;
                border-left: 4px solid #f59e0b;
            }
            .fraud-low {
                background: #064e3b;
                color: #a7f3d0;
                border-left: 4px solid #10b981;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Dashboard Layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("Financial Statement & Fraud Analysis Dashboard", className="dashboard-title"),
        html.P("Advanced Analytics for Corporate Fraud Detection", className="dashboard-subtitle"),
    ], className="dashboard-header"),
    
    # Main Container
    dbc.Container([
        # Control Panel
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Select Company", style={'color': COLOR_SCHEME['text']}),
                        dcc.Dropdown(
                            id='company-dropdown',
                            options=[
                                {'label': '🏢 WorldCom (2000-2002)', 'value': 'worldcom'},
                                {'label': '🏗️ IL&FS (2015-2018)', 'value': 'ilfs'},
                                {'label': '🖨️ Xerox Corporation (1997-2000)', 'value': 'xerox'},
                                {'label': '🏭 Bhushan Steel (2014-2017)', 'value': 'bhushan'}
                            ],
                            value='worldcom',
                            style={'color': '#000', 'fontSize': '1.1rem'},
                            clearable=False
                        ),
                    ])
                ], style={'background': COLOR_SCHEME['card'], 'marginTop': '2rem', 'border': 'none'})
            ], width=6),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Select Analysis Year", style={'color': COLOR_SCHEME['text']}),
                        dcc.Dropdown(
                            id='year-dropdown',
                            style={'color': '#000', 'fontSize': '1.1rem'},
                            clearable=False
                        ),
                    ])
                ], style={'background': COLOR_SCHEME['card'], 'marginTop': '2rem', 'border': 'none'})
            ], width=6),
        ]),
        
        # Company Info Banner
        html.Div(id='company-info-banner', style={'marginTop': '2rem'}),
        
        # Fraud Detection Section
        html.Div([
            html.H2("🔍 Fraud Detection Models", className="section-header"),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='z-score-gauge')
                ], width=4),
                dbc.Col([
                    dcc.Graph(id='m-score-gauge')
                ], width=4),
                dbc.Col([
                    html.Div(id='fraud-summary-card')
                ], width=4),
            ]),
        ]),
        
        # Benford's Law Analysis
        html.Div([
            html.H2("📊 Benford's Law Analysis", className="section-header"),
            dcc.Graph(id='benfords-chart'),
        ]),
        
        # Financial Ratios Section
        html.Div([
            html.H2("📈 Financial Ratios Analysis", className="section-header"),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='profitability-ratios')
                ], width=6),
                dbc.Col([
                    dcc.Graph(id='liquidity-ratios')
                ], width=6),
            ]),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='leverage-ratios')
                ], width=6),
                dbc.Col([
                    dcc.Graph(id='efficiency-ratios')
                ], width=6),
            ]),
        ]),
        
        # Comparative Analysis Section
        html.Div([
            html.H2("🔄 Comparative Analysis", className="section-header"),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='common-size-chart')
                ], width=6),
                dbc.Col([
                    dcc.Graph(id='trend-chart')
                ], width=6),
            ]),
        ]),
        
        # Income Statement Breakdown
        html.Div([
            html.H2("💰 Income Statement Analysis", className="section-header"),
            dcc.Graph(id='waterfall-chart'),
        ]),
        
        # Multi-Year Ratio Spider Chart
        html.Div([
            html.H2("🕸️ Multi-Year Ratio Comparison", className="section-header"),
            dcc.Graph(id='spider-chart'),
        ]),
        
        # Red Flags Section
        html.Div([
            html.H2("🚩 Red Flags Detected", className="section-header"),
            html.Div(id='red-flags-section')
        ]),
        
    ], fluid=True, style={'padding': '2rem'}),
    
], style={'background': COLOR_SCHEME['bg'], 'minHeight': '100vh'})

# =======================
# CALLBACKS
# =======================

@app.callback(
    Output('year-dropdown', 'options'),
    Output('year-dropdown', 'value'),
    Input('company-dropdown', 'value')
)
def update_year_dropdown(company):
    """Update available years based on selected company"""
    df = all_company_data[company]
    years = df['Year'].tolist()
    options = [{'label': str(year), 'value': year} for year in years]
    return options, years[-1]  # Default to most recent year

@app.callback(
    Output('company-info-banner', 'children'),
    Input('company-dropdown', 'value')
)
def update_company_info(company):
    """Display company information banner"""
    
    company_info = {
        'worldcom': {
            'name': 'WorldCom',
            'fraud': 'Accounting Fraud - $11 billion',
            'period': '2000-2002',
            'description': 'WorldCom inflated assets by booking operating expenses as capital expenditures, leading to one of the largest accounting frauds in history.'
        },
        'ilfs': {
            'name': 'Infrastructure Leasing & Financial Services (IL&FS)',
            'fraud': 'Debt Default Crisis - ₹91,000 crore',
            'period': '2015-2018',
            'description': 'IL&FS defaulted on debt obligations, revealing major accounting irregularities and poor governance practices.'
        },
        'xerox': {
            'name': 'Xerox Corporation',
            'fraud': 'Revenue Recognition Fraud - $6 billion',
            'period': '1997-2000',
            'description': 'Xerox manipulated revenue recognition by accelerating lease revenue and improperly accounting for equipment sales.'
        },
        'bhushan': {
            'name': 'Bhushan Steel',
            'fraud': 'Bank Fraud & Debt Default - ₹47,000 crore',
            'period': '2014-2017',
            'description': 'Bhushan Steel was involved in fraudulent loans and fund diversion, leading to insolvency proceedings.'
        }
    }
    
    info = company_info[company]

    return dbc.Alert([
        html.H3(f"🏢 {info['name']}", style={
            'marginBottom': '0.5rem',
            'color': '#f1f5f9',
            'fontWeight': '700'
        }),
        html.H5(f"⚠️ {info['fraud']}", style={
            'color': '#fb923c',
            'fontWeight': '600',
            'marginTop': '0.75rem'
        }),
        html.P(f"📅 Period: {info['period']}", style={
            'marginTop': '1rem',
            'color': '#cbd5e1',
            'fontSize': '1rem'
        }),
        html.P(info['description'], style={
            'marginTop': '1rem',
            'fontSize': '1rem',
            'color': '#e2e8f0',
            'lineHeight': '1.6'
        }),
    ], style={
        'background': 'linear-gradient(135deg, #1e293b 0%, #334155 100%)',
        'border': '2px solid #ef4444',
        'borderRadius': '12px',
        'padding': '1.5rem',
        'boxShadow': '0 4px 6px rgba(0,0,0,0.3)'
    })

@app.callback(
    Output('z-score-gauge', 'figure'),
    Output('m-score-gauge', 'figure'),
    Output('fraud-summary-card', 'children'),
    Input('company-dropdown', 'value'),
    Input('year-dropdown', 'value')
)
def update_fraud_scores(company, year):
    """Update fraud detection scores"""
    
    df = all_company_data[company]
    
    # Calculate Z-Score
    z_scores = calculate_altman_z_score(df)
    year_idx = df[df['Year'] == year].index[0]
    z_score = z_scores.iloc[year_idx]
    
    # Calculate M-Score
    m_scores = calculate_beneish_m_score(df)
    m_score = m_scores[year_idx] if not np.isnan(m_scores[year_idx]) else 0
    
    # Create gauges
    z_fig = create_fraud_score_gauge(z_score, 1.81, 2.99, "Altman Z-Score", COLOR_SCHEME)
    m_fig = create_fraud_score_gauge(m_score, -2.22, -1.78, "Beneish M-Score", COLOR_SCHEME)
    
    # Fraud summary
    z_risk = "High" if z_score < 1.81 else ("Medium" if z_score < 2.99 else "Low")
    m_risk = "High" if m_score > -1.78 else "Low"
    
    z_class = f"fraud-{z_risk.lower()}"
    m_class = f"fraud-{m_risk.lower()}"
    
    summary = html.Div([
        html.H4("Fraud Risk Summary", style={'color': COLOR_SCHEME['text'], 'textAlign': 'center'}),
        html.Div([
            html.Div([
                html.H5("Z-Score Risk", style={'color': COLOR_SCHEME['text']}),
                html.H3(z_risk, style={'margin': '0.5rem 0'})
            ], className=f"fraud-indicator {z_class}"),
            html.Div([
                html.H5("M-Score Risk", style={'color': COLOR_SCHEME['text']}),
                html.H3(m_risk, style={'margin': '0.5rem 0'})
            ], className=f"fraud-indicator {m_class}", style={'marginTop': '1rem'}),
        ]),
        html.Div([
            html.P(f"Analysis Year: {year}", style={'color': COLOR_SCHEME['text'], 'marginTop': '2rem', 'textAlign': 'center'}),
            html.P(f"Z-Score: {z_score:.3f}", style={'color': COLOR_SCHEME['text'], 'textAlign': 'center'}),
            html.P(f"M-Score: {m_score:.3f}", style={'color': COLOR_SCHEME['text'], 'textAlign': 'center'}),
        ])
    ])
    
    return z_fig, m_fig, summary

@app.callback(
    Output('benfords-chart', 'figure'),
    Input('company-dropdown', 'value')
)
def update_benfords(company):
    """Update Benford's Law analysis"""
    
    df = all_company_data[company]
    
    # Collect all financial values for analysis
    financial_values = []
    for col in ['Revenue', 'COGS', 'Operating_Expenses', 'Total_Assets', 'Current_Assets', 
                'Current_Liabilities', 'Total_Debt', 'Receivables']:
        financial_values.extend(df[col].tolist())
    
    actual_dist, expected_dist, chi_square, compliant = benfords_law_analysis(financial_values)
    
    return create_benfords_chart(actual_dist, expected_dist, chi_square, compliant)

@app.callback(
    Output('profitability-ratios', 'figure'),
    Output('liquidity-ratios', 'figure'),
    Output('leverage-ratios', 'figure'),
    Output('efficiency-ratios', 'figure'),
    Input('company-dropdown', 'value')
)
def update_ratio_charts(company):
    """Update all ratio charts"""
    
    df = all_company_data[company]
    ratios = calculate_all_ratios(df)
    
    # Profitability Ratios
    prof_fig = go.Figure()
    prof_fig.add_trace(go.Scatter(x=ratios['Year'], y=ratios['Gross_Margin'], 
                                   mode='lines+markers', name='Gross Margin %',
                                   line=dict(color='#10b981', width=3)))
    prof_fig.add_trace(go.Scatter(x=ratios['Year'], y=ratios['Net_Profit_Margin'], 
                                   mode='lines+markers', name='Net Profit Margin %',
                                   line=dict(color='#3b82f6', width=3)))
    prof_fig.add_trace(go.Scatter(x=ratios['Year'], y=ratios['ROA'], 
                                   mode='lines+markers', name='ROA %',
                                   line=dict(color='#f59e0b', width=3)))
    prof_fig.update_layout(title="Profitability Ratios", template='plotly_dark', height=400)
    
    # Liquidity Ratios
    liq_fig = go.Figure()
    liq_fig.add_trace(go.Scatter(x=ratios['Year'], y=ratios['Current_Ratio'], 
                                  mode='lines+markers', name='Current Ratio',
                                  line=dict(color='#8b5cf6', width=3)))
    liq_fig.add_trace(go.Scatter(x=ratios['Year'], y=ratios['Quick_Ratio'], 
                                  mode='lines+markers', name='Quick Ratio',
                                  line=dict(color='#ec4899', width=3)))
    liq_fig.add_hline(y=1.0, line_dash="dash", line_color="red", 
                      annotation_text="Minimum Safe Level")
    liq_fig.update_layout(title="Liquidity Ratios", template='plotly_dark', height=400)
    
    # Leverage Ratios
    lev_fig = go.Figure()
    lev_fig.add_trace(go.Scatter(x=ratios['Year'], y=ratios['Debt_to_Equity'], 
                                  mode='lines+markers', name='Debt to Equity',
                                  line=dict(color='#ef4444', width=3)))
    lev_fig.add_trace(go.Scatter(x=ratios['Year'], y=ratios['Debt_Ratio'], 
                                  mode='lines+markers', name='Debt Ratio %',
                                  line=dict(color='#f59e0b', width=3)))
    lev_fig.update_layout(title="Leverage Ratios", template='plotly_dark', height=400)
    
    # Efficiency Ratios
    eff_fig = go.Figure()
    eff_fig.add_trace(go.Scatter(x=ratios['Year'], y=ratios['Asset_Turnover'], 
                                  mode='lines+markers', name='Asset Turnover',
                                  line=dict(color='#06b6d4', width=3)))
    eff_fig.add_trace(go.Scatter(x=ratios['Year'], y=ratios['Days_Sales_Outstanding'], 
                                  mode='lines+markers', name='Days Sales Outstanding',
                                  line=dict(color='#84cc16', width=3), yaxis='y2'))
    eff_fig.update_layout(
        title="Efficiency Ratios",
        template='plotly_dark',
        height=400,
        yaxis2=dict(title="DSO (Days)", overlaying='y', side='right')
    )
    
    return prof_fig, liq_fig, lev_fig, eff_fig

@app.callback(
    Output('common-size-chart', 'figure'),
    Output('trend-chart', 'figure'),
    Input('company-dropdown', 'value')
)
def update_comparative_analysis(company):
    """Update common-size and trend analysis"""
    
    df = all_company_data[company]
    
    # Common-Size Analysis
    common_size = common_size_analysis(df)
    
    cs_fig = go.Figure()
    cs_fig.add_trace(go.Bar(x=common_size['Year'], y=common_size['COGS'], 
                            name='COGS', marker_color='#ef4444'))
    cs_fig.add_trace(go.Bar(x=common_size['Year'], y=common_size['Operating_Expenses'], 
                            name='Operating Expenses', marker_color='#f59e0b'))
    cs_fig.add_trace(go.Bar(x=common_size['Year'], y=common_size['EBIT'], 
                            name='EBIT', marker_color='#10b981'))
    cs_fig.update_layout(
        title="Common-Size Analysis (% of Revenue)",
        barmode='stack',
        template='plotly_dark',
        height=400,
        yaxis_title="Percentage of Revenue"
    )
    
    # Trend Analysis
    trend = trend_analysis(df)
    
    trend_fig = go.Figure()
    for col in [c for c in trend.columns if c != 'Year']:
        trend_fig.add_trace(go.Scatter(
            x=trend['Year'], 
            y=trend[col], 
            mode='lines+markers',
            name=col.replace('_Change_%', ''),
            line=dict(width=3)
        ))
    trend_fig.add_hline(y=0, line_dash="dash", line_color="white")
    trend_fig.update_layout(
        title="Trend Analysis (YoY % Change)",
        template='plotly_dark',
        height=400,
        yaxis_title="% Change"
    )
    
    return cs_fig, trend_fig

@app.callback(
    Output('waterfall-chart', 'figure'),
    Input('company-dropdown', 'value'),
    Input('year-dropdown', 'value')
)
def update_waterfall(company, year):
    """Update waterfall chart"""
    
    df = all_company_data[company]
    return create_waterfall_chart(df, year)

@app.callback(
    Output('spider-chart', 'figure'),
    Input('company-dropdown', 'value')
)
def update_spider_chart(company):
    """Update multi-year spider chart"""
    
    df = all_company_data[company]
    ratios = calculate_all_ratios(df)
    years = df['Year'].tolist()
    
    return create_ratio_spider_chart(ratios, years)

@app.callback(
    Output('red-flags-section', 'children'),
    Input('company-dropdown', 'value'),
    Input('year-dropdown', 'value')
)
def update_red_flags(company, year):
    """Identify and display red flags"""
    
    df = all_company_data[company]
    ratios = calculate_all_ratios(df)
    
    year_data = df[df['Year'] == year].iloc[0]
    year_ratios = ratios[ratios['Year'] == year].iloc[0]
    
    red_flags = []
    
    # Check for declining profitability
    if year_ratios['Net_Profit_Margin'] < 5:
        red_flags.append({
            'title': '📉 Low Net Profit Margin',
            'description': f"Net profit margin of {year_ratios['Net_Profit_Margin']:.2f}% indicates poor profitability.",
            'severity': 'high'
        })
    
    # Check liquidity
    if year_ratios['Current_Ratio'] < 1.0:
        red_flags.append({
            'title': '💧 Liquidity Crisis',
            'description': f"Current ratio of {year_ratios['Current_Ratio']:.2f} suggests inability to meet short-term obligations.",
            'severity': 'high'
        })
    
    # Check leverage
    if year_ratios['Debt_to_Equity'] > 2.0:
        red_flags.append({
            'title': '⚖️ High Leverage',
            'description': f"Debt-to-equity ratio of {year_ratios['Debt_to_Equity']:.2f} indicates excessive debt burden.",
            'severity': 'medium'
        })
    
    # Check asset quality
    if len(df) > 1:
        prev_year_idx = df[df['Year'] == year].index[0] - 1
        if prev_year_idx >= 0:
            prev_receivables_ratio = df.iloc[prev_year_idx]['Receivables'] / df.iloc[prev_year_idx]['Revenue']
            curr_receivables_ratio = year_data['Receivables'] / year_data['Revenue']
            
            if curr_receivables_ratio > prev_receivables_ratio * 1.2:
                red_flags.append({
                    'title': '📋 Growing Receivables',
                    'description': f"Receivables growing faster than revenue - potential revenue recognition issues.",
                    'severity': 'medium'
                })
    
    # Check negative equity
    if year_data['Total_Equity'] < 0:
        red_flags.append({
            'title': '🚨 Negative Equity',
            'description': "Company has negative equity - liabilities exceed assets.",
            'severity': 'high'
        })
    
    # Check Z-Score
    z_scores = calculate_altman_z_score(df)
    year_idx = df[df['Year'] == year].index[0]
    z_score = z_scores.iloc[year_idx]
    
    if z_score < 1.81:
        red_flags.append({
            'title': '⚠️ Bankruptcy Risk',
            'description': f"Z-Score of {z_score:.2f} indicates high probability of bankruptcy.",
            'severity': 'high'
        })
    
    # Create red flag cards
    if not red_flags:
        return dbc.Alert("✅ No major red flags detected for this period.", color="success")
    
    flag_cards = []
    for flag in red_flags:
        color = 'danger' if flag['severity'] == 'high' else 'warning'
        flag_cards.append(
            dbc.Alert([
                html.H4(flag['title'], style={'marginBottom': '0.5rem'}),
                html.P(flag['description'], style={'marginBottom': 0})
            ], color=color, style={'margin': '1rem 0'})
        )
    
    return html.Div(flag_cards)

# =======================
# RUN APP
# =======================

if __name__ == '__main__':
    print("\n" + "="*80)
    print("🚀 FINANCIAL FRAUD ANALYSIS DASHBOARD")
    print("="*80)
    print("\n📊 Dashboard is starting...")
    print("🌐 Open your browser and navigate to: http://127.0.0.1:8050")
    print("\n💡 Features:")
    print("   • Altman Z-Score Analysis")
    print("   • Beneish M-Score Detection")
    print("   • Benford's Law Analysis")
    print("   • Comprehensive Financial Ratios")
    print("   • Common-Size & Trend Analysis")
    print("   • Red Flag Detection")
    print("\n⚠️  Press Ctrl+C to stop the server")
    print("="*80 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=8050)
