"""
Report Generator Module
Generates audit reports in multiple formats:
- Excel workpapers with multiple sheets
- HTML reports with interactive visualizations
- PDF reports (optional)
"""

import pandas as pd
from typing import Dict, Any, List, Optional
from datetime import datetime
import json


class ReportGenerator:
    """
    Generates comprehensive audit reports in multiple formats
    """
    
    def __init__(self):
        """Initialize the report generator"""
        self.report_metadata = {
            'generator': 'AI-Assisted Audit Platform',
            'version': '1.0.0'
        }
    
    def generate_excel_report(
        self,
        output_path: str,
        profile_results: Optional[Dict[str, Any]] = None,
        quality_results: Optional[Dict[str, Any]] = None,
        reconciliation_results: Optional[Dict[str, Any]] = None,
        source_df: Optional[pd.DataFrame] = None,
        target_df: Optional[pd.DataFrame] = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive Excel workpaper
        
        Args:
            output_path: Path to save the Excel file
            profile_results: Data profiling results
            quality_results: Quality check results
            reconciliation_results: Reconciliation results
            source_df: Source dataset
            target_df: Target dataset
            
        Returns:
            Dictionary with generation status and details
        """
        try:
            with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
                workbook = writer.book
                
                # Define formats
                header_format = workbook.add_format({
                    'bold': True,
                    'bg_color': '#4472C4',
                    'font_color': 'white',
                    'border': 1
                })
                
                # Summary sheet
                self._create_summary_sheet(
                    writer,
                    profile_results,
                    quality_results,
                    reconciliation_results,
                    header_format
                )
                
                # Profile results sheet
                if profile_results:
                    self._create_profile_sheet(writer, profile_results, header_format)
                
                # Quality results sheet
                if quality_results:
                    self._create_quality_sheet(writer, quality_results, header_format)
                
                # Reconciliation results sheet
                if reconciliation_results:
                    self._create_reconciliation_sheet(writer, reconciliation_results, header_format)
                
                # Source data sheet
                if source_df is not None:
                    source_df.to_excel(writer, sheet_name='Source Data', index=False)
                    self._format_data_sheet(writer, 'Source Data', header_format)
                
                # Target data sheet
                if target_df is not None:
                    target_df.to_excel(writer, sheet_name='Target Data', index=False)
                    self._format_data_sheet(writer, 'Target Data', header_format)
            
            return {
                'success': True,
                'output_path': output_path,
                'timestamp': datetime.now().isoformat(),
                'sheets_created': self._count_sheets(
                    profile_results,
                    quality_results,
                    reconciliation_results,
                    source_df,
                    target_df
                )
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def generate_html_report(
        self,
        output_path: str,
        profile_results: Optional[Dict[str, Any]] = None,
        quality_results: Optional[Dict[str, Any]] = None,
        reconciliation_results: Optional[Dict[str, Any]] = None,
        include_charts: bool = True
    ) -> Dict[str, Any]:
        """
        Generate interactive HTML report
        
        Args:
            output_path: Path to save the HTML file
            profile_results: Data profiling results
            quality_results: Quality check results
            reconciliation_results: Reconciliation results
            include_charts: Whether to include interactive charts
            
        Returns:
            Dictionary with generation status and details
        """
        try:
            html_content = self._build_html_report(
                profile_results,
                quality_results,
                reconciliation_results,
                include_charts
            )
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return {
                'success': True,
                'output_path': output_path,
                'timestamp': datetime.now().isoformat(),
                'file_size_kb': len(html_content) / 1024
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _create_summary_sheet(
        self,
        writer: pd.ExcelWriter,
        profile_results: Optional[Dict[str, Any]],
        quality_results: Optional[Dict[str, Any]],
        reconciliation_results: Optional[Dict[str, Any]],
        header_format: Any
    ) -> None:
        """Create executive summary sheet"""
        summary_data = []
        
        # Report metadata
        summary_data.append(['Audit Report Summary', ''])
        summary_data.append(['Generated', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
        summary_data.append(['', ''])
        
        # Profile summary
        if profile_results:
            summary_data.append(['Data Profile', ''])
            summary_data.append(['Total Rows', profile_results.get('basic_stats', {}).get('row_count', 0)])
            summary_data.append(['Total Columns', profile_results.get('basic_stats', {}).get('column_count', 0)])
            summary_data.append(['Missing Values', profile_results.get('missing_values', {}).get('total_missing', 0)])
            summary_data.append(['Duplicate Rows', profile_results.get('duplicates', {}).get('duplicate_count', 0)])
            summary_data.append(['', ''])
        
        # Quality summary
        if quality_results:
            summary_data.append(['Quality Checks', ''])
            summary_data.append(['Total Rules', quality_results.get('total_rules', 0)])
            summary_data.append(['Rules Passed', quality_results.get('rules_passed', 0)])
            summary_data.append(['Rules Failed', quality_results.get('rules_failed', 0)])
            summary_data.append(['Pass Rate %', quality_results.get('overall_pass_rate', 0)])
            summary_data.append(['', ''])
        
        # Reconciliation summary
        if reconciliation_results:
            summary_data.append(['Reconciliation', ''])
            summary_data.append(['Source Records', reconciliation_results.get('record_counts', {}).get('source_count', 0)])
            summary_data.append(['Target Records', reconciliation_results.get('record_counts', {}).get('target_count', 0)])
            summary_data.append(['Missing Records', reconciliation_results.get('missing_records', {}).get('count', 0)])
            summary_data.append(['Extra Records', reconciliation_results.get('extra_records', {}).get('count', 0)])
            summary_data.append(['Value Differences', reconciliation_results.get('value_differences', {}).get('total_differences', 0)])
        
        df_summary = pd.DataFrame(summary_data, columns=['Metric', 'Value'])
        df_summary.to_excel(writer, sheet_name='Summary', index=False, header=False)
    
    def _create_profile_sheet(
        self,
        writer: pd.ExcelWriter,
        profile_results: Dict[str, Any],
        header_format: Any
    ) -> None:
        """Create data profile sheet"""
        profile_data = []
        
        # Column details
        for col_name, col_details in profile_results.get('column_details', {}).items():
            profile_data.append({
                'Column': col_name,
                'Data Type': col_details.get('data_type', ''),
                'Non-Null Count': col_details.get('non_null_count', 0),
                'Null Count': col_details.get('null_count', 0),
                'Unique Count': col_details.get('unique_count', 0),
                'Unique %': col_details.get('unique_percentage', 0)
            })
        
        if profile_data:
            df_profile = pd.DataFrame(profile_data)
            df_profile.to_excel(writer, sheet_name='Data Profile', index=False)
    
    def _create_quality_sheet(
        self,
        writer: pd.ExcelWriter,
        quality_results: Dict[str, Any],
        header_format: Any
    ) -> None:
        """Create quality check results sheet"""
        quality_data = []
        
        for rule_result in quality_results.get('rule_results', []):
            quality_data.append({
                'Rule Name': rule_result.get('rule_name', ''),
                'Severity': rule_result.get('severity', ''),
                'Status': 'PASSED' if rule_result.get('passed', False) else 'FAILED',
                'Violations': rule_result.get('total_violations', rule_result.get('duplicate_count', 0))
            })
        
        if quality_data:
            df_quality = pd.DataFrame(quality_data)
            df_quality.to_excel(writer, sheet_name='Quality Checks', index=False)
    
    def _create_reconciliation_sheet(
        self,
        writer: pd.ExcelWriter,
        reconciliation_results: Dict[str, Any],
        header_format: Any
    ) -> None:
        """Create reconciliation results sheet"""
        recon_data = []
        
        # Record counts
        recon_data.append({
            'Metric': 'Source Record Count',
            'Value': reconciliation_results.get('record_counts', {}).get('source_count', 0)
        })
        recon_data.append({
            'Metric': 'Target Record Count',
            'Value': reconciliation_results.get('record_counts', {}).get('target_count', 0)
        })
        recon_data.append({
            'Metric': 'Missing Records',
            'Value': reconciliation_results.get('missing_records', {}).get('count', 0)
        })
        recon_data.append({
            'Metric': 'Extra Records',
            'Value': reconciliation_results.get('extra_records', {}).get('count', 0)
        })
        
        if recon_data:
            df_recon = pd.DataFrame(recon_data)
            df_recon.to_excel(writer, sheet_name='Reconciliation', index=False)
    
    def _format_data_sheet(
        self,
        writer: pd.ExcelWriter,
        sheet_name: str,
        header_format: Any
    ) -> None:
        """Apply formatting to data sheets"""
        worksheet = writer.sheets[sheet_name]
        
        # Auto-fit columns
        for i, col in enumerate(worksheet.table.columns):
            worksheet.set_column(i, i, 15)
    
    def _count_sheets(
        self,
        profile_results: Optional[Dict[str, Any]],
        quality_results: Optional[Dict[str, Any]],
        reconciliation_results: Optional[Dict[str, Any]],
        source_df: Optional[pd.DataFrame],
        target_df: Optional[pd.DataFrame]
    ) -> int:
        """Count number of sheets that will be created"""
        count = 1  # Summary sheet always created
        
        if profile_results:
            count += 1
        if quality_results:
            count += 1
        if reconciliation_results:
            count += 1
        if source_df is not None:
            count += 1
        if target_df is not None:
            count += 1
        
        return count
    
    def _build_html_report(
        self,
        profile_results: Optional[Dict[str, Any]],
        quality_results: Optional[Dict[str, Any]],
        reconciliation_results: Optional[Dict[str, Any]],
        include_charts: bool
    ) -> str:
        """Build HTML report content"""
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Audit Report - {datetime.now().strftime('%Y-%m-%d')}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
        }}
        .metric-card {{
            display: inline-block;
            background: #ecf0f1;
            padding: 15px 25px;
            margin: 10px;
            border-radius: 5px;
            min-width: 200px;
        }}
        .metric-label {{
            font-size: 14px;
            color: #7f8c8d;
        }}
        .metric-value {{
            font-size: 28px;
            font-weight: bold;
            color: #2c3e50;
        }}
        .status-pass {{
            color: #27ae60;
        }}
        .status-fail {{
            color: #e74c3c;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #3498db;
            color: white;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            color: #7f8c8d;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>AI-Assisted Audit Report</h1>
        <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <h2>Executive Summary</h2>
        <div class="metrics">
"""
        
        # Add profile metrics
        if profile_results:
            html += f"""
            <div class="metric-card">
                <div class="metric-label">Total Rows</div>
                <div class="metric-value">{profile_results.get('basic_stats', {}).get('row_count', 0):,}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Missing Values</div>
                <div class="metric-value">{profile_results.get('missing_values', {}).get('total_missing', 0):,}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Duplicates</div>
                <div class="metric-value">{profile_results.get('duplicates', {}).get('duplicate_count', 0):,}</div>
            </div>
"""
        
        # Add quality metrics
        if quality_results:
            pass_rate = quality_results.get('overall_pass_rate', 0)
            status_class = 'status-pass' if pass_rate >= 80 else 'status-fail'
            html += f"""
            <div class="metric-card">
                <div class="metric-label">Quality Pass Rate</div>
                <div class="metric-value {status_class}">{pass_rate:.1f}%</div>
            </div>
"""
        
        html += """
        </div>
"""
        
        # Add detailed sections
        if quality_results:
            html += self._build_quality_section_html(quality_results)
        
        if reconciliation_results:
            html += self._build_reconciliation_section_html(reconciliation_results)
        
        html += f"""
        <div class="footer">
            <p>Generated by {self.report_metadata['generator']} v{self.report_metadata['version']}</p>
        </div>
    </div>
</body>
</html>
"""
        
        return html
    
    def _build_quality_section_html(self, quality_results: Dict[str, Any]) -> str:
        """Build HTML section for quality results"""
        html = """
        <h2>Quality Check Results</h2>
        <table>
            <thead>
                <tr>
                    <th>Rule Name</th>
                    <th>Severity</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
"""
        
        for rule_result in quality_results.get('rule_results', []):
            status = 'PASSED' if rule_result.get('passed', False) else 'FAILED'
            status_class = 'status-pass' if rule_result.get('passed', False) else 'status-fail'
            
            html += f"""
                <tr>
                    <td>{rule_result.get('rule_name', '')}</td>
                    <td>{rule_result.get('severity', '').upper()}</td>
                    <td class="{status_class}">{status}</td>
                </tr>
"""
        
        html += """
            </tbody>
        </table>
"""
        return html
    
    def _build_reconciliation_section_html(self, reconciliation_results: Dict[str, Any]) -> str:
        """Build HTML section for reconciliation results"""
        html = f"""
        <h2>Reconciliation Results</h2>
        <table>
            <thead>
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Source Records</td>
                    <td>{reconciliation_results.get('record_counts', {}).get('source_count', 0):,}</td>
                </tr>
                <tr>
                    <td>Target Records</td>
                    <td>{reconciliation_results.get('record_counts', {}).get('target_count', 0):,}</td>
                </tr>
                <tr>
                    <td>Missing Records</td>
                    <td>{reconciliation_results.get('missing_records', {}).get('count', 0):,}</td>
                </tr>
                <tr>
                    <td>Extra Records</td>
                    <td>{reconciliation_results.get('extra_records', {}).get('count', 0):,}</td>
                </tr>
            </tbody>
        </table>
"""
        return html

# Made with Bob
