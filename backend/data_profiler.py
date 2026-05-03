"""
Data Profiler Module
Analyzes datasets to provide comprehensive profiling information including:
- Row and column counts
- Missing values detection
- Duplicate detection
- Data type validation
- Outlier identification
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, Any, List, Optional
from datetime import datetime


class DataProfiler:
    """
    Comprehensive data profiling engine for audit datasets
    """
    
    def __init__(self, outlier_threshold: float = 3.0):
        """
        Initialize the DataProfiler
        
        Args:
            outlier_threshold: Z-score threshold for outlier detection (default: 3.0)
        """
        self.outlier_threshold = outlier_threshold
    
    def profile_dataset(self, df: pd.DataFrame, dataset_name: str = "Dataset") -> Dict[str, Any]:
        """
        Generate comprehensive profile for a dataset
        
        Args:
            df: pandas DataFrame to profile
            dataset_name: Name of the dataset for reporting
            
        Returns:
            Dictionary containing complete profiling results
        """
        profile = {
            'dataset_name': dataset_name,
            'timestamp': datetime.now().isoformat(),
            'basic_stats': self._get_basic_stats(df),
            'missing_values': self._analyze_missing_values(df),
            'duplicates': self._analyze_duplicates(df),
            'data_types': self._analyze_data_types(df),
            'numeric_stats': self._analyze_numeric_columns(df),
            'outliers': self._detect_outliers(df),
            'column_details': self._get_column_details(df)
        }
        
        return profile
    
    def _get_basic_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Get basic dataset statistics"""
        return {
            'row_count': len(df),
            'column_count': len(df.columns),
            'total_cells': df.size,
            'memory_usage_mb': df.memory_usage(deep=True).sum() / (1024 * 1024),
            'columns': list(df.columns)
        }
    
    def _analyze_missing_values(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze missing values in the dataset"""
        missing_counts = df.isnull().sum()
        missing_percentages = (missing_counts / len(df)) * 100
        
        missing_by_column = {}
        for col in df.columns:
            if missing_counts[col] > 0:
                missing_by_column[col] = {
                    'count': int(missing_counts[col]),
                    'percentage': round(missing_percentages[col], 2)
                }
        
        return {
            'total_missing': int(df.isnull().sum().sum()),
            'total_missing_percentage': round((df.isnull().sum().sum() / df.size) * 100, 2),
            'columns_with_missing': len(missing_by_column),
            'missing_by_column': missing_by_column
        }
    
    def _analyze_duplicates(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze duplicate rows in the dataset"""
        duplicate_rows = df.duplicated()
        duplicate_count = duplicate_rows.sum()
        
        return {
            'duplicate_count': int(duplicate_count),
            'duplicate_percentage': round((duplicate_count / len(df)) * 100, 2) if len(df) > 0 else 0,
            'unique_rows': len(df) - duplicate_count
        }
    
    def _analyze_data_types(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze data types in the dataset"""
        type_counts = df.dtypes.value_counts()
        
        types_by_column = {}
        for col in df.columns:
            types_by_column[col] = str(df[col].dtype)
        
        type_summary = {}
        for dtype, count in type_counts.items():
            type_summary[str(dtype)] = int(count)
        
        return {
            'types_by_column': types_by_column,
            'type_summary': type_summary
        }
    
    def _analyze_numeric_columns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze numeric columns with statistical measures"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        numeric_stats = {}
        for col in numeric_cols:
            col_data = df[col].dropna()
            if len(col_data) > 0:
                numeric_stats[col] = {
                    'mean': round(float(col_data.mean()), 4),
                    'median': round(float(col_data.median()), 4),
                    'std': round(float(col_data.std()), 4),
                    'min': round(float(col_data.min()), 4),
                    'max': round(float(col_data.max()), 4),
                    'q25': round(float(col_data.quantile(0.25)), 4),
                    'q75': round(float(col_data.quantile(0.75)), 4)
                }
        
        return {
            'numeric_column_count': len(numeric_cols),
            'numeric_columns': list(numeric_cols),
            'statistics': numeric_stats
        }
    
    def _detect_outliers(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Detect outliers in numeric columns using Z-score method"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        outliers_by_column = {}
        for col in numeric_cols:
            col_data = df[col].dropna()
            if len(col_data) > 0 and col_data.std() > 0:
                z_scores = np.abs(stats.zscore(col_data))
                outlier_indices = np.where(z_scores > self.outlier_threshold)[0]
                
                if len(outlier_indices) > 0:
                    outliers_by_column[col] = {
                        'count': len(outlier_indices),
                        'percentage': round((len(outlier_indices) / len(col_data)) * 100, 2),
                        'indices': outlier_indices.tolist()[:100]  # Limit to first 100
                    }
        
        return {
            'columns_with_outliers': len(outliers_by_column),
            'outliers_by_column': outliers_by_column,
            'threshold_used': self.outlier_threshold
        }
    
    def _get_column_details(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Get detailed information for each column"""
        column_details = {}
        
        for col in df.columns:
            col_data = df[col]
            unique_count = col_data.nunique()
            
            details = {
                'data_type': str(col_data.dtype),
                'non_null_count': int(col_data.count()),
                'null_count': int(col_data.isnull().sum()),
                'unique_count': int(unique_count),
                'unique_percentage': round((unique_count / len(df)) * 100, 2) if len(df) > 0 else 0
            }
            
            # Add sample values (first 5 unique values)
            sample_values = col_data.dropna().unique()[:5].tolist()
            details['sample_values'] = [str(v) for v in sample_values]
            
            column_details[col] = details
        
        return column_details
    
    def compare_profiles(self, profile1: Dict[str, Any], profile2: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compare two dataset profiles
        
        Args:
            profile1: First dataset profile
            profile2: Second dataset profile
            
        Returns:
            Dictionary containing comparison results
        """
        comparison = {
            'dataset1_name': profile1['dataset_name'],
            'dataset2_name': profile2['dataset_name'],
            'row_count_diff': profile2['basic_stats']['row_count'] - profile1['basic_stats']['row_count'],
            'column_count_diff': profile2['basic_stats']['column_count'] - profile1['basic_stats']['column_count'],
            'common_columns': list(set(profile1['basic_stats']['columns']) & set(profile2['basic_stats']['columns'])),
            'unique_to_dataset1': list(set(profile1['basic_stats']['columns']) - set(profile2['basic_stats']['columns'])),
            'unique_to_dataset2': list(set(profile2['basic_stats']['columns']) - set(profile1['basic_stats']['columns']))
        }
        
        return comparison
    
    def generate_summary(self, profile: Dict[str, Any]) -> str:
        """
        Generate a human-readable summary of the profile
        
        Args:
            profile: Dataset profile dictionary
            
        Returns:
            Formatted summary string
        """
        summary = f"""
Dataset Profile Summary: {profile['dataset_name']}
{'=' * 60}

Basic Statistics:
- Total Rows: {profile['basic_stats']['row_count']:,}
- Total Columns: {profile['basic_stats']['column_count']}
- Memory Usage: {profile['basic_stats']['memory_usage_mb']:.2f} MB

Data Quality:
- Missing Values: {profile['missing_values']['total_missing']:,} ({profile['missing_values']['total_missing_percentage']:.2f}%)
- Duplicate Rows: {profile['duplicates']['duplicate_count']:,} ({profile['duplicates']['duplicate_percentage']:.2f}%)
- Columns with Missing Data: {profile['missing_values']['columns_with_missing']}

Data Types:
- Numeric Columns: {profile['numeric_stats']['numeric_column_count']}
- Type Distribution: {profile['data_types']['type_summary']}

Outliers:
- Columns with Outliers: {profile['outliers']['columns_with_outliers']}
- Detection Threshold: {profile['outliers']['threshold_used']} standard deviations

Generated: {profile['timestamp']}
"""
        return summary

# Made with Bob
