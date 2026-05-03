"""
Quick Demo of Backend Functionality
Shows off the key features of the AI-Assisted Audit Platform backend
"""

import pandas as pd
from backend.data_profiler import DataProfiler
from backend.quality_engine import QualityEngine, RequiredFieldsRule, UniquePrimaryKeyRule
from backend.reconciliation import ReconciliationEngine
from backend.report_generator import ReportGenerator

print("\n" + "="*80)
print("  AI-ASSISTED AUDIT PLATFORM - BACKEND DEMO")
print("="*80 + "\n")

# 1. Load sample data
print("1. LOADING SAMPLE DATA")
print("-" * 80)
source_df = pd.read_csv('data/sample_source.csv')
target_df = pd.read_csv('data/sample_target.csv')
print(f"Source dataset: {len(source_df)} rows, {len(source_df.columns)} columns")
print(f"Target dataset: {len(target_df)} rows, {len(target_df.columns)} columns")
print("\nSource data preview:")
print(source_df.head(3))

# 2. Data Profiling
print("\n\n2. DATA PROFILING")
print("-" * 80)
profiler = DataProfiler(outlier_threshold=3.0)
profile = profiler.profile_dataset(source_df, "Source Dataset")

print(f"Total Rows: {profile['basic_stats']['row_count']}")
print(f"Total Columns: {profile['basic_stats']['column_count']}")
print(f"Missing Values: {profile['missing_values']['total_missing']}")
print(f"Duplicate Rows: {profile['duplicates']['duplicate_count']}")
print(f"Memory Usage: {profile['basic_stats']['memory_usage_mb']:.4f} MB")

print("\nColumn Details:")
for col, details in list(profile['column_details'].items())[:3]:
    print(f"  - {col}: {details['data_type']}, {details['non_null_count']} non-null")

# 3. Quality Checks
print("\n\n3. QUALITY VALIDATION")
print("-" * 80)
engine = QualityEngine()

# Add rules
engine.add_rule(RequiredFieldsRule(
    required_columns=['transaction_id', 'customer_id', 'amount'],
    severity='critical'
))

engine.add_rule(UniquePrimaryKeyRule(
    key_columns=['transaction_id'],
    severity='critical'
))

# Run checks
results = engine.run_quality_checks(source_df, "Source Dataset")

print(f"Total Rules: {results['total_rules']}")
print(f"Rules Passed: {results['rules_passed']}")
print(f"Rules Failed: {results['rules_failed']}")
print(f"Pass Rate: {results['overall_pass_rate']:.1f}%")

print("\nRule Results:")
for rule_result in results['rule_results']:
    status = "PASS" if rule_result['passed'] else "FAIL"
    print(f"  [{status}] {rule_result['rule_name']} ({rule_result['severity']})")

# 4. Reconciliation
print("\n\n4. DATASET RECONCILIATION")
print("-" * 80)
recon_engine = ReconciliationEngine(tolerance=0.01)

recon_results = recon_engine.reconcile_datasets(
    source_df=source_df,
    target_df=target_df,
    key_columns=['transaction_id'],
    source_name="Source System",
    target_name="Target System"
)

print(f"Source Records: {recon_results['record_counts']['source_count']}")
print(f"Target Records: {recon_results['record_counts']['target_count']}")
print(f"Record Difference: {recon_results['record_counts']['difference']}")
print(f"Missing Records: {recon_results['missing_records']['count']}")
print(f"Extra Records: {recon_results['extra_records']['count']}")
print(f"Value Differences: {recon_results['value_differences'].get('total_differences', 0)}")

if recon_results['summary']['overall_match']:
    print("\nResult: PERFECT MATCH!")
else:
    print("\nResult: DIFFERENCES FOUND")

# 5. Report Generation
print("\n\n5. REPORT GENERATION")
print("-" * 80)
generator = ReportGenerator()

# Generate Excel report
print("Generating Excel report...")
excel_result = generator.generate_excel_report(
    output_path='data/demo_audit_report.xlsx',
    profile_results=profile,
    quality_results=results,
    reconciliation_results=recon_results,
    source_df=source_df,
    target_df=target_df
)

if excel_result['success']:
    print(f"SUCCESS: Excel report saved to {excel_result['output_path']}")
    print(f"  - Sheets created: {excel_result['sheets_created']}")
else:
    print(f"ERROR: {excel_result['error']}")

# Generate HTML report
print("\nGenerating HTML report...")
html_result = generator.generate_html_report(
    output_path='data/demo_audit_report.html',
    profile_results=profile,
    quality_results=results,
    reconciliation_results=recon_results
)

if html_result['success']:
    print(f"SUCCESS: HTML report saved to {html_result['output_path']}")
    print(f"  - File size: {html_result['file_size_kb']:.2f} KB")
else:
    print(f"ERROR: {html_result['error']}")

# Summary
print("\n\n" + "="*80)
print("  DEMO COMPLETE!")
print("="*80)
print("\nBackend Features Demonstrated:")
print("  [X] Data Profiling - Comprehensive dataset analysis")
print("  [X] Quality Validation - Rule-based quality checks")
print("  [X] Reconciliation - Dataset comparison and difference detection")
print("  [X] Report Generation - Excel and HTML report creation")
print("\nGenerated Files:")
print("  - data/demo_audit_report.xlsx")
print("  - data/demo_audit_report.html")
print("\nNext Steps:")
print("  1. Open the generated reports to see the results")
print("  2. Review BACKEND_API_DOCUMENTATION.md for integration details")
print("  3. Start building the Streamlit UI using these backend modules")
print("\n")

# Made with Bob
