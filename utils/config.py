"""
Configuration Utility
Manages application configuration including:
- Environment variables
- API keys
- Default settings
- Configuration validation
"""

import os
from typing import Dict, Any, Optional
import json
from pathlib import Path


class Config:
    """
    Configuration manager for the audit platform
    """
    
    # Default configuration values
    DEFAULTS = {
        'outlier_threshold': 3.0,
        'numeric_tolerance': 0.01,
        'max_sample_size': 10000,
        'report_format': 'excel',
        'date_format': '%Y-%m-%d',
        'datetime_format': '%Y-%m-%d %H:%M:%S',
        'encoding': 'utf-8',
        'decimal_places': 4
    }
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration
        
        Args:
            config_file: Path to configuration file (JSON)
        """
        self.config = self.DEFAULTS.copy()
        
        # Load from config file if provided
        if config_file and Path(config_file).exists():
            self.load_from_file(config_file)
        
        # Override with environment variables
        self.load_from_env()
    
    def load_from_file(self, config_file: str) -> None:
        """
        Load configuration from JSON file
        
        Args:
            config_file: Path to configuration file
        """
        try:
            with open(config_file, 'r') as f:
                file_config = json.load(f)
                self.config.update(file_config)
        except Exception as e:
            print(f"Warning: Could not load config file: {e}")
    
    def load_from_env(self) -> None:
        """Load configuration from environment variables"""
        # IBM Bob API configuration
        if os.getenv('IBM_BOB_API_KEY'):
            self.config['ibm_bob_api_key'] = os.getenv('IBM_BOB_API_KEY')
        
        if os.getenv('IBM_BOB_API_URL'):
            self.config['ibm_bob_api_url'] = os.getenv('IBM_BOB_API_URL')
        
        # Numeric settings
        if os.getenv('OUTLIER_THRESHOLD'):
            try:
                self.config['outlier_threshold'] = float(os.getenv('OUTLIER_THRESHOLD'))
            except ValueError:
                pass
        
        if os.getenv('NUMERIC_TOLERANCE'):
            try:
                self.config['numeric_tolerance'] = float(os.getenv('NUMERIC_TOLERANCE'))
            except ValueError:
                pass
        
        # Report settings
        if os.getenv('REPORT_FORMAT'):
            self.config['report_format'] = os.getenv('REPORT_FORMAT')
        
        if os.getenv('DATE_FORMAT'):
            self.config['date_format'] = os.getenv('DATE_FORMAT')
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self.config[key] = value
    
    def get_all(self) -> Dict[str, Any]:
        """
        Get all configuration values
        
        Returns:
            Dictionary of all configuration
        """
        return self.config.copy()
    
    def save_to_file(self, config_file: str) -> None:
        """
        Save configuration to JSON file
        
        Args:
            config_file: Path to save configuration
        """
        try:
            with open(config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error saving config file: {e}")
    
    def validate(self) -> Dict[str, Any]:
        """
        Validate configuration
        
        Returns:
            Dictionary with validation results
        """
        errors = []
        warnings = []
        
        # Check numeric thresholds
        if self.config.get('outlier_threshold', 0) <= 0:
            errors.append("outlier_threshold must be positive")
        
        if self.config.get('numeric_tolerance', 0) < 0:
            errors.append("numeric_tolerance must be non-negative")
        
        # Check API configuration
        if not self.config.get('ibm_bob_api_key'):
            warnings.append("IBM Bob API key not configured - AI features will be limited")
        
        # Check report format
        valid_formats = ['excel', 'html', 'pdf']
        if self.config.get('report_format') not in valid_formats:
            errors.append(f"report_format must be one of: {', '.join(valid_formats)}")
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
    
    def reset_to_defaults(self) -> None:
        """Reset configuration to default values"""
        self.config = self.DEFAULTS.copy()
    
    def __repr__(self) -> str:
        """String representation of configuration"""
        return f"Config({len(self.config)} settings)"
    
    def __str__(self) -> str:
        """Human-readable string representation"""
        return json.dumps(self.config, indent=2)


class AuditConfig(Config):
    """
    Specialized configuration for audit operations
    """
    
    AUDIT_DEFAULTS = {
        'required_fields_severity': 'critical',
        'duplicate_severity': 'high',
        'missing_value_threshold': 0.05,  # 5% threshold
        'outlier_action': 'flag',  # flag, remove, or ignore
        'reconciliation_tolerance': 0.01,
        'auto_generate_findings': True,
        'include_ai_insights': True
    }
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize audit configuration"""
        super().__init__(config_file)
        self.config.update(self.AUDIT_DEFAULTS)
        
        # Load audit-specific settings from environment
        self.load_audit_env()
    
    def load_audit_env(self) -> None:
        """Load audit-specific environment variables"""
        if os.getenv('MISSING_VALUE_THRESHOLD'):
            try:
                self.config['missing_value_threshold'] = float(os.getenv('MISSING_VALUE_THRESHOLD'))
            except ValueError:
                pass
        
        if os.getenv('AUTO_GENERATE_FINDINGS'):
            self.config['auto_generate_findings'] = os.getenv('AUTO_GENERATE_FINDINGS').lower() == 'true'
        
        if os.getenv('INCLUDE_AI_INSIGHTS'):
            self.config['include_ai_insights'] = os.getenv('INCLUDE_AI_INSIGHTS').lower() == 'true'


class DatabaseConfig(Config):
    """
    Configuration for database connections (future enhancement)
    """
    
    DB_DEFAULTS = {
        'db_type': 'postgresql',
        'db_host': 'localhost',
        'db_port': 5432,
        'db_name': 'audit_db',
        'connection_timeout': 30,
        'pool_size': 5
    }
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize database configuration"""
        super().__init__(config_file)
        self.config.update(self.DB_DEFAULTS)
        
        # Load database settings from environment
        self.load_db_env()
    
    def load_db_env(self) -> None:
        """Load database environment variables"""
        if os.getenv('DB_TYPE'):
            self.config['db_type'] = os.getenv('DB_TYPE')
        
        if os.getenv('DB_HOST'):
            self.config['db_host'] = os.getenv('DB_HOST')
        
        if os.getenv('DB_PORT'):
            try:
                self.config['db_port'] = int(os.getenv('DB_PORT'))
            except ValueError:
                pass
        
        if os.getenv('DB_NAME'):
            self.config['db_name'] = os.getenv('DB_NAME')
        
        if os.getenv('DB_USER'):
            self.config['db_user'] = os.getenv('DB_USER')
        
        if os.getenv('DB_PASSWORD'):
            self.config['db_password'] = os.getenv('DB_PASSWORD')
    
    def get_connection_string(self) -> str:
        """
        Get database connection string
        
        Returns:
            Connection string for database
        """
        db_type = self.config.get('db_type', 'postgresql')
        user = self.config.get('db_user', '')
        password = self.config.get('db_password', '')
        host = self.config.get('db_host', 'localhost')
        port = self.config.get('db_port', 5432)
        db_name = self.config.get('db_name', 'audit_db')
        
        if db_type == 'postgresql':
            return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
        elif db_type == 'mysql':
            return f"mysql://{user}:{password}@{host}:{port}/{db_name}"
        else:
            return ""


# Global configuration instance
_global_config = None


def get_config() -> Config:
    """
    Get global configuration instance
    
    Returns:
        Global Config instance
    """
    global _global_config
    if _global_config is None:
        _global_config = Config()
    return _global_config


def set_config(config: Config) -> None:
    """
    Set global configuration instance
    
    Args:
        config: Config instance to set as global
    """
    global _global_config
    _global_config = config

# Made with Bob
