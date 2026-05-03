"""
Data Quality Rule Engine
Validates data against predefined quality rules including:
- Required fields validation
- Unique primary keys
- Date format validation
- Value range checks
- Referential integrity
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
import re


class QualityRule:
    """Base class for quality rules"""
    
    def __init__(self, rule_name: str, description: str, severity: str = "medium"):
        """
        Initialize a quality rule
        
        Args:
            rule_name: Name of the rule
            description: Description of what the rule checks
            severity: Severity level (critical, high, medium, low)
        """
        self.rule_name = rule_name
        self.description = description
        self.severity = severity
    
    def validate(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validate the rule against a dataset
        
        Args:
            df: DataFrame to validate
            
        Returns:
            Dictionary with validation results
        """
        raise NotImplementedError("Subclasses must implement validate method")


class RequiredFieldsRule(QualityRule):
    """Validates that required fields are not null"""
    
    def __init__(self, required_columns: List[str], severity: str = "critical"):
        super().__init__(
            rule_name="Required Fields",
            description="Validates that required fields contain no null values",
            severity=severity
        )
        self.required_columns = required_columns
    
    def validate(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Check for null values in required columns"""
        violations = {}
        missing_columns = []
        
        for col in self.required_columns:
            if col not in df.columns:
                missing_columns.append(col)
            else:
                null_count = df[col].isnull().sum()
                if null_count > 0:
                    violations[col] = {
                        'null_count': int(null_count),
                        'null_percentage': round((null_count / len(df)) * 100, 2),
                        'sample_indices': df[df[col].isnull()].index.tolist()[:10]
                    }
        
        return {
            'rule_name': self.rule_name,
            'severity': self.severity,
            'passed': len(violations) == 0 and len(missing_columns) == 0,
            'violations': violations,
            'missing_columns': missing_columns,
            'total_violations': sum(v['null_count'] for v in violations.values())
        }


class UniquePrimaryKeyRule(QualityRule):
    """Validates that primary key columns contain unique values"""
    
    def __init__(self, key_columns: List[str], severity: str = "critical"):
        super().__init__(
            rule_name="Unique Primary Key",
            description="Validates that primary key columns contain unique values",
            severity=severity
        )
        self.key_columns = key_columns
    
    def validate(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Check for duplicate values in key columns"""
        missing_columns = [col for col in self.key_columns if col not in df.columns]
        
        if missing_columns:
            return {
                'rule_name': self.rule_name,
                'severity': self.severity,
                'passed': False,
                'missing_columns': missing_columns,
                'duplicate_count': 0
            }
        
        # Check for duplicates based on key columns
        duplicates = df[df.duplicated(subset=self.key_columns, keep=False)]
        duplicate_count = len(duplicates)
        
        duplicate_groups = []
        if duplicate_count > 0:
            # Group duplicates and show first 5 groups
            for key_values, group in duplicates.groupby(self.key_columns):
                if len(duplicate_groups) < 5:
                    duplicate_groups.append({
                        'key_values': key_values if isinstance(key_values, tuple) else (key_values,),
                        'count': len(group),
                        'indices': group.index.tolist()
                    })
        
        return {
            'rule_name': self.rule_name,
            'severity': self.severity,
            'passed': duplicate_count == 0,
            'duplicate_count': duplicate_count,
            'duplicate_percentage': round((duplicate_count / len(df)) * 100, 2) if len(df) > 0 else 0,
            'duplicate_groups': duplicate_groups
        }


class DateFormatRule(QualityRule):
    """Validates date format in specified columns"""
    
    def __init__(self, date_columns: Dict[str, str], severity: str = "high"):
        """
        Initialize date format rule
        
        Args:
            date_columns: Dictionary mapping column names to expected date formats
                         e.g., {'transaction_date': '%Y-%m-%d', 'created_at': '%Y-%m-%d %H:%M:%S'}
            severity: Severity level
        """
        super().__init__(
            rule_name="Date Format Validation",
            description="Validates that date columns match expected formats",
            severity=severity
        )
        self.date_columns = date_columns
    
    def validate(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Check date format compliance"""
        violations = {}
        missing_columns = []
        
        for col, date_format in self.date_columns.items():
            if col not in df.columns:
                missing_columns.append(col)
                continue
            
            invalid_dates = []
            col_data = df[col].dropna()
            
            for idx, value in col_data.items():
                try:
                    if isinstance(value, str):
                        datetime.strptime(value, date_format)
                except (ValueError, TypeError):
                    if len(invalid_dates) < 10:  # Limit to first 10 examples
                        invalid_dates.append({
                            'index': int(idx),
                            'value': str(value)
                        })
            
            if invalid_dates:
                violations[col] = {
                    'expected_format': date_format,
                    'invalid_count': len(invalid_dates),
                    'invalid_percentage': round((len(invalid_dates) / len(col_data)) * 100, 2) if len(col_data) > 0 else 0,
                    'examples': invalid_dates
                }
        
        return {
            'rule_name': self.rule_name,
            'severity': self.severity,
            'passed': len(violations) == 0 and len(missing_columns) == 0,
            'violations': violations,
            'missing_columns': missing_columns
        }


class ValueRangeRule(QualityRule):
    """Validates that numeric values fall within expected ranges"""
    
    def __init__(self, range_definitions: Dict[str, Dict[str, float]], severity: str = "medium"):
        """
        Initialize value range rule
        
        Args:
            range_definitions: Dictionary mapping column names to min/max values
                              e.g., {'amount': {'min': 0, 'max': 1000000}, 'quantity': {'min': 1, 'max': 100}}
            severity: Severity level
        """
        super().__init__(
            rule_name="Value Range Validation",
            description="Validates that numeric values fall within expected ranges",
            severity=severity
        )
        self.range_definitions = range_definitions
    
    def validate(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Check value range compliance"""
        violations = {}
        missing_columns = []
        
        for col, ranges in self.range_definitions.items():
            if col not in df.columns:
                missing_columns.append(col)
                continue
            
            col_data = pd.to_numeric(df[col], errors='coerce')
            min_val = ranges.get('min', -np.inf)
            max_val = ranges.get('max', np.inf)
            
            out_of_range = col_data[(col_data < min_val) | (col_data > max_val)]
            
            if len(out_of_range) > 0:
                violations[col] = {
                    'expected_min': min_val,
                    'expected_max': max_val,
                    'violation_count': len(out_of_range),
                    'violation_percentage': round((len(out_of_range) / len(col_data.dropna())) * 100, 2),
                    'actual_min': float(col_data.min()) if not col_data.empty else None,
                    'actual_max': float(col_data.max()) if not col_data.empty else None,
                    'sample_violations': out_of_range.head(10).tolist()
                }
        
        return {
            'rule_name': self.rule_name,
            'severity': self.severity,
            'passed': len(violations) == 0 and len(missing_columns) == 0,
            'violations': violations,
            'missing_columns': missing_columns
        }


class ReferentialIntegrityRule(QualityRule):
    """Validates referential integrity between datasets"""
    
    def __init__(self, foreign_key_column: str, reference_values: List[Any], severity: str = "high"):
        """
        Initialize referential integrity rule
        
        Args:
            foreign_key_column: Column containing foreign key values
            reference_values: List of valid reference values
            severity: Severity level
        """
        super().__init__(
            rule_name="Referential Integrity",
            description="Validates that foreign key values exist in reference data",
            severity=severity
        )
        self.foreign_key_column = foreign_key_column
        self.reference_values = set(reference_values)
    
    def validate(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Check referential integrity"""
        if self.foreign_key_column not in df.columns:
            return {
                'rule_name': self.rule_name,
                'severity': self.severity,
                'passed': False,
                'missing_column': self.foreign_key_column,
                'orphaned_count': 0
            }
        
        col_data = df[self.foreign_key_column].dropna()
        orphaned_values = col_data[~col_data.isin(self.reference_values)]
        
        return {
            'rule_name': self.rule_name,
            'severity': self.severity,
            'passed': len(orphaned_values) == 0,
            'orphaned_count': len(orphaned_values),
            'orphaned_percentage': round((len(orphaned_values) / len(col_data)) * 100, 2) if len(col_data) > 0 else 0,
            'sample_orphaned_values': orphaned_values.unique().tolist()[:10]
        }


class QualityEngine:
    """Main quality engine for running multiple quality rules"""
    
    def __init__(self):
        """Initialize the quality engine"""
        self.rules: List[QualityRule] = []
    
    def add_rule(self, rule: QualityRule) -> None:
        """Add a quality rule to the engine"""
        self.rules.append(rule)
    
    def add_rules(self, rules: List[QualityRule]) -> None:
        """Add multiple quality rules to the engine"""
        self.rules.extend(rules)
    
    def clear_rules(self) -> None:
        """Clear all rules from the engine"""
        self.rules = []
    
    def run_quality_checks(self, df: pd.DataFrame, dataset_name: str = "Dataset") -> Dict[str, Any]:
        """
        Run all quality rules against a dataset
        
        Args:
            df: DataFrame to validate
            dataset_name: Name of the dataset for reporting
            
        Returns:
            Dictionary containing all quality check results
        """
        results = {
            'dataset_name': dataset_name,
            'timestamp': datetime.now().isoformat(),
            'total_rules': len(self.rules),
            'rules_passed': 0,
            'rules_failed': 0,
            'rule_results': []
        }
        
        for rule in self.rules:
            try:
                rule_result = rule.validate(df)
                results['rule_results'].append(rule_result)
                
                if rule_result.get('passed', False):
                    results['rules_passed'] += 1
                else:
                    results['rules_failed'] += 1
            except Exception as e:
                results['rule_results'].append({
                    'rule_name': rule.rule_name,
                    'severity': rule.severity,
                    'passed': False,
                    'error': str(e)
                })
                results['rules_failed'] += 1
        
        results['overall_pass_rate'] = round((results['rules_passed'] / results['total_rules']) * 100, 2) if results['total_rules'] > 0 else 0
        
        return results
    
    def generate_summary(self, results: Dict[str, Any]) -> str:
        """
        Generate a human-readable summary of quality check results
        
        Args:
            results: Quality check results dictionary
            
        Returns:
            Formatted summary string
        """
        summary = f"""
Data Quality Check Summary: {results['dataset_name']}
{'=' * 60}

Overall Results:
- Total Rules: {results['total_rules']}
- Rules Passed: {results['rules_passed']} ✓
- Rules Failed: {results['rules_failed']} ✗
- Pass Rate: {results['overall_pass_rate']:.2f}%

Rule Details:
"""
        
        for rule_result in results['rule_results']:
            status = "✓ PASSED" if rule_result.get('passed', False) else "✗ FAILED"
            summary += f"\n{status} - {rule_result['rule_name']} ({rule_result['severity']})"
            
            if not rule_result.get('passed', False):
                if 'total_violations' in rule_result:
                    summary += f"\n  Violations: {rule_result['total_violations']}"
                elif 'duplicate_count' in rule_result:
                    summary += f"\n  Duplicates: {rule_result['duplicate_count']}"
                elif 'orphaned_count' in rule_result:
                    summary += f"\n  Orphaned Records: {rule_result['orphaned_count']}"
        
        summary += f"\n\nGenerated: {results['timestamp']}\n"
        
        return summary

# Made with Bob
