"""
Data Upload Component
Handles file uploads and data loading
"""

import streamlit as st
import pandas as pd
from io import BytesIO

def render_upload_component():
    """Render data upload interface"""
    
    st.title("📤 Upload Data")
    st.markdown("Upload your source and target datasets for analysis and reconciliation.")
    
    # Upload tabs
    tab1, tab2 = st.tabs(["📁 Source Data", "📁 Target Data"])
    
    with tab1:
        st.subheader("Source Dataset")
        st.markdown("Upload the primary dataset for analysis.")
        
        source_file = st.file_uploader(
            "Choose a file",
            type=['csv', 'xlsx', 'xls'],
            key="source_upload",
            help="Supported formats: CSV, Excel (.xlsx, .xls)"
        )
        
        if source_file is not None:
            try:
                # Load data based on file type
                if source_file.name.endswith('.csv'):
                    df = pd.read_csv(source_file)
                else:
                    df = pd.read_excel(source_file)
                
                # Store in session state
                st.session_state.source_data = df
                st.session_state.uploaded_files['source'] = source_file.name
                
                # Display success message
                st.success(f"✅ Successfully loaded: {source_file.name}")
                
                # Display preview
                st.subheader("📊 Data Preview")
                st.dataframe(df.head(10), use_container_width=True)
                
                # Display basic info
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Rows", f"{len(df):,}")
                with col2:
                    st.metric("Columns", len(df.columns))
                with col3:
                    st.metric("Size", f"{source_file.size / 1024:.1f} KB")
                
                # Column information
                with st.expander("📋 Column Details"):
                    col_info = pd.DataFrame({
                        'Column': df.columns,
                        'Type': df.dtypes.astype(str),
                        'Non-Null': df.count(),
                        'Null Count': df.isnull().sum()
                    })
                    st.dataframe(col_info, use_container_width=True)
                
            except Exception as e:
                st.error(f"❌ Error loading file: {str(e)}")
    
    with tab2:
        st.subheader("Target Dataset")
        st.markdown("Upload the comparison dataset for reconciliation.")
        
        target_file = st.file_uploader(
            "Choose a file",
            type=['csv', 'xlsx', 'xls'],
            key="target_upload",
            help="Supported formats: CSV, Excel (.xlsx, .xls)"
        )
        
        if target_file is not None:
            try:
                # Load data based on file type
                if target_file.name.endswith('.csv'):
                    df = pd.read_csv(target_file)
                else:
                    df = pd.read_excel(target_file)
                
                # Store in session state
                st.session_state.target_data = df
                st.session_state.uploaded_files['target'] = target_file.name
                
                # Display success message
                st.success(f"✅ Successfully loaded: {target_file.name}")
                
                # Display preview
                st.subheader("📊 Data Preview")
                st.dataframe(df.head(10), use_container_width=True)
                
                # Display basic info
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Rows", f"{len(df):,}")
                with col2:
                    st.metric("Columns", len(df.columns))
                with col3:
                    st.metric("Size", f"{target_file.size / 1024:.1f} KB")
                
                # Column information
                with st.expander("📋 Column Details"):
                    col_info = pd.DataFrame({
                        'Column': df.columns,
                        'Type': df.dtypes.astype(str),
                        'Non-Null': df.count(),
                        'Null Count': df.isnull().sum()
                    })
                    st.dataframe(col_info, use_container_width=True)
                
            except Exception as e:
                st.error(f"❌ Error loading file: {str(e)}")
    
    # Action buttons
    st.markdown("---")
    st.subheader("⚡ Next Steps")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔍 Run Profiling", use_container_width=True, disabled=st.session_state.source_data is None):
            st.session_state.current_page = 'profiling'
            st.rerun()
    
    with col2:
        if st.button("✅ Quality Checks", use_container_width=True, disabled=st.session_state.source_data is None):
            st.session_state.current_page = 'quality'
            st.rerun()
    
    with col3:
        if st.button("🔄 Reconciliation", use_container_width=True, 
                    disabled=(st.session_state.source_data is None or st.session_state.target_data is None)):
            st.session_state.current_page = 'reconciliation'
            st.rerun()
    
    # Upload tips
    st.markdown("---")
    with st.expander("💡 Upload Tips"):
        st.markdown("""
        **Supported File Formats:**
        - CSV (Comma-separated values)
        - Excel (.xlsx, .xls)
        
        **Best Practices:**
        - Ensure first row contains column headers
        - Remove any summary rows or totals
        - Check for consistent data types in columns
        - Remove special characters from column names
        - Ensure date formats are consistent
        
        **File Size Limits:**
        - Maximum file size: 200 MB
        - For larger files, consider splitting or using database connections
        """)

# Made with Bob
