"""
Reconciliation Component
Compare source and target datasets for differences
Integrated with backend ReconciliationEngine module
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Import backend reconciliation engine
from backend.reconciliation import ReconciliationEngine

def perform_reconciliation(source_df, target_df, key_column=None):
    """
    Perform reconciliation between source and target datasets using backend ReconciliationEngine
    
    Args:
        source_df: Source pandas DataFrame
        target_df: Target pandas DataFrame
        key_column: Column to use as primary key for matching records
        
    Returns:
        dict: Reconciliation results in UI-compatible format
    """
    try:
        # Use backend ReconciliationEngine
        engine = ReconciliationEngine()
        
        # If no key column specified, try to find a suitable one
        if key_column is None:
            common_cols = set(source_df.columns) & set(target_df.columns)
            if common_cols:
                key_column = list(common_cols)[0]  # Use first common column
        
        # Backend expects a list of key columns
        key_columns = [key_column] if key_column else []
        
        if not key_columns:
            st.error("❌ No common columns found for reconciliation")
            return None
        
        result = engine.reconcile_datasets(source_df, target_df, key_columns)
        
        if not result['success']:
            st.error(f"❌ Reconciliation failed: {result.get('error', 'Unknown error')}")
            return None
        
        # Convert backend format to UI format
        backend_results = result
        
        # Transform to match UI expectations
        ui_results = {
            'timestamp': datetime.now(),
            'source_rows': len(source_df),
            'target_rows': len(target_df),
            'row_difference': len(source_df) - len(target_df),
            'source_columns': list(source_df.columns),
            'target_columns': list(target_df.columns),
            'common_columns': backend_results.get('common_columns', []),
            'missing_in_target': backend_results.get('missing_in_target', []),
            'missing_in_source': backend_results.get('extra_in_target', []),
            'column_mapping': {},
            'data_differences': backend_results.get('value_differences', []),
            'key_column': key_column
        }
        
        # Build column mapping from common columns
        for col in ui_results['common_columns']:
            if col in source_df.columns and col in target_df.columns:
                source_dtype = str(source_df[col].dtype)
                target_dtype = str(target_df[col].dtype)
                
                ui_results['column_mapping'][col] = {
                    'source_dtype': source_dtype,
                    'target_dtype': target_dtype,
                    'dtype_match': source_dtype == target_dtype,
                    'source_nulls': source_df[col].isnull().sum(),
                    'target_nulls': target_df[col].isnull().sum()
                }
        
        return ui_results
        
    except Exception as e:
        st.error(f"❌ Error during reconciliation: {str(e)}")
        return None

def render_reconciliation_component():
    """Render reconciliation interface"""
    
    st.title("🔄 Data Reconciliation")
    st.markdown("Compare source and target datasets to identify differences and discrepancies.")
    
    # Check if both datasets are loaded
    if st.session_state.source_data is None or st.session_state.target_data is None:
        st.warning("⚠️ Both source and target datasets are required for reconciliation.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Source Data:** {'✅ Loaded' if st.session_state.source_data is not None else '❌ Not loaded'}")
        with col2:
            st.info(f"**Target Data:** {'✅ Loaded' if st.session_state.target_data is not None else '❌ Not loaded'}")
        
        if st.button("📤 Go to Upload"):
            st.session_state.current_page = 'upload'
            st.rerun()
        return
    
    source_df = st.session_state.source_data
    target_df = st.session_state.target_data
    
    # Reconciliation configuration
    st.subheader("⚙️ Reconciliation Settings")
    
    # Key column selection
    common_columns = list(set(source_df.columns) & set(target_df.columns))
    if common_columns:
        key_column = st.selectbox(
            "Select key column for matching records",
            options=common_columns,
            help="Choose a column that uniquely identifies records in both datasets"
        )
    else:
        st.error("❌ No common columns found between source and target datasets!")
        return
    
    col1, col2 = st.columns(2)
    with col1:
        compare_structure = st.checkbox("Compare structure", value=True)
        compare_counts = st.checkbox("Compare row counts", value=True)
    with col2:
        compare_values = st.checkbox("Compare values", value=True)
        identify_missing = st.checkbox("Identify missing records", value=True)
    
    # Run reconciliation
    if st.button("🔄 Run Reconciliation", type="primary", use_container_width=True):
        with st.spinner("🔄 Performing reconciliation..."):
            results = perform_reconciliation(source_df, target_df, key_column)
            
            # Check if reconciliation was successful
            if results is None:
                st.error("❌ Reconciliation failed. Please check your data and try again.")
                return
            
            st.session_state.reconciliation_results = results
    
    # Display results
    if st.session_state.reconciliation_results:
        results = st.session_state.reconciliation_results
        
        st.markdown("---")
        st.success("✅ Reconciliation complete!")
        
        # Summary metrics
        st.subheader("📊 Reconciliation Summary")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Source Rows", f"{results['source_rows']:,}")
        with col2:
            st.metric("Target Rows", f"{results['target_rows']:,}")
        with col3:
            delta_color = "normal" if results['row_difference'] == 0 else "inverse"
            st.metric("Row Difference", results['row_difference'], delta=results['row_difference'])
        with col4:
            match_percent = (min(results['source_rows'], results['target_rows']) / 
                           max(results['source_rows'], results['target_rows']) * 100) if max(results['source_rows'], results['target_rows']) > 0 else 0
            st.metric("Match %", f"{match_percent:.1f}%")
        
        # Column comparison
        st.markdown("---")
        st.subheader("📋 Column Comparison")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Common Columns", len(results['common_columns']))
        with col2:
            st.metric("Missing in Target", len(results['missing_in_target']))
        with col3:
            st.metric("Missing in Source", len(results['missing_in_source']))
        
        # Common columns details
        if results['common_columns']:
            with st.expander("✅ Common Columns"):
                st.write(results['common_columns'])
        
        # Missing columns
        if results['missing_in_target']:
            with st.expander("❌ Columns Missing in Target", expanded=True):
                st.warning(f"The following columns exist in source but not in target:")
                st.write(results['missing_in_target'])
        
        if results['missing_in_source']:
            with st.expander("❌ Columns Missing in Source", expanded=True):
                st.warning(f"The following columns exist in target but not in source:")
                st.write(results['missing_in_source'])
        
        # Column mapping details
        st.markdown("---")
        st.subheader("🗺️ Column Mapping Analysis")
        
        if results['column_mapping']:
            mapping_data = []
            for col, info in results['column_mapping'].items():
                mapping_data.append({
                    'Column': col,
                    'Source Type': info['source_dtype'],
                    'Target Type': info['target_dtype'],
                    'Type Match': '✅' if info['dtype_match'] else '❌',
                    'Source Nulls': info['source_nulls'],
                    'Target Nulls': info['target_nulls']
                })
            
            mapping_df = pd.DataFrame(mapping_data)
            st.dataframe(mapping_df, use_container_width=True)
            
            # Type mismatch warning
            type_mismatches = [row for row in mapping_data if row['Type Match'] == '❌']
            if type_mismatches:
                st.warning(f"⚠️ {len(type_mismatches)} column(s) have data type mismatches!")
        
        # Visualization
        st.markdown("---")
        st.subheader("📊 Visual Comparison")
        
        # Row count comparison
        comparison_data = pd.DataFrame({
            'Dataset': ['Source', 'Target'],
            'Row Count': [results['source_rows'], results['target_rows']]
        })
        
        fig = px.bar(
            comparison_data,
            x='Dataset',
            y='Row Count',
            title='Row Count Comparison',
            color='Dataset',
            color_discrete_map={'Source': '#1f77b4', 'Target': '#ff7f0e'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Column comparison pie chart
        col_comparison = pd.DataFrame({
            'Category': ['Common', 'Only in Source', 'Only in Target'],
            'Count': [
                len(results['common_columns']),
                len(results['missing_in_target']),
                len(results['missing_in_source'])
            ]
        })
        
        fig = px.pie(
            col_comparison,
            values='Count',
            names='Category',
            title='Column Distribution'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # AI Insights
        st.markdown("---")
        st.subheader("🤖 AI-Powered Insights")
        
        insights = []
        
        if results['row_difference'] != 0:
            insights.append(f"• Row count mismatch detected: {abs(results['row_difference'])} rows difference")
        
        if results['missing_in_target']:
            insights.append(f"• {len(results['missing_in_target'])} column(s) missing in target dataset")
        
        if results['missing_in_source']:
            insights.append(f"• {len(results['missing_in_source'])} column(s) missing in source dataset")
        
        type_mismatches = sum(1 for info in results['column_mapping'].values() if not info['dtype_match'])
        if type_mismatches > 0:
            insights.append(f"• {type_mismatches} column(s) have data type inconsistencies")
        
        if insights:
            for insight in insights:
                st.warning(insight)
        else:
            st.success("✅ No major discrepancies detected! Datasets are well-aligned.")
        
        # Export options
        st.markdown("---")
        st.subheader("💾 Export Reconciliation Report")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 Export to Excel", use_container_width=True):
                st.info("Excel export functionality coming soon!")
        with col2:
            if st.button("📄 Generate PDF Report", use_container_width=True):
                st.info("PDF export functionality coming soon!")

# Made with Bob
