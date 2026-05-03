# Audit-Canvas
## AI-Assisted Audit Data Quality & Reconciliation Platform

This is the Audit Canvas Project for IBM Bob Dev Hackathon - a web-based AI-assisted audit platform designed to streamline data validation, reconciliation, and audit documentation.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11.3 or higher
- pip (Python package manager)
- Windows OS (for .bat scripts) or Linux/Mac

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Audit-Canvas
   ```

2. **Install all required packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run security vulnerability scan**
   ```bash
   pip-audit --desc
   ```

4. **Fix security vulnerabilities (IMPORTANT!)**
   ```bash
   # Windows
   fix_vulnerabilities.bat
   
   # Linux/Mac
   chmod +x fix_vulnerabilities.sh
   ./fix_vulnerabilities.sh
   ```

---

## 📦 Installed Libraries

### Core Framework & Data Processing
- **streamlit** (1.57.0) - Web UI framework
- **pandas** (3.0.2) - Data manipulation and analysis
- **numpy** (2.4.4) - Numerical computing

### File Handling & Excel Support
- **openpyxl** (3.1.5) - Excel (.xlsx) file operations
- **xlrd** (2.0.2) - Excel (.xls) file reading
- **xlsxwriter** (3.2.9) - Enhanced Excel report generation

### Data Quality & Analysis
- **python-dateutil** (2.9.0.post0) - Date validation
- **scipy** (1.17.1) - Statistical analysis
- **plotly** (6.7.0) - Interactive data visualization

### Report Generation
- **jinja2** (3.1.6) - HTML template rendering

### Security & Monitoring
- **pip-audit** (2.10.0) - Vulnerability scanner

### Optional Enhancements
- **streamlit-aggrid** (1.2.1.post2) - Enhanced data grids
- **pillow** (12.2.0) - Image handling
- **requests** (2.32.5) - HTTP operations

For a complete list, see [LIBRARIES_SUMMARY.md](LIBRARIES_SUMMARY.md)

---

## 🔒 Security

### Vulnerability Status
✅ **SECURE:** All vulnerabilities have been resolved! **0 known vulnerabilities**

**Security Status (Updated 2026-05-02 20:43 UTC):**
- ✅ All 18 vulnerabilities have been patched
- ✅ All packages upgraded to secure versions
- ✅ Verified with pip-audit: No known vulnerabilities found

**Remediation Summary:**
- 🔴 Critical: 1 vulnerability → ✅ FIXED (mysql-connector-python 9.1.0)
- 🟠 High: 10 vulnerabilities → ✅ FIXED (urllib3 2.6.3, setuptools 78.1.1, protobuf 6.33.5)
- 🟡 Medium: 5 vulnerabilities → ✅ FIXED (pip 26.1, python-dotenv 1.2.2, requests 2.33.0)
- 🟢 Low: 2 vulnerabilities → ✅ FIXED (pygments 2.20.0, pytest 9.0.3)

### Security Documentation

All security files are organized in the **security-docs/** folder:
- [security-docs/README.md](security-docs/README.md) - **START HERE** - Complete guide to all security files
- [security-docs/SECURITY_REMEDIATION_LOG.md](security-docs/SECURITY_REMEDIATION_LOG.md) - Complete remediation log
- [security-docs/SECURITY_VULNERABILITY_REPORT.md](security-docs/SECURITY_VULNERABILITY_REPORT.md) - Initial findings
- [security-docs/vulnerability_scan.json](security-docs/vulnerability_scan.json) - Machine-readable scan results
- [security-docs/fix_vulnerabilities.bat](security-docs/fix_vulnerabilities.bat) - Automated fix script

### Regular Security Scanning
```bash
# Run weekly vulnerability scans
pip-audit --desc

# Generate JSON report
pip-audit --format json --output vulnerability_scan.json
```

---

## 🎯 Platform Features

Based on the [AI Audit Platform Design Document](AI_Audit_Platform_Design_Document_Full.pdf):

### 1. Data Profiling
- Row/column counts
- Missing values detection
- Duplicate detection
- Data type validation
- Outlier identification

### 2. Data Quality Rule Engine
- Required fields validation
- Unique primary keys
- Date format validation
- Value range checks
- Referential integrity

### 3. Reconciliation Engine
- Record count comparison
- Missing/extra records detection
- Column mapping validation
- Data type consistency checks

### 4. AI-Powered Features
- Anomaly explanation in plain English
- Column mapping suggestions
- Automated audit findings generation
- Documentation assistance

### 5. Report Generation
- Excel workpapers export
- HTML audit reports
- Interactive visualizations

---

## 🏗️ Technology Stack

- **Frontend:** Streamlit
- **Backend:** Python 3.11.3
- **Data Processing:** pandas, numpy, scipy
- **Visualization:** plotly
- **AI Integration:** IBM Bob
- **Output Formats:** Excel (openpyxl, xlsxwriter), HTML (jinja2)

---

## 📋 Project Structure

```
Audit-Canvas/
├── AI_Audit_Platform_Design_Document_Full.pdf  # Full design specification
├── requirements.txt                             # Python dependencies (updated with secure versions)
├── LIBRARIES_SUMMARY.md                         # Detailed library documentation
├── LICENSE                                      # Project license
├── README.md                                    # This file (main documentation)
│
└── security-docs/                               # Security documentation folder
    ├── README.md                                # Guide to all security files
    ├── SECURITY_VULNERABILITY_REPORT.md         # Initial vulnerability analysis
    ├── SECURITY_REMEDIATION_LOG.md              # Complete remediation timeline
    ├── vulnerability_scan.json                  # Machine-readable scan results
    └── fix_vulnerabilities.bat                  # Automated remediation script
```

---

## 🚦 Getting Started with Development

### 1. Set Up Environment
```bash
# Verify Python version
python --version  # Should be 3.11.3 or higher

# Install dependencies
pip install -r requirements.txt

# Fix security vulnerabilities
fix_vulnerabilities.bat
```

### 2. Run the Application
```bash
streamlit run app.py
```

### 3. Access the Platform
Open your browser and navigate to:
```
http://localhost:8501
```

---

## 🔧 Development Workflow

### User Workflow
1. Upload datasets (CSV/Excel)
2. Run automated profiling
3. Execute data quality checks
4. Perform reconciliation
5. Review AI-generated insights
6. Export audit report

### Example Scenario
```
Source Dataset: 10,000 rows
Target Dataset: 9,850 rows

Findings:
- 150 missing records detected
- 138 null values identified
- Column mapping mismatch found
- AI-generated explanation provided
```

---

## 👥 Team Structure

**Member 1:** Backend Development
- Data processing logic
- Quality rule engine
- Reconciliation algorithms

**Member 2:** UI/UX Design
- Streamlit interface
- Presentation materials
- Documentation

---

## 🤖 IBM Bob Integration

IBM Bob is used as an AI development assistant to:
- Accelerate coding and testing
- Debug issues efficiently
- Generate documentation
- Provide code suggestions
- Enable rapid prototyping

---

## 📊 Success Metrics

- ⏱️ Time saved in audit tasks
- 🔍 Number of issues detected
- 📉 Reduction in manual effort
- 👥 User adoption rate
- ✅ Accuracy improvements

---

## 🔮 Future Enhancements

- Database integration (PostgreSQL, MySQL)
- Role-based access control
- Real-time monitoring dashboard
- Advanced anomaly detection (ML models)
- Enterprise audit workflow integration
- Multi-user collaboration
- API for external integrations

---

## 📚 Documentation

- **Design Document:** [AI_Audit_Platform_Design_Document_Full.pdf](AI_Audit_Platform_Design_Document_Full.pdf)
- **Library Reference:** [LIBRARIES_SUMMARY.md](LIBRARIES_SUMMARY.md)
- **Security Report:** [SECURITY_VULNERABILITY_REPORT.md](SECURITY_VULNERABILITY_REPORT.md)

### External Resources
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Plotly Documentation](https://plotly.com/python/)
- [pip-audit Documentation](https://pypi.org/project/pip-audit/)

---

## 🛡️ Security Best Practices

1. **Regular Scans:** Run `pip-audit` weekly
2. **Dependency Updates:** Keep packages up-to-date
3. **Virtual Environments:** Use isolated environments for production
4. **Access Control:** Implement proper authentication
5. **Data Encryption:** Encrypt sensitive audit data
6. **Audit Logging:** Track all data access and modifications

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the terms specified in the [LICENSE](LICENSE) file.

---

## 🏆 IBM Bob Dev Hackathon

This project demonstrates how AI and Python can transform audit workflows by improving:
- ✅ **Efficiency:** Automated data validation and profiling
- ✅ **Accuracy:** Consistent quality checks and reconciliation
- ✅ **Scalability:** Handle large datasets efficiently
- ✅ **Transparency:** AI-powered explanations and documentation
- ✅ **Usability:** Simple, intuitive web interface

---

## 📞 Support

For questions, issues, or contributions:
- Open an issue on GitHub
- Contact the development team
- Review the documentation

---

## ⚠️ Important Notes

1. **Security First:** Always run `fix_vulnerabilities.bat` after initial installation
2. **Testing:** Test all updates in a staging environment before production
3. **Backups:** Maintain regular backups of audit data
4. **Compliance:** Ensure compliance with relevant audit standards (SOC 2, ISO 27001, etc.)

---

**Last Updated:** 2026-05-02 20:43 UTC
**Version:** 1.0.0
**Python Version:** 3.11.3
**Security Status:** ✅ SECURE - All vulnerabilities resolved (0 known vulnerabilities)
**Status:** Ready for Development
