"""
Reports Component
Generate and export audit reports
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import io

def generate_excel_report(source_df, profiling_results, quality_results, reconciliation_results):
    """Generate comprehensive Excel report"""
    
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Summary sheet
        summary_data = {
            'Report Generated': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            'Source Rows': [len(source_df) if source_df is not None else 0],
            'Source Columns': [len(source_df.columns) if source_df is not None else 0]
        }
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        # Source data preview
        if source_df is not None:
            source_df.head(100).to_excel(writer, sheet_name='Source Data', index=False)
        
        # Profiling results
        if profiling_results:
            prof_data = []
            for col, info in profiling_results.get('column_analysis', {}).items():
                prof_data.append({
                    'Column': col,
                    'Type': info.get('dtype', ''),
                    'Unique Values': info.get('unique_values', 0),
                    'Missing Count': info.get('missing_count', 0),
                    'Missing %': info.get('missing_percent', 0)
                })
            if prof_data:
                pd.DataFrame(prof_data).to_excel(writer, sheet_name='Profiling', index=False)
        
        # Quality results
        if quality_results:
            quality_df = pd.DataFrame(quality_results.get('checks', []))
            if not quality_df.empty:
                quality_df.to_excel(writer, sheet_name='Quality Checks', index=False)
    
    output.seek(0)
    return output

def render_reports_component():
    """Render reports generation interface"""
    
    st.title("📊 Reports")
    st.markdown("Generate comprehensive audit reports and export results.")
    
    # Check if data is available
    has_data = st.session_state.source_data is not None
    has_profiling = st.session_state.profiling_results is not None
    has_quality = st.session_state.quality_results is not None
    has_reconciliation = st.session_state.reconciliation_results is not None
    
    # Report status
    st.subheader("📋 Report Components Status")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Source Data", "✅" if has_data else "❌")
    with col2:
        st.metric("Profiling", "✅" if has_profiling else "❌")
    with col3:
        st.metric("Quality Checks", "✅" if has_quality else "❌")
    with col4:
        st.metric("Reconciliation", "✅" if has_reconciliation else "❌")
    
    if not has_data:
        st.warning("⚠️ No data available. Please upload data first.")
        if st.button("📤 Go to Upload"):
            st.session_state.current_page = 'upload'
            st.rerun()
        return
    
    st.markdown("---")
    
    # Report configuration
    st.subheader("⚙️ Report Configuration")
    
    report_title = st.text_input("Report Title", value="Audit Canvas - Data Quality Report")
    report_author = st.text_input("Author", value=st.session_state.username)
    
    col1, col2 = st.columns(2)
    with col1:
        include_profiling = st.checkbox("Include Profiling Results", value=has_profiling)
        include_quality = st.checkbox("Include Quality Checks", value=has_quality)
    with col2:
        include_reconciliation = st.checkbox("Include Reconciliation", value=has_reconciliation)
        include_raw_data = st.checkbox("Include Raw Data Preview", value=True)
    
    # Report preview
    st.markdown("---")
    st.subheader("👁️ Report Preview")
    
    with st.expander("📄 Report Contents", expanded=True):
        st.markdown(f"""
        ### {report_title}
        **Author:** {report_author}  
        **Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        ---
        
        #### Executive Summary
        - Total Records: {len(st.session_state.source_data):,}
        - Total Columns: {len(st.session_state.source_data.columns)}
        - Report Sections: {sum([include_profiling, include_quality, include_reconciliation, include_raw_data])}
        
        #### Sections Included:
        """)
        
        if include_raw_data:
            st.markdown("- ✅ Raw Data Preview")
        if include_profiling:
            st.markdown("- ✅ Data Profiling Analysis")
        if include_quality:
            st.markdown("- ✅ Quality Check Results")
        if include_reconciliation:
            st.markdown("- ✅ Reconciliation Findings")
    
    # Export options
    st.markdown("---")
    st.subheader("💾 Export Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📊 Excel Report")
        st.markdown("Comprehensive workbook with multiple sheets")
        
        if st.button("📥 Download Excel", use_container_width=True, type="primary"):
            try:
                excel_data = generate_excel_report(
                    st.session_state.source_data,
                    st.session_state.profiling_results if include_profiling else None,
                    st.session_state.quality_results if include_quality else None,
                    st.session_state.reconciliation_results if include_reconciliation else None
                )
                
                st.download_button(
                    label="💾 Save Excel File",
                    data=excel_data,
                    file_name=f"audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
                st.success("✅ Excel report generated!")
            except Exception as e:
                st.error(f"❌ Error generating Excel report: {str(e)}")
    
    with col2:
        st.markdown("### 📄 PDF Report")
        st.markdown("Professional formatted document")
        
        if st.button("📥 Download PDF", use_container_width=True):
            st.info("PDF export functionality coming soon!")
    
    with col3:
        st.markdown("### 📋 CSV Export")
        st.markdown("Raw data in CSV format")
        
        if st.button("📥 Download CSV", use_container_width=True):
            csv = st.session_state.source_data.to_csv(index=False)
            st.download_button(
                label="💾 Save CSV File",
                data=csv,
                file_name=f"audit_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
            st.success("✅ CSV file ready for download!")
    
    # Report history
    st.markdown("---")
    st.subheader("📚 Report History")
    
    st.info("No previous reports. Generate your first report above!")
    
    # Report templates
    st.markdown("---")
    with st.expander("📋 Report Templates"):
        st.markdown("""
        **Standard Audit Report**
        - Executive summary
        - Data profiling results
        - Quality check findings
        - Recommendations
        
        **Reconciliation Report**
        - Source vs Target comparison
        - Missing records analysis
        - Column mapping details
        - Discrepancy summary
        
        **Data Quality Report**
        - Completeness metrics
        - Accuracy assessment
        - Consistency checks
        - Validity analysis
        
        **Custom Report**
        - Select specific sections
        - Add custom commentary
        - Include visualizations
        - Tailored recommendations
        """)

# Made with Bob
