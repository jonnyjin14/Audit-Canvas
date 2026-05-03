# Backend API Documentation for UI Integration

This document provides comprehensive guidance for integrating the backend modules with the Streamlit UI.

---

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Module Reference](#module-reference)
4. [Integration Examples](#integration-examples)
5. [Error Handling](#error-handling)
6. [Best Practices](#best-practices)

---

## Overview

The backend is organized into modular components that can be independently imported and used:

```
backend/
├── data_profiler.py       # Data profiling and analysis
├── quality_engine.py      # Data quality validation
├── reconciliation.py      # Dataset reconciliation
├── ai_integration.py      # IBM Bob AI integration
└── report_generator.py    # Report generation

utils/
├── file_handler.py        # File I/O operations
├── validators.py          # Validation functions
└── config.py              # Configuration management
```

---

## Installation

Before using the backend, install dependencies:

```bash
pip install -r requirements.txt
```

---

## Module Reference

### 1. File Handler (`utils.file_handler`)

**Purpose:** Handle file uploads and data loading

**Basic Usage:**
```python
from utils.file_handler import FileHandler

handler = FileHandler()

# Read a file
result = handler.read_file('path/to/file.csv')
if result['success']:
    df = result['df']
    print(f"Loaded {result['row_count']} rows")
```

**Key Methods:**
- `read_file(file_path, sheet_name=None)` - Read CSV or Excel file
- `read_excel_sheets(file_path)` - Read all sheets from Excel
- `write_file(df, output_path)` - Write DataFrame to file
- `validate_file_structure(file_path, required_columns, min_rows)` - Validate file

**Streamlit Integration Example:**
```python
import streamlit as st
from utils.file_handler import FileHandler

uploaded_file = st.file_uploader("Upload CSV or Excel", type=['csv', 'xlsx'])

if uploaded_file:
    handler = FileHandler()
    
    # Save uploaded file temporarily
    with open("temp_file.csv", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Read the file
    result = handler.read_file("temp_file.csv")
    
    if result['success']:
        st.success(f"Loaded {result['row_count']} rows")
        st.dataframe(result['df'])
    else:
        st.error(f"Error: {result['error']}")
```

---

### 2. Data Profiler (`backend.data_profiler`)

**Purpose:** Generate comprehensive data profiles

**Basic Usage:**
```python
from backend.data_profiler import DataProfiler

profiler = DataProfiler(outlier_threshold=3.0)
profile = profiler.profile_dataset(df, dataset_name="My Dataset")

# Access results
print(f"Rows: {profile['basic_stats']['row_count']}")
print(f"Missing: {profile['missing_values']['total_missing']}")
print(f"Duplicates: {profile['duplicates']['duplicate_count']}")
```

**Profile Structure:**
```python
{
    'dataset_name': str,
    'timestamp': str,
    'basic_stats': {
        'row_count': int,
        'column_count': int,
        'total_cells': int,
        'memory_usage_mb': float,
        'columns': list
    },
    'missing_values': {
        'total_missing': int,
        'total_missing_percentage': float,
        'columns_with_missing': int,
        'missing_by_column': dict
    },
    'duplicates': {
        'duplicate_count': int,
        'duplicate_percentage': float,
        'unique_rows': int
    },
    'data_types': dict,
    'numeric_stats': dict,
    'outliers': dict,
    'column_details': dict
}
```

**Streamlit Integration Example:**
```python
import streamlit as st
from backend.data_profiler import DataProfiler

if st.button("Profile Data"):
    with st.spinner("Profiling dataset..."):
        profiler = DataProfiler()
        profile = profiler.profile_dataset(df, "Uploaded Data")
    
    # Display results
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Rows", f"{profile['basic_stats']['row_count']:,}")
    col2.metric("Missing Values", profile['missing_values']['total_missing'])
    col3.metric("Duplicates", profile['duplicates']['duplicate_count'])
    
    # Show detailed profile
    with st.expander("Detailed Profile"):
        st.text(profiler.generate_summary(profile))
```

---

### 3. Quality Engine (`backend.quality_engine`)

**Purpose:** Validate data against quality rules

**Basic Usage:**
```python
from backend.quality_engine import (
    QualityEngine,
    RequiredFieldsRule,
    UniquePrimaryKeyRule,
    DateFormatRule,
    ValueRangeRule
)

# Create engine and add rules
engine = QualityEngine()

engine.add_rule(RequiredFieldsRule(
    required_columns=['id', 'name', 'amount'],
    severity='critical'
))

engine.add_rule(UniquePrimaryKeyRule(
    key_columns=['id'],
    severity='critical'
))

engine.add_rule(DateFormatRule(
    date_columns={'date': '%Y-%m-%d'},
    severity='high'
))

engine.add_rule(ValueRangeRule(
    range_definitions={'amount': {'min': 0, 'max': 10000}},
    severity='medium'
))

# Run checks
results = engine.run_quality_checks(df, "My Dataset")

# Check results
print(f"Pass Rate: {results['overall_pass_rate']}%")
for rule_result in results['rule_results']:
    status = "✓" if rule_result['passed'] else "✗"
    print(f"{status} {rule_result['rule_name']}")
```

**Streamlit Integration Example:**
```python
import streamlit as st
from backend.quality_engine import QualityEngine, RequiredFieldsRule

st.subheader("Quality Checks")

# Let user configure rules
required_cols = st.multiselect("Required Columns", df.columns.tolist())

if st.button("Run Quality Checks"):
    engine = QualityEngine()
    
    if required_cols:
        engine.add_rule(RequiredFieldsRule(required_cols, 'critical'))
    
    with st.spinner("Running quality checks..."):
        results = engine.run_quality_checks(df, "Dataset")
    
    # Display results
    st.metric("Pass Rate", f"{results['overall_pass_rate']:.1f}%")
    
    for rule_result in results['rule_results']:
        if rule_result['passed']:
            st.success(f"✓ {rule_result['rule_name']}")
        else:
            st.error(f"✗ {rule_result['rule_name']}")
            if 'violations' in rule_result:
                st.json(rule_result['violations'])
```

---

### 4. Reconciliation Engine (`backend.reconciliation`)

**Purpose:** Compare two datasets and identify differences

**Basic Usage:**
```python
from backend.reconciliation import ReconciliationEngine

engine = ReconciliationEngine(tolerance=0.01)

recon_results = engine.reconcile_datasets(
    source_df=source_df,
    target_df=target_df,
    key_columns=['id'],
    source_name="Source System",
    target_name="Target System",
    compare_columns=['amount', 'quantity']  # Optional
)

# Access results
print(f"Missing: {recon_results['missing_records']['count']}")
print(f"Extra: {recon_results['extra_records']['count']}")
print(f"Differences: {recon_results['value_differences']['total_differences']}")
```

**Streamlit Integration Example:**
```python
import streamlit as st
from backend.reconciliation import ReconciliationEngine

col1, col2 = st.columns(2)

with col1:
    source_file = st.file_uploader("Source File", key="source")
with col2:
    target_file = st.file_uploader("Target File", key="target")

if source_file and target_file:
    # Load both files
    source_df = pd.read_csv(source_file)
    target_df = pd.read_csv(target_file)
    
    # Select key columns
    key_cols = st.multiselect("Key Columns", source_df.columns.tolist())
    
    if st.button("Reconcile") and key_cols:
        engine = ReconciliationEngine()
        
        with st.spinner("Reconciling datasets..."):
            results = engine.reconcile_datasets(
                source_df, target_df, key_cols,
                "Source", "Target"
            )
        
        # Display summary
        st.subheader("Reconciliation Results")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Missing Records", results['missing_records']['count'])
        col2.metric("Extra Records", results['extra_records']['count'])
        col3.metric("Value Differences", 
                   results['value_differences'].get('total_differences', 0))
        
        # Show detailed results
        if results['summary']['overall_match']:
            st.success("✓ Perfect Match!")
        else:
            st.warning("✗ Differences Found")
            
        with st.expander("Detailed Results"):
            st.text(engine.generate_summary(results))
```

---

### 5. AI Integration (`backend.ai_integration`)

**Purpose:** Integrate with IBM Bob for AI-powered insights

**Basic Usage:**
```python
from backend.ai_integration import IBMBobIntegration

# Initialize (API key from environment or config)
ai = IBMBobIntegration(api_key="your-api-key")

# Explain anomaly
explanation = ai.explain_anomaly({
    'type': 'outlier',
    'column': 'amount',
    'value': 15000
})

# Suggest column mappings
mappings = ai.suggest_column_mapping(
    source_columns=['txn_id', 'amt'],
    target_columns=['transaction_id', 'amount']
)

# Generate audit findings
findings = ai.generate_audit_findings(
    profile_results=profile,
    quality_results=quality,
    reconciliation_results=recon
)
```

**Streamlit Integration Example:**
```python
import streamlit as st
from backend.ai_integration import IBMBobIntegration

st.subheader("AI Insights")

if st.button("Generate AI Findings"):
    ai = IBMBobIntegration()
    
    with st.spinner("Generating AI insights..."):
        findings = ai.generate_audit_findings(
            profile_results=profile,
            quality_results=quality
        )
    
    if findings['success']:
        st.success("AI findings generated!")
        
        for finding in findings['findings']:
            with st.expander(f"{finding['severity'].upper()}: {finding['title']}"):
                st.write(finding['description'])
                st.info(f"Recommendation: {finding['recommendation']}")
    else:
        st.warning(f"AI unavailable: {findings.get('error', 'Unknown error')}")
        st.info("Using fallback findings...")
```

---

### 6. Report Generator (`backend.report_generator`)

**Purpose:** Generate Excel and HTML reports

**Basic Usage:**
```python
from backend.report_generator import ReportGenerator

generator = ReportGenerator()

# Generate Excel report
excel_result = generator.generate_excel_report(
    output_path='audit_report.xlsx',
    profile_results=profile,
    quality_results=quality,
    reconciliation_results=recon,
    source_df=source_df,
    target_df=target_df
)

# Generate HTML report
html_result = generator.generate_html_report(
    output_path='audit_report.html',
    profile_results=profile,
    quality_results=quality,
    reconciliation_results=recon,
    include_charts=True
)
```

**Streamlit Integration Example:**
```python
import streamlit as st
from backend.report_generator import ReportGenerator

st.subheader("Generate Reports")

report_format = st.selectbox("Format", ["Excel", "HTML", "Both"])

if st.button("Generate Report"):
    generator = ReportGenerator()
    
    with st.spinner("Generating report..."):
        if report_format in ["Excel", "Both"]:
            excel_result = generator.generate_excel_report(
                'audit_report.xlsx',
                profile, quality, recon,
                source_df, target_df
            )
            
            if excel_result['success']:
                with open('audit_report.xlsx', 'rb') as f:
                    st.download_button(
                        "Download Excel Report",
                        f,
                        file_name="audit_report.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
        
        if report_format in ["HTML", "Both"]:
            html_result = generator.generate_html_report(
                'audit_report.html',
                profile, quality, recon
            )
            
            if html_result['success']:
                with open('audit_report.html', 'rb') as f:
                    st.download_button(
                        "Download HTML Report",
                        f,
                        file_name="audit_report.html",
                        mime="text/html"
                    )
```

---

## Complete Streamlit App Example

Here's a minimal complete Streamlit app integrating all backend modules:

```python
import streamlit as st
import pandas as pd
from utils.file_handler import FileHandler
from backend.data_profiler import DataProfiler
from backend.quality_engine import QualityEngine, RequiredFieldsRule
from backend.report_generator import ReportGenerator

st.title("AI-Assisted Audit Platform")

# File upload
uploaded_file = st.file_uploader("Upload Dataset", type=['csv', 'xlsx'])

if uploaded_file:
    # Load data
    handler = FileHandler()
    with open("temp.csv", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    result = handler.read_file("temp.csv")
    
    if result['success']:
        df = result['df']
        st.success(f"Loaded {len(df)} rows")
        
        # Show data
        st.dataframe(df.head())
        
        # Profile data
        if st.button("Profile Data"):
            profiler = DataProfiler()
            profile = profiler.profile_dataset(df, "Dataset")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Rows", profile['basic_stats']['row_count'])
            col2.metric("Missing", profile['missing_values']['total_missing'])
            col3.metric("Duplicates", profile['duplicates']['duplicate_count'])
        
        # Quality checks
        st.subheader("Quality Checks")
        required_cols = st.multiselect("Required Columns", df.columns.tolist())
        
        if st.button("Run Checks") and required_cols:
            engine = QualityEngine()
            engine.add_rule(RequiredFieldsRule(required_cols))
            
            results = engine.run_quality_checks(df)
            st.metric("Pass Rate", f"{results['overall_pass_rate']:.1f}%")
        
        # Generate report
        if st.button("Generate Report"):
            generator = ReportGenerator()
            excel_result = generator.generate_excel_report(
                'report.xlsx',
                profile_results=profile if 'profile' in locals() else None,
                quality_results=results if 'results' in locals() else None,
                source_df=df
            )
            
            if excel_result['success']:
                with open('report.xlsx', 'rb') as f:
                    st.download_button("Download Report", f, "audit_report.xlsx")
```

---

## Error Handling

All backend methods return dictionaries with a `success` field:

```python
result = handler.read_file('file.csv')

if result['success']:
    # Process data
    df = result['df']
else:
    # Handle error
    st.error(f"Error: {result['error']}")
```

---

## Best Practices

1. **Always check `success` field** before accessing results
2. **Use `st.spinner()`** for long-running operations
3. **Cache expensive operations** with `@st.cache_data`
4. **Handle file cleanup** after processing temporary files
5. **Validate user inputs** before passing to backend
6. **Use try-except blocks** for additional error handling
7. **Display progress** for multi-step operations

---

## Configuration

Set up configuration before using backend:

```python
from utils.config import Config

config = Config()
config.set('outlier_threshold', 3.0)
config.set('ibm_bob_api_key', 'your-key')

# Or use environment variables
# IBM_BOB_API_KEY=your-key
```

---

## Testing

Run the test suite to verify backend functionality:

```bash
python tests/test_backend.py
```

---

## Support

For issues or questions:
- Check the inline documentation in each module
- Review the test script for usage examples
- Refer to the design document for architecture details

---

**Last Updated:** 2026-05-03  
**Version:** 1.0.0