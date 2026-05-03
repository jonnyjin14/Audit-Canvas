"""
Data Profiling Component
Automated data quality profiling and analysis
Integrated with backend DataProfiler module
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Import backend profiler
from backend.data_profiler import DataProfiler

def analyze_data(df):
    """
    Perform comprehensive data profiling using backend DataProfiler
    
    Args:
        df: pandas DataFrame to profile
        
    Returns:
        dict: Profile results in UI-compatible format
    """
    try:
        # Use backend DataProfiler
        profiler = DataProfiler()
        result = profiler.profile_dataset(df)
        
        if not result['success']:
            st.error(f"❌ Profiling failed: {result.get('error', 'Unknown error')}")
            return None
        
        # Convert backend format to UI format
        backend_profile = result['profile']
        
        # Transform to match UI expectations
        profile = {
            'basic_info': {
                'rows': backend_profile['row_count'],
                'columns': backend_profile['column_count'],
                'memory_usage': backend_profile['memory_usage_mb'],
                'duplicates': backend_profile['duplicate_count']
            },
            'column_analysis': {},
            'missing_data': backend_profile.get('missing_values', {}),
            'data_types': backend_profile.get('data_types', {})
        }
        
        # Convert column details to UI format
        for col_name, col_info in backend_profile.get('columns', {}).items():
            profile['column_analysis'][col_name] = {
                'dtype': col_info.get('dtype', 'unknown'),
                'unique_values': col_info.get('unique_count', 0),
                'missing_count': col_info.get('missing_count', 0),
                'missing_percent': col_info.get('missing_percent', 0.0)
            }
            
            # Add numeric statistics if available
            if col_info.get('is_numeric', False):
                stats = col_info.get('statistics', {})
                profile['column_analysis'][col_name].update({
                    'min': stats.get('min', 0),
                    'max': stats.get('max', 0),
                    'mean': stats.get('mean', 0),
                    'median': stats.get('median', 0),
                    'std': stats.get('std', 0)
                })
        
        return profile
        
    except Exception as e:
        st.error(f"❌ Error during profiling: {str(e)}")
        return None

def render_profiling_component():
    """Render data profiling interface"""
    
    st.title("🔍 Data Profiling")
    st.markdown("Automated analysis of data quality, completeness, and characteristics.")
    
    # Check if data is loaded
    if st.session_state.source_data is None:
        st.warning("⚠️ No data loaded. Please upload data first.")
        if st.button("📤 Go to Upload"):
            st.session_state.current_page = 'upload'
            st.rerun()
        return
    
    df = st.session_state.source_data
    
    # Run profiling
    with st.spinner("🔄 Analyzing data..."):
        profile = analyze_data(df)
        
        # Check if profiling was successful
        if profile is None:
            st.error("❌ Profiling failed. Please check your data and try again.")
            return
        
        st.session_state.profiling_results = profile
    
    # Display results
    st.success("✅ Profiling complete!")
    
    # Basic Information
    st.subheader("📊 Dataset Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Rows", f"{profile['basic_info']['rows']:,}")
    with col2:
        st.metric("Total Columns", profile['basic_info']['columns'])
    with col3:
        st.metric("Memory Usage", f"{profile['basic_info']['memory_usage']:.2f} MB")
    with col4:
        st.metric("Duplicate Rows", profile['basic_info']['duplicates'])
    
    # Missing Data Analysis
    st.markdown("---")
    st.subheader("🔍 Missing Data Analysis")
    
    missing_data = []
    for col, info in profile['column_analysis'].items():
        if info['missing_count'] > 0:
            missing_data.append({
                'Column': col,
                'Missing Count': info['missing_count'],
                'Missing %': f"{info['missing_percent']:.2f}%"
            })
    
    if missing_data:
        missing_df = pd.DataFrame(missing_data)
        st.dataframe(missing_df, use_container_width=True)
        
        # Visualization
        fig = px.bar(
            missing_df,
            x='Column',
            y='Missing Count',
            title='Missing Values by Column',
            color='Missing Count',
            color_continuous_scale='Reds'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.success("✅ No missing values detected!")
    
    # Column Details
    st.markdown("---")
    st.subheader("📋 Column Analysis")
    
    col_details = []
    for col, info in profile['column_analysis'].items():
        col_details.append({
            'Column': col,
            'Type': info['dtype'],
            'Unique Values': info['unique_values'],
            'Missing': info['missing_count'],
            'Missing %': f"{info['missing_percent']:.2f}%"
        })
    
    col_df = pd.DataFrame(col_details)
    st.dataframe(col_df, use_container_width=True)
    
    # Numeric Columns Analysis
    st.markdown("---")
    st.subheader("📈 Numeric Columns Statistics")
    
    numeric_cols = [col for col, info in profile['column_analysis'].items() 
                   if 'mean' in info]
    
    if numeric_cols:
        selected_col = st.selectbox("Select column to analyze", numeric_cols)
        
        if selected_col:
            col_info = profile['column_analysis'][selected_col]
            
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("Min", f"{col_info['min']:.2f}")
            with col2:
                st.metric("Max", f"{col_info['max']:.2f}")
            with col3:
                st.metric("Mean", f"{col_info['mean']:.2f}")
            with col4:
                st.metric("Median", f"{col_info['median']:.2f}")
            with col5:
                st.metric("Std Dev", f"{col_info['std']:.2f}")
            
            # Distribution plot
            fig = px.histogram(
                df,
                x=selected_col,
                title=f'Distribution of {selected_col}',
                nbins=30
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Box plot
            fig = px.box(
                df,
                y=selected_col,
                title=f'Box Plot of {selected_col}'
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No numeric columns found in the dataset.")
    
    # Data Quality Score
    st.markdown("---")
    st.subheader("⭐ Data Quality Score")
    
    # Calculate quality score
    total_cells = profile['basic_info']['rows'] * profile['basic_info']['columns']
    missing_cells = sum(info['missing_count'] for info in profile['column_analysis'].values())
    completeness = ((total_cells - missing_cells) / total_cells) * 100 if total_cells > 0 else 0
    
    duplicate_score = 100 - (profile['basic_info']['duplicates'] / profile['basic_info']['rows'] * 100)
    
    overall_score = (completeness + duplicate_score) / 2
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Completeness", f"{completeness:.1f}%")
    with col2:
        st.metric("Uniqueness", f"{duplicate_score:.1f}%")
    with col3:
        st.metric("Overall Quality", f"{overall_score:.1f}%")
    
    # Quality gauge
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=overall_score,
        title={'text': "Data Quality Score"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 75], 'color': "gray"},
                {'range': [75, 100], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    st.plotly_chart(fig, use_container_width=True)
    
    # Export options
    st.markdown("---")
    st.subheader("💾 Export Profiling Report")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 Export to Excel", use_container_width=True):
            st.info("Excel export functionality coming soon!")
    with col2:
        if st.button("📄 Generate PDF Report", use_container_width=True):
            st.info("PDF export functionality coming soon!")

# Made with Bob
