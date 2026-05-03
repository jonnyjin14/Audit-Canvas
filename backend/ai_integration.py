"""
AI Integration Module
Integrates with IBM Bob for AI-powered features including:
- Anomaly explanation in plain English
- Column mapping suggestions
- Automated audit findings generation
- Documentation assistance
"""

import requests
from typing import Dict, Any, List, Optional
import json
from datetime import datetime


class IBMBobIntegration:
    """
    Integration with IBM Bob AI for audit assistance
    """
    
    def __init__(self, api_key: Optional[str] = None, api_url: Optional[str] = None):
        """
        Initialize IBM Bob integration
        
        Args:
            api_key: IBM Bob API key (if None, will look for environment variable)
            api_url: IBM Bob API endpoint URL
        """
        self.api_key = api_key
        self.api_url = api_url or "https://api.ibm.com/bob/v1"
        self.session = requests.Session()
        
        if self.api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            })
    
    def explain_anomaly(
        self,
        anomaly_data: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Get AI-powered explanation for detected anomalies
        
        Args:
            anomaly_data: Dictionary containing anomaly details
            context: Additional context about the dataset
            
        Returns:
            Dictionary with AI-generated explanation
        """
        prompt = self._build_anomaly_prompt(anomaly_data, context)
        
        try:
            response = self._call_ai_api(prompt, task_type="explain")
            return {
                'success': True,
                'explanation': response.get('text', ''),
                'confidence': response.get('confidence', 0.0),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'explanation': self._generate_fallback_explanation(anomaly_data)
            }
    
    def suggest_column_mapping(
        self,
        source_columns: List[str],
        target_columns: List[str],
        sample_data: Optional[Dict[str, List[Any]]] = None
    ) -> Dict[str, Any]:
        """
        Get AI suggestions for column mapping between datasets
        
        Args:
            source_columns: List of source column names
            target_columns: List of target column names
            sample_data: Optional sample data for better matching
            
        Returns:
            Dictionary with suggested mappings
        """
        prompt = self._build_mapping_prompt(source_columns, target_columns, sample_data)
        
        try:
            response = self._call_ai_api(prompt, task_type="mapping")
            mappings = self._parse_mapping_response(response)
            
            return {
                'success': True,
                'mappings': mappings,
                'confidence_scores': response.get('confidence_scores', {}),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'mappings': self._generate_fallback_mappings(source_columns, target_columns)
            }
    
    def generate_audit_findings(
        self,
        profile_results: Dict[str, Any],
        quality_results: Dict[str, Any],
        reconciliation_results: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate automated audit findings based on analysis results
        
        Args:
            profile_results: Data profiling results
            quality_results: Quality check results
            reconciliation_results: Reconciliation results (optional)
            
        Returns:
            Dictionary with generated audit findings
        """
        prompt = self._build_findings_prompt(
            profile_results,
            quality_results,
            reconciliation_results
        )
        
        try:
            response = self._call_ai_api(prompt, task_type="findings")
            findings = self._parse_findings_response(response)
            
            return {
                'success': True,
                'findings': findings,
                'summary': response.get('summary', ''),
                'recommendations': response.get('recommendations', []),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'findings': self._generate_fallback_findings(
                    profile_results,
                    quality_results,
                    reconciliation_results
                )
            }
    
    def generate_documentation(
        self,
        analysis_results: Dict[str, Any],
        doc_type: str = "summary"
    ) -> Dict[str, Any]:
        """
        Generate documentation for audit analysis
        
        Args:
            analysis_results: Combined analysis results
            doc_type: Type of documentation (summary, detailed, executive)
            
        Returns:
            Dictionary with generated documentation
        """
        prompt = self._build_documentation_prompt(analysis_results, doc_type)
        
        try:
            response = self._call_ai_api(prompt, task_type="documentation")
            
            return {
                'success': True,
                'documentation': response.get('text', ''),
                'format': doc_type,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'documentation': self._generate_fallback_documentation(analysis_results)
            }
    
    def _call_ai_api(self, prompt: str, task_type: str) -> Dict[str, Any]:
        """
        Make API call to IBM Bob
        
        Args:
            prompt: The prompt to send
            task_type: Type of task (explain, mapping, findings, documentation)
            
        Returns:
            API response dictionary
        """
        # This is a placeholder for actual IBM Bob API integration
        # In production, this would make real API calls
        
        if not self.api_key:
            raise ValueError("API key not configured")
        
        endpoint = f"{self.api_url}/{task_type}"
        payload = {
            'prompt': prompt,
            'task_type': task_type,
            'max_tokens': 1000,
            'temperature': 0.7
        }
        
        # Simulated response for development
        # Replace with actual API call: response = self.session.post(endpoint, json=payload)
        return {
            'text': f"AI-generated response for {task_type}",
            'confidence': 0.85,
            'timestamp': datetime.now().isoformat()
        }
    
    def _build_anomaly_prompt(
        self,
        anomaly_data: Dict[str, Any],
        context: Optional[Dict[str, Any]]
    ) -> str:
        """Build prompt for anomaly explanation"""
        prompt = f"""
Analyze the following data anomaly and provide a clear explanation:

Anomaly Details:
{json.dumps(anomaly_data, indent=2)}
"""
        if context:
            prompt += f"\nContext:\n{json.dumps(context, indent=2)}"
        
        prompt += "\n\nProvide a clear, concise explanation of what this anomaly means and potential causes."
        return prompt
    
    def _build_mapping_prompt(
        self,
        source_columns: List[str],
        target_columns: List[str],
        sample_data: Optional[Dict[str, List[Any]]]
    ) -> str:
        """Build prompt for column mapping suggestions"""
        prompt = f"""
Suggest the best column mappings between these datasets:

Source Columns: {', '.join(source_columns)}
Target Columns: {', '.join(target_columns)}
"""
        if sample_data:
            prompt += f"\n\nSample Data:\n{json.dumps(sample_data, indent=2)}"
        
        prompt += "\n\nProvide suggested mappings with confidence scores."
        return prompt
    
    def _build_findings_prompt(
        self,
        profile_results: Dict[str, Any],
        quality_results: Dict[str, Any],
        reconciliation_results: Optional[Dict[str, Any]]
    ) -> str:
        """Build prompt for audit findings generation"""
        prompt = f"""
Generate audit findings based on the following analysis:

Data Profile:
- Total Rows: {profile_results.get('basic_stats', {}).get('row_count', 0)}
- Missing Values: {profile_results.get('missing_values', {}).get('total_missing', 0)}
- Duplicates: {profile_results.get('duplicates', {}).get('duplicate_count', 0)}

Quality Checks:
- Rules Passed: {quality_results.get('rules_passed', 0)}
- Rules Failed: {quality_results.get('rules_failed', 0)}
"""
        if reconciliation_results:
            prompt += f"""
Reconciliation:
- Missing Records: {reconciliation_results.get('missing_records', {}).get('count', 0)}
- Extra Records: {reconciliation_results.get('extra_records', {}).get('count', 0)}
- Value Differences: {reconciliation_results.get('value_differences', {}).get('total_differences', 0)}
"""
        
        prompt += "\n\nGenerate professional audit findings with severity levels and recommendations."
        return prompt
    
    def _build_documentation_prompt(
        self,
        analysis_results: Dict[str, Any],
        doc_type: str
    ) -> str:
        """Build prompt for documentation generation"""
        return f"""
Generate {doc_type} documentation for the following audit analysis:

{json.dumps(analysis_results, indent=2)}

Format the documentation professionally and include key insights.
"""
    
    def _parse_mapping_response(self, response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse AI response for column mappings"""
        # Placeholder parsing logic
        return []
    
    def _parse_findings_response(self, response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse AI response for audit findings"""
        # Placeholder parsing logic
        return []
    
    def _generate_fallback_explanation(self, anomaly_data: Dict[str, Any]) -> str:
        """Generate basic explanation when AI is unavailable"""
        return f"Anomaly detected in the data. Manual review recommended. Details: {anomaly_data}"
    
    def _generate_fallback_mappings(
        self,
        source_columns: List[str],
        target_columns: List[str]
    ) -> List[Dict[str, Any]]:
        """Generate basic column mappings when AI is unavailable"""
        mappings = []
        
        # Simple exact match
        for source_col in source_columns:
            if source_col in target_columns:
                mappings.append({
                    'source': source_col,
                    'target': source_col,
                    'confidence': 1.0,
                    'method': 'exact_match'
                })
        
        return mappings
    
    def _generate_fallback_findings(
        self,
        profile_results: Dict[str, Any],
        quality_results: Dict[str, Any],
        reconciliation_results: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate basic findings when AI is unavailable"""
        findings = []
        
        # Check for missing values
        missing_total = profile_results.get('missing_values', {}).get('total_missing', 0)
        if missing_total > 0:
            findings.append({
                'severity': 'medium',
                'category': 'data_quality',
                'title': 'Missing Values Detected',
                'description': f'Found {missing_total} missing values in the dataset',
                'recommendation': 'Review and address missing data'
            })
        
        # Check for duplicates
        duplicate_count = profile_results.get('duplicates', {}).get('duplicate_count', 0)
        if duplicate_count > 0:
            findings.append({
                'severity': 'high',
                'category': 'data_quality',
                'title': 'Duplicate Records Found',
                'description': f'Found {duplicate_count} duplicate records',
                'recommendation': 'Investigate and remove duplicates'
            })
        
        # Check quality rules
        rules_failed = quality_results.get('rules_failed', 0)
        if rules_failed > 0:
            findings.append({
                'severity': 'high',
                'category': 'compliance',
                'title': 'Quality Rules Failed',
                'description': f'{rules_failed} quality rules failed validation',
                'recommendation': 'Review failed rules and remediate issues'
            })
        
        return findings
    
    def _generate_fallback_documentation(self, analysis_results: Dict[str, Any]) -> str:
        """Generate basic documentation when AI is unavailable"""
        return f"""
Audit Analysis Documentation
Generated: {datetime.now().isoformat()}

This is a basic documentation summary. For enhanced AI-powered documentation,
please configure IBM Bob API credentials.

Analysis Results:
{json.dumps(analysis_results, indent=2)}
"""

# Made with Bob
