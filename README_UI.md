# Audit Canvas - UI Documentation

## 🎨 User Interface Overview

The Audit Canvas platform features a modern, intuitive web interface built with Streamlit, designed for efficient audit data analysis and reconciliation.

---

## 📱 Application Structure

### Main Components

1. **Login Page** (`utils/auth.py`)
   - Secure authentication system
   - Demo credentials for testing
   - Session management

2. **Dashboard** (`pages/dashboard.py`)
   - Central navigation hub
   - Quick metrics overview
   - Recent activity tracking

3. **Data Upload** (`components/upload.py`)
   - Support for CSV and Excel files
   - Source and target dataset management
   - Data preview and validation

4. **Data Profiling** (`components/profiling.py`)
   - Automated data quality analysis
   - Statistical summaries
   - Missing data visualization
   - Data quality scoring

5. **Quality Checks** (`components/quality.py`)
   - Configurable validation rules
   - Null value detection
   - Duplicate identification
   - Outlier analysis

6. **Reconciliation** (`components/reconciliation.py`)
   - Source vs target comparison
   - Column mapping analysis
   - Row count reconciliation
   - AI-powered insights

7. **Reports** (`components/reports.py`)
   - Excel report generation
   - CSV export
   - Customizable report templates
   - Download functionality

---

## 🔐 Authentication

### Demo Credentials

The application includes three demo accounts:

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Administrator |
| auditor | audit123 | Auditor |
| demo | demo123 | Demo User |

### Login Features
- Secure password hashing (SHA256)
- Session state management
- Auto-logout functionality
- User role display

---

## 🏠 Dashboard Features

### Navigation Menu
- 🏠 Dashboard - Home page with overview
- 📤 Upload Data - File upload interface
- 🔍 Data Profiling - Automated analysis
- ✅ Quality Checks - Validation rules
- 🔄 Reconciliation - Data comparison
- 📊 Reports - Export and reporting
- ⚙️ Settings - User preferences

### Quick Stats
- Files uploaded count
- Active tasks tracking
- Real-time metrics

### Quick Actions
- One-click access to key features
- Context-aware button states
- Streamlined workflow

---

## 📤 Data Upload

### Supported Formats
- CSV (Comma-separated values)
- Excel (.xlsx, .xls)

### Features
- Drag-and-drop file upload
- Automatic data type detection
- Data preview (first 10 rows)
- Column information display
- File size and row count metrics

### Best Practices
- First row should contain headers
- Remove summary rows
- Consistent data types per column
- Clean column names
- Standardized date formats

---

## 🔍 Data Profiling

### Analysis Components

**Basic Information**
- Total rows and columns
- Memory usage
- Duplicate detection

**Missing Data Analysis**
- Missing value counts per column
- Missing percentage calculation
- Visual bar charts

**Column Analysis**
- Data type identification
- Unique value counts
- Null value statistics

**Numeric Statistics**
- Min, max, mean, median
- Standard deviation
- Distribution histograms
- Box plots for outliers

**Data Quality Score**
- Completeness percentage
- Uniqueness score
- Overall quality gauge (0-100)

---

## ✅ Quality Checks

### Validation Rules

1. **Required Fields**
   - Checks for null values
   - Severity: High

2. **Duplicate Detection**
   - Identifies duplicate rows
   - Severity: Medium

3. **Outlier Detection**
   - IQR method for numeric columns
   - Severity: Medium

4. **Date Validation** (Configurable)
   - Format consistency
   - Severity: High

5. **Range Checks** (Configurable)
   - Value boundaries
   - Severity: Medium

6. **Referential Integrity** (Configurable)
   - Foreign key validation
   - Severity: High

### Results Display
- Summary metrics (passed/failed/warnings)
- Detailed check results
- Filterable by status
- Expandable details per check

---

## 🔄 Reconciliation

### Comparison Features

**Row Count Analysis**
- Source vs target row counts
- Difference calculation
- Match percentage

**Column Comparison**
- Common columns identification
- Missing columns detection
- Data type consistency checks

**Visual Analytics**
- Bar charts for row counts
- Pie charts for column distribution
- Interactive Plotly visualizations

**AI Insights**
- Automated discrepancy detection
- Plain English explanations
- Actionable recommendations

---

## 📊 Reports

### Report Types

1. **Excel Report**
   - Multiple sheets (Summary, Data, Profiling, Quality)
   - Formatted tables
   - Ready for audit documentation

2. **PDF Report** (Coming Soon)
   - Professional formatting
   - Charts and visualizations
   - Executive summary

3. **CSV Export**
   - Raw data export
   - Compatible with all tools
   - Quick download

### Report Configuration
- Custom report title
- Author information
- Selectable sections
- Include/exclude options

### Export Features
- One-click download
- Timestamped filenames
- Multiple format support

---

## 🎨 Styling and Theme

### Color Scheme
- Primary: `#1f77b4` (Blue)
- Background: `#ffffff` (White)
- Secondary: `#f0f2f6` (Light Gray)
- Text: `#262730` (Dark Gray)

### UI Elements
- Rounded corners (6-8px)
- Smooth transitions
- Hover effects
- Responsive design

### Custom Styles
- Located in `assets/styles.css`
- Streamlit theme in `.streamlit/config.toml`
- Consistent spacing and typography

---

## 🚀 Running the Application

### Start the Application
```bash
streamlit run app.py
```

### Access the Interface
```
http://localhost:8501
```

### Default Port
- Port 8501 (configurable in config.toml)

---

## 📁 File Structure

```
Audit-Canvas/
├── app.py                          # Main application entry point
├── .streamlit/
│   └── config.toml                 # Streamlit configuration
├── assets/
│   └── styles.css                  # Custom CSS styles
├── pages/
│   ├── __init__.py
│   └── dashboard.py                # Main dashboard
├── components/
│   ├── __init__.py
│   ├── upload.py                   # Upload component
│   ├── profiling.py                # Profiling component
│   ├── quality.py                  # Quality checks component
│   ├── reconciliation.py           # Reconciliation component
│   └── reports.py                  # Reports component
└── utils/
    ├── __init__.py
    ├── auth.py                     # Authentication
    └── session.py                  # Session management
```

---

## 🔧 Configuration

### Streamlit Config (`.streamlit/config.toml`)
- Theme colors
- Server settings
- Browser configuration
- Runner options

### Session State Variables
- `authenticated` - Login status
- `username` - Current user
- `current_page` - Active page
- `source_data` - Uploaded source dataset
- `target_data` - Uploaded target dataset
- `profiling_results` - Analysis results
- `quality_results` - Validation results
- `reconciliation_results` - Comparison results

---

## 💡 Usage Tips

1. **Start with Upload**
   - Always upload data before analysis
   - Use both source and target for reconciliation

2. **Run Profiling First**
   - Understand your data structure
   - Identify quality issues early

3. **Configure Quality Checks**
   - Enable relevant validation rules
   - Review failed checks carefully

4. **Use Reconciliation**
   - Compare datasets systematically
   - Review AI insights for guidance

5. **Generate Reports**
   - Export results for documentation
   - Include all relevant sections

---

## 🐛 Troubleshooting

### Common Issues

**Login Not Working**
- Verify credentials match demo accounts
- Check session state initialization

**File Upload Fails**
- Ensure file format is supported (CSV, Excel)
- Check file size (max 200MB)
- Verify file is not corrupted

**Profiling Errors**
- Ensure data is loaded
- Check for empty datasets
- Verify column data types

**Report Generation Issues**
- Confirm data is analyzed
- Check available disk space
- Verify write permissions

---

## 🔮 Future Enhancements

- Real-time collaboration
- Advanced AI insights
- Custom validation rules
- Database connectivity
- API integrations
- Mobile responsive design
- Dark mode theme
- Multi-language support

---

## 📞 Support

For issues or questions:
- Review this documentation
- Check the main README.md
- Examine component source code
- Test with demo data first

---

**Last Updated:** 2026-05-03  
**Version:** 1.0.0  
**Status:** Production Ready