"""
Reconciliation Engine
Compares two datasets to identify differences including:
- Record count comparison
- Missing/extra records detection
- Column mapping validation
- Data type consistency checks
- Value-level differences
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime


class ReconciliationEngine:
    """
    Engine for reconciling two datasets and identifying differences
    """
    
    def __init__(self, tolerance: float = 0.01):
        """
        Initialize the ReconciliationEngine
        
        Args:
            tolerance: Tolerance for numeric comparisons (default: 0.01)
        """
        self.tolerance = tolerance
    
    def reconcile_datasets(
        self,
        source_df: pd.DataFrame,
        target_df: pd.DataFrame,
        key_columns: List[str],
        source_name: str = "Source",
        target_name: str = "Target",
        compare_columns: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Perform comprehensive reconciliation between two datasets
        
        Args:
            source_df: Source dataset
            target_df: Target dataset
            key_columns: Columns to use as unique identifiers
            source_name: Name of source dataset
            target_name: Name of target dataset
            compare_columns: Specific columns to compare (if None, compares all common columns)
            
        Returns:
            Dictionary containing reconciliation results
        """
        reconciliation = {
            'source_name': source_name,
            'target_name': target_name,
            'timestamp': datetime.now().isoformat(),
            'key_columns': key_columns,
            'record_counts': self._compare_record_counts(source_df, target_df),
            'column_comparison': self._compare_columns(source_df, target_df),
            'data_type_comparison': self._compare_data_types(source_df, target_df),
            'missing_records': self._find_missing_records(source_df, target_df, key_columns),
            'extra_records': self._find_extra_records(source_df, target_df, key_columns),
            'value_differences': self._compare_values(
                source_df, target_df, key_columns, compare_columns
            )
        }
        
        # Calculate summary statistics
        reconciliation['summary'] = self._generate_reconciliation_summary(reconciliation)
        
        return reconciliation
    
    def _compare_record_counts(self, source_df: pd.DataFrame, target_df: pd.DataFrame) -> Dict[str, Any]:
        """Compare record counts between datasets"""
        source_count = len(source_df)
        target_count = len(target_df)
        difference = target_count - source_count
        
        return {
            'source_count': source_count,
            'target_count': target_count,
            'difference': difference,
            'difference_percentage': round((abs(difference) / source_count) * 100, 2) if source_count > 0 else 0,
            'match': source_count == target_count
        }
    
    def _compare_columns(self, source_df: pd.DataFrame, target_df: pd.DataFrame) -> Dict[str, Any]:
        """Compare column structures between datasets"""
        source_cols = set(source_df.columns)
        target_cols = set(target_df.columns)
        
        common_cols = source_cols & target_cols
        missing_in_target = source_cols - target_cols
        extra_in_target = target_cols - source_cols
        
        return {
            'source_columns': list(source_cols),
            'target_columns': list(target_cols),
            'common_columns': list(common_cols),
            'missing_in_target': list(missing_in_target),
            'extra_in_target': list(extra_in_target),
            'column_count_match': len(source_cols) == len(target_cols),
            'all_columns_match': len(missing_in_target) == 0 and len(extra_in_target) == 0
        }
    
    def _compare_data_types(self, source_df: pd.DataFrame, target_df: pd.DataFrame) -> Dict[str, Any]:
        """Compare data types for common columns"""
        common_cols = set(source_df.columns) & set(target_df.columns)
        
        type_mismatches = {}
        for col in common_cols:
            source_type = str(source_df[col].dtype)
            target_type = str(target_df[col].dtype)
            
            if source_type != target_type:
                type_mismatches[col] = {
                    'source_type': source_type,
                    'target_type': target_type
                }
        
        return {
            'columns_checked': len(common_cols),
            'type_mismatches': type_mismatches,
            'mismatch_count': len(type_mismatches),
            'all_types_match': len(type_mismatches) == 0
        }
    
    def _find_missing_records(
        self,
        source_df: pd.DataFrame,
        target_df: pd.DataFrame,
        key_columns: List[str]
    ) -> Dict[str, Any]:
        """Find records in source that are missing in target"""
        # Verify key columns exist
        missing_keys_source = [col for col in key_columns if col not in source_df.columns]
        missing_keys_target = [col for col in key_columns if col not in target_df.columns]
        
        if missing_keys_source or missing_keys_target:
            return {
                'error': 'Key columns not found',
                'missing_in_source': missing_keys_source,
                'missing_in_target': missing_keys_target,
                'count': 0
            }
        
        # Create composite keys
        source_keys = source_df[key_columns].apply(lambda x: tuple(x), axis=1)
        target_keys = target_df[key_columns].apply(lambda x: tuple(x), axis=1)
        
        # Find missing keys
        missing_keys = set(source_keys) - set(target_keys)
        
        # Get sample records
        sample_records = []
        if missing_keys:
            missing_mask = source_keys.isin(missing_keys)
            sample_df = source_df[missing_mask].head(10)
            sample_records = sample_df.to_dict('records')
        
        return {
            'count': len(missing_keys),
            'percentage': round((len(missing_keys) / len(source_df)) * 100, 2) if len(source_df) > 0 else 0,
            'sample_records': sample_records
        }
    
    def _find_extra_records(
        self,
        source_df: pd.DataFrame,
        target_df: pd.DataFrame,
        key_columns: List[str]
    ) -> Dict[str, Any]:
        """Find records in target that don't exist in source"""
        # Verify key columns exist
        missing_keys_source = [col for col in key_columns if col not in source_df.columns]
        missing_keys_target = [col for col in key_columns if col not in target_df.columns]
        
        if missing_keys_source or missing_keys_target:
            return {
                'error': 'Key columns not found',
                'missing_in_source': missing_keys_source,
                'missing_in_target': missing_keys_target,
                'count': 0
            }
        
        # Create composite keys
        source_keys = source_df[key_columns].apply(lambda x: tuple(x), axis=1)
        target_keys = target_df[key_columns].apply(lambda x: tuple(x), axis=1)
        
        # Find extra keys
        extra_keys = set(target_keys) - set(source_keys)
        
        # Get sample records
        sample_records = []
        if extra_keys:
            extra_mask = target_keys.isin(extra_keys)
            sample_df = target_df[extra_mask].head(10)
            sample_records = sample_df.to_dict('records')
        
        return {
            'count': len(extra_keys),
            'percentage': round((len(extra_keys) / len(target_df)) * 100, 2) if len(target_df) > 0 else 0,
            'sample_records': sample_records
        }
    
    def _compare_values(
        self,
        source_df: pd.DataFrame,
        target_df: pd.DataFrame,
        key_columns: List[str],
        compare_columns: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Compare values for matching records"""
        # Verify key columns exist
        missing_keys_source = [col for col in key_columns if col not in source_df.columns]
        missing_keys_target = [col for col in key_columns if col not in target_df.columns]
        
        if missing_keys_source or missing_keys_target:
            return {
                'error': 'Key columns not found',
                'differences_found': 0
            }
        
        # Determine columns to compare
        if compare_columns is None:
            common_cols = list(set(source_df.columns) & set(target_df.columns))
            compare_columns = [col for col in common_cols if col not in key_columns]
        
        # Merge datasets on key columns
        merged = source_df.merge(
            target_df,
            on=key_columns,
            how='inner',
            suffixes=('_source', '_target')
        )
        
        differences = []
        column_differences = {}
        
        for col in compare_columns:
            source_col = f"{col}_source" if f"{col}_source" in merged.columns else col
            target_col = f"{col}_target" if f"{col}_target" in merged.columns else col
            
            if source_col not in merged.columns or target_col not in merged.columns:
                continue
            
            # Compare values
            diff_mask = self._values_differ(merged[source_col], merged[target_col])
            diff_count = diff_mask.sum()
            
            if diff_count > 0:
                column_differences[col] = {
                    'difference_count': int(diff_count),
                    'difference_percentage': round((diff_count / len(merged)) * 100, 2) if len(merged) > 0 else 0
                }
                
                # Get sample differences
                diff_records = merged[diff_mask].head(5)
                for _, row in diff_records.iterrows():
                    key_values = {k: row[k] for k in key_columns}
                    differences.append({
                        'key': key_values,
                        'column': col,
                        'source_value': str(row[source_col]),
                        'target_value': str(row[target_col])
                    })
        
        return {
            'records_compared': len(merged),
            'columns_compared': len(compare_columns),
            'columns_with_differences': len(column_differences),
            'total_differences': sum(d['difference_count'] for d in column_differences.values()),
            'column_differences': column_differences,
            'sample_differences': differences[:20]  # Limit to 20 samples
        }
    
    def _values_differ(self, series1: pd.Series, series2: pd.Series) -> pd.Series:
        """
        Compare two series and return mask of differences
        Handles numeric tolerance and null values
        """
        # Handle nulls - both null is considered equal
        both_null = series1.isnull() & series2.isnull()
        
        # For numeric columns, use tolerance
        if pd.api.types.is_numeric_dtype(series1) and pd.api.types.is_numeric_dtype(series2):
            numeric_diff = np.abs(series1 - series2) > self.tolerance
            return numeric_diff & ~both_null
        else:
            # For non-numeric, direct comparison
            return (series1 != series2) & ~both_null
    
    def _generate_reconciliation_summary(self, reconciliation: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary statistics for reconciliation"""
        return {
            'records_match': reconciliation['record_counts']['match'],
            'columns_match': reconciliation['column_comparison']['all_columns_match'],
            'data_types_match': reconciliation['data_type_comparison']['all_types_match'],
            'missing_records_count': reconciliation['missing_records']['count'],
            'extra_records_count': reconciliation['extra_records']['count'],
            'value_differences_count': reconciliation['value_differences'].get('total_differences', 0),
            'overall_match': (
                reconciliation['record_counts']['match'] and
                reconciliation['column_comparison']['all_columns_match'] and
                reconciliation['data_type_comparison']['all_types_match'] and
                reconciliation['missing_records']['count'] == 0 and
                reconciliation['extra_records']['count'] == 0 and
                reconciliation['value_differences'].get('total_differences', 0) == 0
            )
        }
    
    def generate_summary(self, reconciliation: Dict[str, Any]) -> str:
        """
        Generate a human-readable summary of reconciliation results
        
        Args:
            reconciliation: Reconciliation results dictionary
            
        Returns:
            Formatted summary string
        """
        summary = f"""
Reconciliation Summary: {reconciliation['source_name']} vs {reconciliation['target_name']}
{'=' * 80}

Record Counts:
- Source Records: {reconciliation['record_counts']['source_count']:,}
- Target Records: {reconciliation['record_counts']['target_count']:,}
- Difference: {reconciliation['record_counts']['difference']:,} ({reconciliation['record_counts']['difference_percentage']:.2f}%)
- Match: {'✓ YES' if reconciliation['record_counts']['match'] else '✗ NO'}

Column Structure:
- Common Columns: {len(reconciliation['column_comparison']['common_columns'])}
- Missing in Target: {len(reconciliation['column_comparison']['missing_in_target'])}
- Extra in Target: {len(reconciliation['column_comparison']['extra_in_target'])}
- Match: {'✓ YES' if reconciliation['column_comparison']['all_columns_match'] else '✗ NO'}

Data Type Consistency:
- Columns Checked: {reconciliation['data_type_comparison']['columns_checked']}
- Type Mismatches: {reconciliation['data_type_comparison']['mismatch_count']}
- Match: {'✓ YES' if reconciliation['data_type_comparison']['all_types_match'] else '✗ NO'}

Record Differences:
- Missing Records (in source, not in target): {reconciliation['missing_records']['count']:,}
- Extra Records (in target, not in source): {reconciliation['extra_records']['count']:,}

Value Differences:
- Records Compared: {reconciliation['value_differences'].get('records_compared', 0):,}
- Columns with Differences: {reconciliation['value_differences'].get('columns_with_differences', 0)}
- Total Value Differences: {reconciliation['value_differences'].get('total_differences', 0):,}

Overall Result: {'✓ PERFECT MATCH' if reconciliation['summary']['overall_match'] else '✗ DIFFERENCES FOUND'}

Generated: {reconciliation['timestamp']}
"""
        return summary

# Made with Bob
