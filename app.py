import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Page configuration
st.set_page_config(
    page_title="QA Defect Analytics Dashboard",
    page_icon="🐛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main > div {
        padding-top: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("🐛 QA Defect Analytics Dashboard")
st.markdown("**Comprehensive defect tracking and analytics for QA teams**")
st.markdown("---")

# Load data function with caching
@st.cache_data
def load_data(file):
    """Load and preprocess defect data"""
    try:
        df = pd.read_csv(file)
        
        # Convert dates
        df['reported_date'] = pd.to_datetime(df['reported_date'], errors='coerce')
        df['resolved_date'] = pd.to_datetime(df['resolved_date'], errors='coerce')
        
        # Calculate resolution time
        df['resolution_time'] = (df['resolved_date'] - df['reported_date']).dt.days
        
        # Extract month for time series
        df['reported_month'] = df['reported_date'].dt.to_period('M').astype(str)
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Sidebar - File upload
st.sidebar.header("📁 Data Source")
uploaded_file = st.sidebar.file_uploader(
    "Upload your defects CSV file", 
    type=['csv'],
    help="CSV with columns: defect_id, module, severity, status, reported_date, resolved_date, priority, assigned_to"
)

# Load data
if uploaded_file is not None:
    df = load_data(uploaded_file)
    st.sidebar.success("✅ Custom file loaded!")
else:
    try:
        df = load_data('defects.csv')
        st.sidebar.info("📊 Using sample dataset")
    except:
        st.error("No data file found. Please upload a CSV file.")
        st.stop()

if df is None:
    st.stop()

# Sidebar filters
st.sidebar.markdown("---")
st.sidebar.header("🔍 Filters")

# Severity filter
selected_severity = st.sidebar.multiselect(
    "Severity",
    options=sorted(df['severity'].unique().tolist()),
    default=sorted(df['severity'].unique().tolist())
)

# Status filter
selected_status = st.sidebar.multiselect(
    "Status",
    options=sorted(df['status'].unique().tolist()),
    default=sorted(df['status'].unique().tolist())
)

# Module filter
selected_modules = st.sidebar.multiselect(
    "Module/Component",
    options=sorted(df['module'].unique().tolist()),
    default=sorted(df['module'].unique().tolist())
)

# Date range filter
min_date = df['reported_date'].min().date()
max_date = df['reported_date'].max().date()

date_range = st.sidebar.date_input(
    "Reported Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Apply filters
filtered_df = df.copy()

if selected_severity:
    filtered_df = filtered_df[filtered_df['severity'].isin(selected_severity)]

if selected_status:
    filtered_df = filtered_df[filtered_df['status'].isin(selected_status)]

if selected_modules:
    filtered_df = filtered_df[filtered_df['module'].isin(selected_modules)]

if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        (filtered_df['reported_date'].dt.date >= start_date) & 
        (filtered_df['reported_date'].dt.date <= end_date)
    ]

# Sidebar metrics
st.sidebar.markdown("---")
st.sidebar.metric("📊 Total Records", len(df))
st.sidebar.metric("🔽 Filtered Records", len(filtered_df))

# Check if data exists
if len(filtered_df) == 0:
    st.warning("⚠️ No data matches the filters. Please adjust your filters.")
    st.stop()

# KEY METRICS
st.header("📊 Key Metrics")
col1, col2, col3, col4, col5 = st.columns(5)

total_defects = len(filtered_df)
col1.metric("Total Defects", total_defects)

open_defects = len(filtered_df[filtered_df['status'].isin(['Open', 'In Progress', 'Reopened'])])
closed_defects = len(filtered_df[filtered_df['status'].isin(['Resolved', 'Closed'])])
col2.metric("Open Defects", open_defects, delta=f"-{closed_defects} closed")

critical_count = len(filtered_df[filtered_df['severity'] == 'Critical'])
major_count = len(filtered_df[filtered_df['severity'] == 'Major'])
minor_count = len(filtered_df[filtered_df['severity'] == 'Minor'])

col3.metric("Critical", critical_count, delta="High Priority", delta_color="inverse")
col4.metric("Major", major_count)
col5.metric("Minor", minor_count)

# Average resolution time
avg_resolution = filtered_df['resolution_time'].mean()
if not np.isnan(avg_resolution):
    st.metric("⏱️ Average Resolution Time", f"{avg_resolution:.1f} days")
else:
    st.metric("⏱️ Average Resolution Time", "N/A")

st.markdown("---")

# VISUALIZATIONS
st.header("📈 Analytics & Visualizations")

col1, col2 = st.columns(2)

# Chart 1: Defects by Severity
with col1:
    st.subheader("Defects by Severity")
    severity_counts = filtered_df['severity'].value_counts().reset_index()
    severity_counts.columns = ['Severity', 'Count']
    
    color_map = {
        'Critical': '#FF4B4B',
        'Major': '#FFA500',
        'Minor': '#FFD700',
        'Low': '#90EE90'
    }
    
    fig_severity = px.bar(
        severity_counts,
        x='Severity',
        y='Count',
        color='Severity',
        color_discrete_map=color_map,
        text='Count'
    )
    fig_severity.update_traces(textposition='outside')
    fig_severity.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig_severity, use_container_width=True)

# Chart 2: Status Distribution
with col2:
    st.subheader("Defect Status Distribution")
    status_counts = filtered_df['status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']
    
    fig_status = px.pie(
        status_counts,
        values='Count',
        names='Status',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_status.update_traces(textposition='inside', textinfo='percent+label')
    fig_status.update_layout(height=400)
    st.plotly_chart(fig_status, use_container_width=True)

col1, col2 = st.columns(2)

# Chart 3: Time Series
with col1:
    st.subheader("Defects Reported Over Time")
    
    time_series = filtered_df.groupby('reported_month').size().reset_index()
    time_series.columns = ['Month', 'Count']
    
    fig_timeline = px.line(
        time_series,
        x='Month',
        y='Count',
        markers=True,
        line_shape='spline'
    )
    fig_timeline.update_traces(line_color='#1f77b4', marker=dict(size=8))
    fig_timeline.update_layout(
        height=400,
        xaxis_title="Month",
        yaxis_title="Number of Defects",
        hovermode='x unified'
    )
    st.plotly_chart(fig_timeline, use_container_width=True)

# Chart 4: Top Modules
with col2:
    st.subheader("Top Modules with Most Defects")
    
    module_counts = filtered_df['module'].value_counts().head(8).reset_index()
    module_counts.columns = ['Module', 'Count']
    
    fig_modules = px.bar(
        module_counts,
        y='Module',
        x='Count',
        orientation='h',
        text='Count',
        color='Count',
        color_continuous_scale='Reds'
    )
    fig_modules.update_traces(textposition='outside')
    fig_modules.update_layout(
        height=400,
        showlegend=False,
        yaxis={'categoryorder': 'total ascending'}
    )
    st.plotly_chart(fig_modules, use_container_width=True)

st.markdown("---")

# HIGH-RISK ANALYSIS
st.header("⚠️ High-Risk Module Analysis")

high_severity = filtered_df[filtered_df['severity'].isin(['Critical', 'Major'])]
risk_analysis = high_severity.groupby('module').agg({
    'defect_id': 'count',
    'severity': lambda x: (x == 'Critical').sum()
}).reset_index()
risk_analysis.columns = ['Module', 'Total High Severity', 'Critical Count']
risk_analysis = risk_analysis.sort_values('Critical Count', ascending=False).head(10)

if len(risk_analysis) > 0:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_risk = px.bar(
            risk_analysis,
            x='Module',
            y=['Critical Count', 'Total High Severity'],
            barmode='group',
            color_discrete_map={
                'Critical Count': '#FF4B4B', 
                'Total High Severity': '#FFA500'
            },
            labels={'value': 'Count', 'variable': 'Type'}
        )
        fig_risk.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig_risk, use_container_width=True)
    
    with col2:
        st.markdown("**🔴 Critical Modules:**")
        for idx, row in risk_analysis.head(5).iterrows():
            if row['Critical Count'] > 0:
                st.error(f"**{row['Module']}**: {row['Critical Count']} critical")
            else:
                st.warning(f"**{row['Module']}**: {row['Total High Severity']} high severity")
else:
    st.info("No high-severity defects found.")

st.markdown("---")

# DATA TABLE
st.header("📋 Detailed Defect Data")

show_all = st.checkbox("Show all columns", value=False)

if show_all:
    display_df = filtered_df
else:
    display_df = filtered_df[['defect_id', 'module', 'severity', 'status', 
                               'reported_date', 'priority', 'assigned_to']]

display_df_formatted = display_df.copy()
if 'reported_date' in display_df_formatted.columns:
    display_df_formatted['reported_date'] = display_df_formatted['reported_date'].dt.strftime('%Y-%m-%d')
if 'resolved_date' in display_df_formatted.columns:
    display_df_formatted['resolved_date'] = display_df_formatted['resolved_date'].dt.strftime('%Y-%m-%d')

st.dataframe(display_df_formatted, use_container_width=True, height=400)

# Download button
csv = filtered_df.to_csv(index=False)
st.download_button(
    label="⬇️ Download Filtered Data as CSV",
    data=csv,
    file_name=f"filtered_defects_{datetime.now().strftime('%Y%m%d')}.csv",
    mime="text/csv"
)

# Footer
st.markdown("---")
st.markdown(
    f"<div style='text-align: center; color: #888;'>"
    f"QA Defect Analytics Dashboard | Built with Streamlit & Plotly | "
    f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    f"</div>",
    unsafe_allow_html=True
)
