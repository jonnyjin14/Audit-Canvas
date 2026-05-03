"""
File Handler Utility
Handles file operations for CSV and Excel files including:
- Reading various file formats
- Validating file structure
- Converting between formats
- Error handling
"""

import pandas as pd
from typing import Dict, Any, Optional, List
import os
from pathlib import Path


class FileHandler:
    """
    Utility class for handling file operations
    """
    
    SUPPORTED_EXTENSIONS = ['.csv', '.xlsx', '.xls']
    
    def __init__(self):
        """Initialize the file handler"""
        self.last_error = None
    
    def read_file(
        self,
        file_path: str,
        sheet_name: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Read a file and return DataFrame with metadata
        
        Args:
            file_path: Path to the file
            sheet_name: Sheet name for Excel files (None for first sheet)
            **kwargs: Additional arguments to pass to pandas read functions
            
        Returns:
            Dictionary containing DataFrame and metadata
        """
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                return {
                    'success': False,
                    'error': f'File not found: {file_path}',
                    'df': None
                }
            
            extension = file_path.suffix.lower()
            
            if extension not in self.SUPPORTED_EXTENSIONS:
                return {
                    'success': False,
                    'error': f'Unsupported file type: {extension}',
                    'df': None
                }
            
            # Read based on file type
            if extension == '.csv':
                df = pd.read_csv(file_path, **kwargs)
            elif extension in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path, sheet_name=sheet_name or 0, **kwargs)
            
            return {
                'success': True,
                'df': df,
                'file_name': file_path.name,
                'file_path': str(file_path),
                'file_size_mb': file_path.stat().st_size / (1024 * 1024),
                'extension': extension,
                'row_count': len(df),
                'column_count': len(df.columns)
            }
        
        except Exception as e:
            self.last_error = str(e)
            return {
                'success': False,
                'error': str(e),
                'df': None
            }
    
    def read_excel_sheets(self, file_path: str) -> Dict[str, Any]:
        """
        Read all sheets from an Excel file
        
        Args:
            file_path: Path to the Excel file
            
        Returns:
            Dictionary with sheet names and DataFrames
        """
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                return {
                    'success': False,
                    'error': f'File not found: {file_path}'
                }
            
            # Get all sheet names
            excel_file = pd.ExcelFile(file_path)
            sheet_names = excel_file.sheet_names
            
            # Read all sheets
            sheets = {}
            for sheet_name in sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                sheets[sheet_name] = df
            
            return {
                'success': True,
                'sheets': sheets,
                'sheet_names': sheet_names,
                'sheet_count': len(sheet_names),
                'file_name': file_path.name
            }
        
        except Exception as e:
            self.last_error = str(e)
            return {
                'success': False,
                'error': str(e)
            }
    
    def write_file(
        self,
        df: pd.DataFrame,
        output_path: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Write DataFrame to file
        
        Args:
            df: DataFrame to write
            output_path: Path to save the file
            **kwargs: Additional arguments for pandas write functions
            
        Returns:
            Dictionary with write status
        """
        try:
            output_path = Path(output_path)
            
            # Create directory if it doesn't exist
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            extension = output_path.suffix.lower()
            
            if extension == '.csv':
                df.to_csv(output_path, index=False, **kwargs)
            elif extension in ['.xlsx', '.xls']:
                df.to_excel(output_path, index=False, **kwargs)
            else:
                return {
                    'success': False,
                    'error': f'Unsupported output format: {extension}'
                }
            
            return {
                'success': True,
                'output_path': str(output_path),
                'file_size_mb': output_path.stat().st_size / (1024 * 1024),
                'rows_written': len(df),
                'columns_written': len(df.columns)
            }
        
        except Exception as e:
            self.last_error = str(e)
            return {
                'success': False,
                'error': str(e)
            }
    
    def validate_file_structure(
        self,
        file_path: str,
        required_columns: Optional[List[str]] = None,
        min_rows: int = 0
    ) -> Dict[str, Any]:
        """
        Validate file structure and content
        
        Args:
            file_path: Path to the file
            required_columns: List of required column names
            min_rows: Minimum number of rows required
            
        Returns:
            Dictionary with validation results
        """
        result = self.read_file(file_path)
        
        if not result['success']:
            return result
        
        df = result['df']
        validation_errors = []
        
        # Check required columns
        if required_columns:
            missing_columns = set(required_columns) - set(df.columns)
            if missing_columns:
                validation_errors.append(f"Missing required columns: {', '.join(missing_columns)}")
        
        # Check minimum rows
        if len(df) < min_rows:
            validation_errors.append(f"File has {len(df)} rows, minimum required: {min_rows}")
        
        # Check for empty DataFrame
        if df.empty:
            validation_errors.append("File is empty")
        
        return {
            'success': len(validation_errors) == 0,
            'valid': len(validation_errors) == 0,
            'errors': validation_errors,
            'df': df,
            'file_info': {
                'row_count': len(df),
                'column_count': len(df.columns),
                'columns': list(df.columns)
            }
        }
    
    def convert_file(
        self,
        input_path: str,
        output_path: str,
        sheet_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Convert file from one format to another
        
        Args:
            input_path: Path to input file
            output_path: Path to output file
            sheet_name: Sheet name for Excel input files
            
        Returns:
            Dictionary with conversion status
        """
        # Read input file
        read_result = self.read_file(input_path, sheet_name=sheet_name)
        
        if not read_result['success']:
            return read_result
        
        # Write to output file
        write_result = self.write_file(read_result['df'], output_path)
        
        if write_result['success']:
            write_result['converted_from'] = read_result['extension']
            write_result['converted_to'] = Path(output_path).suffix.lower()
        
        return write_result
    
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """
        Get information about a file without reading all data
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary with file information
        """
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                return {
                    'success': False,
                    'error': f'File not found: {file_path}'
                }
            
            extension = file_path.suffix.lower()
            
            # Get basic file info
            info = {
                'success': True,
                'file_name': file_path.name,
                'file_path': str(file_path),
                'file_size_mb': file_path.stat().st_size / (1024 * 1024),
                'extension': extension,
                'modified_time': file_path.stat().st_mtime
            }
            
            # Get row/column count without loading full data
            if extension == '.csv':
                # Quick row count for CSV
                with open(file_path, 'r', encoding='utf-8') as f:
                    row_count = sum(1 for _ in f) - 1  # Subtract header
                    f.seek(0)
                    header = f.readline().strip().split(',')
                    info['row_count'] = row_count
                    info['column_count'] = len(header)
                    info['columns'] = header
            
            elif extension in ['.xlsx', '.xls']:
                # Get Excel info
                excel_file = pd.ExcelFile(file_path)
                info['sheet_names'] = excel_file.sheet_names
                info['sheet_count'] = len(excel_file.sheet_names)
            
            return info
        
        except Exception as e:
            self.last_error = str(e)
            return {
                'success': False,
                'error': str(e)
            }

# Made with Bob
