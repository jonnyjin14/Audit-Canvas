"""
Validators Utility
Provides validation functions for data quality checks including:
- Date format validation
- Numeric range validation
- String pattern validation
- Custom validation rules
"""

import pandas as pd
import re
from typing import Any, List, Optional, Callable, Dict
from datetime import datetime


class Validators:
    """
    Collection of validation functions for data quality checks
    """
    
    @staticmethod
    def validate_date_format(value: Any, date_format: str) -> bool:
        """
        Validate if a value matches a specific date format
        
        Args:
            value: Value to validate
            date_format: Expected date format (e.g., '%Y-%m-%d')
            
        Returns:
            True if valid, False otherwise
        """
        if pd.isna(value):
            return False
        
        try:
            if isinstance(value, str):
                datetime.strptime(value, date_format)
                return True
            return False
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_numeric_range(
        value: Any,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None
    ) -> bool:
        """
        Validate if a numeric value falls within a range
        
        Args:
            value: Value to validate
            min_value: Minimum allowed value (inclusive)
            max_value: Maximum allowed value (inclusive)
            
        Returns:
            True if valid, False otherwise
        """
        if pd.isna(value):
            return False
        
        try:
            num_value = float(value)
            
            if min_value is not None and num_value < min_value:
                return False
            
            if max_value is not None and num_value > max_value:
                return False
            
            return True
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_pattern(value: Any, pattern: str) -> bool:
        """
        Validate if a value matches a regex pattern
        
        Args:
            value: Value to validate
            pattern: Regex pattern to match
            
        Returns:
            True if valid, False otherwise
        """
        if pd.isna(value):
            return False
        
        try:
            return bool(re.match(pattern, str(value)))
        except re.error:
            return False
    
    @staticmethod
    def validate_email(value: Any) -> bool:
        """
        Validate email format
        
        Args:
            value: Value to validate
            
        Returns:
            True if valid email, False otherwise
        """
        if pd.isna(value):
            return False
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return Validators.validate_pattern(value, email_pattern)
    
    @staticmethod
    def validate_phone(value: Any, country_code: str = 'US') -> bool:
        """
        Validate phone number format
        
        Args:
            value: Value to validate
            country_code: Country code for format (default: US)
            
        Returns:
            True if valid phone number, False otherwise
        """
        if pd.isna(value):
            return False
        
        # US phone number pattern
        if country_code == 'US':
            phone_pattern = r'^\+?1?\d{10}$|^\(\d{3}\)\s?\d{3}-?\d{4}$'
            return Validators.validate_pattern(str(value).replace('-', '').replace(' ', ''), phone_pattern)
        
        return False
    
    @staticmethod
    def validate_not_null(value: Any) -> bool:
        """
        Validate that value is not null
        
        Args:
            value: Value to validate
            
        Returns:
            True if not null, False otherwise
        """
        return not pd.isna(value)
    
    @staticmethod
    def validate_unique(series: pd.Series) -> Dict[str, Any]:
        """
        Validate uniqueness of values in a series
        
        Args:
            series: Pandas Series to validate
            
        Returns:
            Dictionary with validation results
        """
        duplicates = series[series.duplicated(keep=False)]
        
        return {
            'is_unique': len(duplicates) == 0,
            'duplicate_count': len(duplicates),
            'unique_count': series.nunique(),
            'total_count': len(series),
            'duplicate_values': duplicates.unique().tolist()[:10]  # First 10
        }
    
    @staticmethod
    def validate_length(
        value: Any,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None
    ) -> bool:
        """
        Validate string length
        
        Args:
            value: Value to validate
            min_length: Minimum length (inclusive)
            max_length: Maximum length (inclusive)
            
        Returns:
            True if valid, False otherwise
        """
        if pd.isna(value):
            return False
        
        str_value = str(value)
        length = len(str_value)
        
        if min_length is not None and length < min_length:
            return False
        
        if max_length is not None and length > max_length:
            return False
        
        return True
    
    @staticmethod
    def validate_in_list(value: Any, valid_values: List[Any]) -> bool:
        """
        Validate if value is in a list of valid values
        
        Args:
            value: Value to validate
            valid_values: List of valid values
            
        Returns:
            True if valid, False otherwise
        """
        if pd.isna(value):
            return False
        
        return value in valid_values
    
    @staticmethod
    def validate_data_type(value: Any, expected_type: type) -> bool:
        """
        Validate data type
        
        Args:
            value: Value to validate
            expected_type: Expected Python type
            
        Returns:
            True if valid, False otherwise
        """
        if pd.isna(value):
            return False
        
        return isinstance(value, expected_type)
    
    @staticmethod
    def validate_positive(value: Any) -> bool:
        """
        Validate if numeric value is positive
        
        Args:
            value: Value to validate
            
        Returns:
            True if positive, False otherwise
        """
        if pd.isna(value):
            return False
        
        try:
            return float(value) > 0
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_negative(value: Any) -> bool:
        """
        Validate if numeric value is negative
        
        Args:
            value: Value to validate
            
        Returns:
            True if negative, False otherwise
        """
        if pd.isna(value):
            return False
        
        try:
            return float(value) < 0
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_column_exists(df: pd.DataFrame, column_name: str) -> bool:
        """
        Validate if column exists in DataFrame
        
        Args:
            df: DataFrame to check
            column_name: Column name to validate
            
        Returns:
            True if column exists, False otherwise
        """
        return column_name in df.columns
    
    @staticmethod
    def validate_no_duplicates(df: pd.DataFrame, subset: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Validate that DataFrame has no duplicate rows
        
        Args:
            df: DataFrame to validate
            subset: Columns to consider for duplicates (None = all columns)
            
        Returns:
            Dictionary with validation results
        """
        duplicates = df[df.duplicated(subset=subset, keep=False)]
        
        return {
            'is_valid': len(duplicates) == 0,
            'duplicate_count': len(duplicates),
            'total_rows': len(df),
            'duplicate_percentage': round((len(duplicates) / len(df)) * 100, 2) if len(df) > 0 else 0
        }
    
    @staticmethod
    def validate_custom(
        value: Any,
        validation_func: Callable[[Any], bool]
    ) -> bool:
        """
        Validate using a custom function
        
        Args:
            value: Value to validate
            validation_func: Custom validation function
            
        Returns:
            True if valid, False otherwise
        """
        try:
            return validation_func(value)
        except Exception:
            return False
    
    @staticmethod
    def validate_series(
        series: pd.Series,
        validation_func: Callable[[Any], bool]
    ) -> Dict[str, Any]:
        """
        Validate all values in a series using a validation function
        
        Args:
            series: Pandas Series to validate
            validation_func: Validation function to apply
            
        Returns:
            Dictionary with validation results
        """
        valid_mask = series.apply(validation_func)
        invalid_count = (~valid_mask).sum()
        
        return {
            'is_valid': invalid_count == 0,
            'valid_count': valid_mask.sum(),
            'invalid_count': invalid_count,
            'total_count': len(series),
            'valid_percentage': round((valid_mask.sum() / len(series)) * 100, 2) if len(series) > 0 else 0,
            'invalid_indices': series[~valid_mask].index.tolist()[:10]  # First 10
        }


class ValidationRuleBuilder:
    """
    Builder class for creating complex validation rules
    """
    
    def __init__(self):
        """Initialize the validation rule builder"""
        self.rules = []
    
    def add_rule(
        self,
        rule_name: str,
        validation_func: Callable[[Any], bool],
        error_message: str
    ) -> 'ValidationRuleBuilder':
        """
        Add a validation rule
        
        Args:
            rule_name: Name of the rule
            validation_func: Validation function
            error_message: Error message if validation fails
            
        Returns:
            Self for method chaining
        """
        self.rules.append({
            'name': rule_name,
            'func': validation_func,
            'error': error_message
        })
        return self
    
    def validate_value(self, value: Any) -> Dict[str, Any]:
        """
        Validate a value against all rules
        
        Args:
            value: Value to validate
            
        Returns:
            Dictionary with validation results
        """
        results = {
            'is_valid': True,
            'passed_rules': [],
            'failed_rules': []
        }
        
        for rule in self.rules:
            try:
                if rule['func'](value):
                    results['passed_rules'].append(rule['name'])
                else:
                    results['is_valid'] = False
                    results['failed_rules'].append({
                        'name': rule['name'],
                        'error': rule['error']
                    })
            except Exception as e:
                results['is_valid'] = False
                results['failed_rules'].append({
                    'name': rule['name'],
                    'error': f"Validation error: {str(e)}"
                })
        
        return results
    
    def validate_series(self, series: pd.Series) -> Dict[str, Any]:
        """
        Validate a series against all rules
        
        Args:
            series: Pandas Series to validate
            
        Returns:
            Dictionary with validation results
        """
        results = {
            'total_values': len(series),
            'valid_count': 0,
            'invalid_count': 0,
            'rule_results': {}
        }
        
        for rule in self.rules:
            rule_result = Validators.validate_series(series, rule['func'])
            results['rule_results'][rule['name']] = rule_result
        
        # Calculate overall validity
        all_valid = all(r['is_valid'] for r in results['rule_results'].values())
        results['is_valid'] = all_valid
        
        return results

# Made with Bob
