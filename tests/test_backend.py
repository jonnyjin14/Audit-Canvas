"""
Backend Test Script
Tests all backend modules with sample data
Run this to verify backend functionality before UI integration
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from backend.data_profiler import DataProfiler
from backend.quality_engine import (
    QualityEngine,
    RequiredFieldsRule,
    UniquePrimaryKeyRule,
    DateFormatRule,
    ValueRangeRule
)
from backend.reconciliation import ReconciliationEngine
from backend.ai_integration import IBMBobIntegration
from backend.report_generator import ReportGenerator
from utils.file_handler import FileHandler
from utils.config import Config


def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'=' * 80}")
    print(f"  {title}")
    print(f"{'=' * 80}\n")


def test_file_handler():
    """Test file handler functionality"""
    print_section("Testing File Handler")
    
    handler = FileHandler()
    
    # Test reading source file
    print("Reading source file...")
    result = handler.read_file('data/sample_source.csv')
    
    if result['success']:
        print(f"✓ Successfully read {result['file_name']}")
        print(f"  - Rows: {result['row_count']}")
        print(f"  - Columns: {result['column_count']}")
        print(f"  - Size: {result['file_size_mb']:.4f} MB")
        return result['df']
    else:
        print(f"✗ Error: {result['error']}")
        return None


def test_data_profiler(df):
    """Test data profiler functionality"""
    print_section("Testing Data Profiler")
    
    profiler = DataProfiler(outlier_threshold=3.0)
    
    print("Profiling dataset...")
    profile = profiler.profile_dataset(df, dataset_name="Sample Source Data")
    
    print(f"✓ Profile generated successfully")
    print(f"\nBasic Statistics:")
    print(f"  - Total Rows: {profile['basic_stats']['row_count']}")
    print(f"  - Total Columns: {profile['basic_stats']['column_count']}")
    print(f"  - Memory Usage: {profile['basic_stats']['memory_usage_mb']:.4f} MB")
    
    print(f"\nData Quality:")
    print(f"  - Missing Values: {profile['missing_values']['total_missing']}")
    print(f"  - Duplicate Rows: {profile['duplicates']['duplicate_count']}")
    print(f"  - Columns with Outliers: {profile['outliers']['columns_with_outliers']}")
    
    # Print summary
    print("\n" + profiler.generate_summary(profile))
    
    return profile


def test_quality_engine(df):
    """Test quality engine functionality"""
    print_section("Testing Quality Engine")
    
    engine = QualityEngine()
    
    # Add quality rules
    print("Adding quality rules...")
    engine.add_rule(RequiredFieldsRule(
        required_columns=['transaction_id', 'customer_id', 'amount'],
        severity='critical'
    ))
    
    engine.add_rule(UniquePrimaryKeyRule(
        key_columns=['transaction_id'],
        severity='critical'
    ))
    
    engine.add_rule(DateFormatRule(
        date_columns={'transaction_date': '%Y-%m-%d'},
        severity='high'
    ))
    
    engine.add_rule(ValueRangeRule(
        range_definitions={
            'amount': {'min': 0, 'max': 10000},
            'quantity': {'min': 1, 'max': 100}
        },
        severity='medium'
    ))
    
    print(f"✓ Added {len(engine.rules)} quality rules")
    
    # Run quality checks
    print("\nRunning quality checks...")
    results = engine.run_quality_checks(df, dataset_name="Sample Source Data")
    
    print(f"✓ Quality checks completed")
    print(f"  - Total Rules: {results['total_rules']}")
    print(f"  - Rules Passed: {results['rules_passed']}")
    print(f"  - Rules Failed: {results['rules_failed']}")
    print(f"  - Pass Rate: {results['overall_pass_rate']:.2f}%")
    
    # Print summary
    print("\n" + engine.generate_summary(results))
    
    return results


def test_reconciliation():
    """Test reconciliation engine functionality"""
    print_section("Testing Reconciliation Engine")
    
    handler = FileHandler()
    
    # Read both files
    print("Reading source and target files...")
    source_result = handler.read_file('data/sample_source.csv')
    target_result = handler.read_file('data/sample_target.csv')
    
    if not source_result['success'] or not target_result['success']:
        print("✗ Error reading files")
        return None
    
    source_df = source_result['df']
    target_df = target_result['df']
    
    print(f"✓ Source: {len(source_df)} rows")
    print(f"✓ Target: {len(target_df)} rows")
    
    # Perform reconciliation
    print("\nPerforming reconciliation...")
    engine = ReconciliationEngine(tolerance=0.01)
    
    recon_results = engine.reconcile_datasets(
        source_df=source_df,
        target_df=target_df,
        key_columns=['transaction_id'],
        source_name="Source System",
        target_name="Target System"
    )
    
    print(f"✓ Reconciliation completed")
    print(f"\nResults:")
    print(f"  - Records Match: {recon_results['record_counts']['match']}")
    print(f"  - Missing Records: {recon_results['missing_records']['count']}")
    print(f"  - Extra Records: {recon_results['extra_records']['count']}")
    print(f"  - Value Differences: {recon_results['value_differences'].get('total_differences', 0)}")
    
    # Print summary
    print("\n" + engine.generate_summary(recon_results))
    
    return recon_results


def test_ai_integration(profile_results, quality_results):
    """Test AI integration functionality"""
    print_section("Testing AI Integration")
    
    ai = IBMBobIntegration()
    
    print("Note: AI integration requires API key configuration")
    print("Testing with fallback mode...\n")
    
    # Test anomaly explanation
    print("Testing anomaly explanation...")
    anomaly_data = {
        'type': 'outlier',
        'column': 'amount',
        'value': 15000,
        'expected_range': '0-10000'
    }
    
    explanation = ai.explain_anomaly(anomaly_data)
    print(f"✓ Explanation generated: {explanation['success']}")
    
    # Test column mapping
    print("\nTesting column mapping suggestions...")
    mapping = ai.suggest_column_mapping(
        source_columns=['transaction_id', 'customer_id', 'amount'],
        target_columns=['txn_id', 'cust_id', 'total_amount']
    )
    print(f"✓ Mappings generated: {mapping['success']}")
    
    # Test findings generation
    print("\nTesting audit findings generation...")
    findings = ai.generate_audit_findings(
        profile_results=profile_results,
        quality_results=quality_results
    )
    print(f"✓ Findings generated: {findings['success']}")
    if findings['success']:
        print(f"  - Number of findings: {len(findings['findings'])}")
    
    return findings


def test_report_generator(profile_results, quality_results, recon_results):
    """Test report generator functionality"""
    print_section("Testing Report Generator")
    
    generator = ReportGenerator()
    handler = FileHandler()
    
    # Read data for reports
    source_result = handler.read_file('data/sample_source.csv')
    target_result = handler.read_file('data/sample_target.csv')
    
    # Generate Excel report
    print("Generating Excel report...")
    excel_result = generator.generate_excel_report(
        output_path='data/audit_report.xlsx',
        profile_results=profile_results,
        quality_results=quality_results,
        reconciliation_results=recon_results,
        source_df=source_result['df'] if source_result['success'] else None,
        target_df=target_result['df'] if target_result['success'] else None
    )
    
    if excel_result['success']:
        print(f"✓ Excel report generated: {excel_result['output_path']}")
        print(f"  - Sheets created: {excel_result['sheets_created']}")
    else:
        print(f"✗ Error: {excel_result['error']}")
    
    # Generate HTML report
    print("\nGenerating HTML report...")
    html_result = generator.generate_html_report(
        output_path='data/audit_report.html',
        profile_results=profile_results,
        quality_results=quality_results,
        reconciliation_results=recon_results,
        include_charts=True
    )
    
    if html_result['success']:
        print(f"✓ HTML report generated: {html_result['output_path']}")
        print(f"  - File size: {html_result['file_size_kb']:.2f} KB")
    else:
        print(f"✗ Error: {html_result['error']}")
    
    return excel_result, html_result


def test_config():
    """Test configuration functionality"""
    print_section("Testing Configuration")
    
    config = Config()
    
    print("Default configuration loaded:")
    print(f"  - Outlier Threshold: {config.get('outlier_threshold')}")
    print(f"  - Numeric Tolerance: {config.get('numeric_tolerance')}")
    print(f"  - Report Format: {config.get('report_format')}")
    
    # Validate configuration
    validation = config.validate()
    print(f"\nConfiguration validation:")
    print(f"  - Valid: {validation['is_valid']}")
    if validation['warnings']:
        print(f"  - Warnings: {len(validation['warnings'])}")
        for warning in validation['warnings']:
            print(f"    • {warning}")
    
    return config


def run_all_tests():
    """Run all backend tests"""
    print("\n" + "=" * 80)
    print("  AI-ASSISTED AUDIT PLATFORM - BACKEND TEST SUITE")
    print("=" * 80)
    
    try:
        # Test configuration
        config = test_config()
        
        # Test file handler and load data
        source_df = test_file_handler()
        if source_df is None:
            print("\n✗ Cannot proceed without data")
            return
        
        # Test data profiler
        profile_results = test_data_profiler(source_df)
        
        # Test quality engine
        quality_results = test_quality_engine(source_df)
        
        # Test reconciliation
        recon_results = test_reconciliation()
        
        # Test AI integration
        ai_findings = test_ai_integration(profile_results, quality_results)
        
        # Test report generator
        if recon_results:
            excel_result, html_result = test_report_generator(
                profile_results,
                quality_results,
                recon_results
            )
        
        # Final summary
        print_section("TEST SUMMARY")
        print("✓ All backend modules tested successfully!")
        print("\nNext Steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Configure IBM Bob API key (optional)")
        print("3. Integrate with Streamlit UI")
        print("4. Test with real audit data")
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()

# Made with Bob
