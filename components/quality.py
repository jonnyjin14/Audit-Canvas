"""
Data Quality Checks Component
Automated data quality validation rules
Integrated with backend QualityEngine module
"""

import streamlit as st
import pandas as pd
from datetime import datetime

# Import backend quality engine
from backend.quality_engine import QualityEngine

def run_quality_checks(df):
    """
    Run comprehensive data quality checks using backend QualityEngine
    
    Args:
        df: pandas DataFrame to validate
        
    Returns:
        dict: Quality check results in UI-compatible format
    """
    try:
        # Use backend QualityEngine
        engine = QualityEngine()
        result = engine.run_quality_checks(df)
        
        if not result['success']:
            st.error(f"❌ Quality checks failed: {result.get('error', 'Unknown error')}")
            return None
        
        # Convert backend format to UI format
        backend_results = result
        
        # Transform to match UI expectations
        ui_results = {
            'timestamp': datetime.now(),
            'checks': [],
            'passed': backend_results.get('summary', {}).get('passed', 0),
            'failed': backend_results.get('summary', {}).get('failed', 0),
            'warnings': backend_results.get('summary', {}).get('warnings', 0)
        }
        
        # Convert rule results to UI format
        for rule_result in backend_results.get('results', []):
            status = rule_result.get('status', 'unknown').title()
            
            # Map status to UI format
            if status == 'Pass':
                status = 'Passed'
                severity = 'Low'
            elif status == 'Fail':
                status = 'Failed'
                severity = rule_result.get('severity', 'High')
            else:
                status = 'Warning'
                severity = 'Medium'
            
            ui_results['checks'].append({
                'check': rule_result.get('rule', 'Unknown Rule'),
                'column': rule_result.get('column', 'All'),
                'status': status,
                'message': rule_result.get('message', 'No message'),
                'severity': severity
            })
        
        return ui_results
        
    except Exception as e:
        st.error(f"❌ Error during quality checks: {str(e)}")
        return None

def render_quality_component():
    """Render data quality checks interface"""
    
    st.title("✅ Data Quality Checks")
    st.markdown("Automated validation rules to ensure data integrity and completeness.")
    
    # Check if data is loaded
    if st.session_state.source_data is None:
        st.warning("⚠️ No data loaded. Please upload data first.")
        if st.button("📤 Go to Upload"):
            st.session_state.current_page = 'upload'
            st.rerun()
        return
    
    df = st.session_state.source_data
    
    # Quality check configuration
    st.subheader("⚙️ Configure Quality Checks")
    
    col1, col2 = st.columns(2)
    with col1:
        check_nulls = st.checkbox("Check for null values", value=True)
        check_duplicates = st.checkbox("Check for duplicates", value=True)
        check_outliers = st.checkbox("Check for outliers", value=True)
    
    with col2:
        check_dates = st.checkbox("Validate date formats", value=False)
        check_ranges = st.checkbox("Check value ranges", value=False)
        check_referential = st.checkbox("Referential integrity", value=False)
    
    # Run checks button
    if st.button("🔍 Run Quality Checks", type="primary", use_container_width=True):
        with st.spinner("🔄 Running quality checks..."):
            results = run_quality_checks(df)
            
            # Check if quality checks were successful
            if results is None:
                st.error("❌ Quality checks failed. Please check your data and try again.")
                return
            
            st.session_state.quality_results = results
    
    # Display results if available
    if st.session_state.quality_results:
        results = st.session_state.quality_results
        
        st.markdown("---")
        st.success("✅ Quality checks complete!")
        
        # Summary metrics
        st.subheader("📊 Quality Check Summary")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Checks", len(results['checks']))
        with col2:
            st.metric("✅ Passed", results['passed'], delta=None)
        with col3:
            st.metric("❌ Failed", results['failed'], delta=None)
        with col4:
            st.metric("⚠️ Warnings", results['warnings'], delta=None)
        
        # Detailed results
        st.markdown("---")
        st.subheader("📋 Detailed Results")
        
        # Filter options
        filter_status = st.multiselect(
            "Filter by status",
            ['Passed', 'Failed', 'Warning'],
            default=['Failed', 'Warning']
        )
        
        # Display checks
        for check in results['checks']:
            if check['status'] in filter_status:
                if check['status'] == 'Passed':
                    icon = "✅"
                    color = "green"
                elif check['status'] == 'Failed':
                    icon = "❌"
                    color = "red"
                else:
                    icon = "⚠️"
                    color = "orange"
                
                with st.expander(f"{icon} {check['check']} - {check['column']}"):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**Message:** {check['message']}")
                        st.write(f"**Column:** {check['column']}")
                    with col2:
                        st.write(f"**Status:** {check['status']}")
                        st.write(f"**Severity:** {check['severity']}")
        
        # Failed checks details
        failed_checks = [c for c in results['checks'] if c['status'] == 'Failed']
        if failed_checks:
            st.markdown("---")
            st.subheader("❌ Failed Checks Details")
            
            failed_df = pd.DataFrame(failed_checks)
            st.dataframe(failed_df, use_container_width=True)
        
        # Export results
        st.markdown("---")
        st.subheader("💾 Export Results")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 Export to Excel", use_container_width=True):
                st.info("Excel export functionality coming soon!")
        with col2:
            if st.button("📄 Generate Report", use_container_width=True):
                st.info("Report generation coming soon!")
    
    # Quality rules documentation
    st.markdown("---")
    with st.expander("📚 Quality Check Rules"):
        st.markdown("""
        **Required Fields Check**
        - Validates that critical fields have no null values
        - Severity: High
        
        **Duplicate Detection**
        - Identifies duplicate records in the dataset
        - Severity: Medium
        
        **Outlier Detection**
        - Uses IQR method to detect statistical outliers
        - Severity: Medium
        
        **Date Format Validation**
        - Ensures date fields follow consistent format
        - Severity: High
        
        **Value Range Checks**
        - Validates numeric values are within expected ranges
        - Severity: Medium
        
        **Referential Integrity**
        - Checks foreign key relationships
        - Severity: High
        """)

# Made with Bob
