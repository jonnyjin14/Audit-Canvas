# 🚀 Audit Canvas - Quick Start Guide

## Getting Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
streamlit run app.py
```

### Step 3: Access the Application
Open your browser and navigate to:
```
http://localhost:8501
```

---

## 🔐 Login Credentials

Use any of these demo accounts to login:

| Username | Password | Description |
|----------|----------|-------------|
| **admin** | admin123 | Full administrator access |
| **auditor** | audit123 | Auditor role |
| **demo** | demo123 | Demo user |

---

## 📋 Basic Workflow

### 1. Login
- Enter username and password
- Click "Login" button
- You'll be redirected to the dashboard

### 2. Upload Data
- Click "📤 Upload Data" in the sidebar
- Upload your source dataset (CSV or Excel)
- Optionally upload target dataset for reconciliation
- Review the data preview

### 3. Run Analysis
Choose from these options:

**🔍 Data Profiling**
- Automatic data quality analysis
- Statistical summaries
- Missing data detection
- Quality scoring

**✅ Quality Checks**
- Configure validation rules
- Run automated checks
- Review failed checks
- Export results

**🔄 Reconciliation**
- Compare source vs target
- Identify differences
- Column mapping analysis
- AI-powered insights

### 4. Generate Reports
- Navigate to "📊 Reports"
- Configure report settings
- Download Excel, PDF, or CSV
- Save for audit documentation

---

## 💡 Quick Tips

### For Best Results:
1. ✅ Ensure your data has headers in the first row
2. ✅ Remove any summary rows or totals
3. ✅ Use consistent date formats
4. ✅ Clean column names (no special characters)
5. ✅ Check file size (max 200MB)

### Navigation:
- Use the **sidebar menu** for main navigation
- Click **Quick Actions** on dashboard for shortcuts
- Use **breadcrumbs** to track your location
- **Logout** button is always in the sidebar

### Data Management:
- Upload both source and target for reconciliation
- Data persists during your session
- Logout clears all session data
- Re-upload if you need to start fresh

---

## 🎯 Common Use Cases

### Use Case 1: Data Quality Assessment
1. Upload your dataset
2. Go to "🔍 Data Profiling"
3. Review quality score and metrics
4. Export profiling report

### Use Case 2: Reconciliation
1. Upload source dataset
2. Upload target dataset
3. Go to "🔄 Reconciliation"
4. Run reconciliation
5. Review differences and insights
6. Export reconciliation report

### Use Case 3: Audit Documentation
1. Complete profiling and quality checks
2. Go to "📊 Reports"
3. Configure report sections
4. Download Excel report
5. Include in audit workpapers

---

## 🔧 Troubleshooting

### Application Won't Start
```bash
# Check if Streamlit is installed
pip show streamlit

# Reinstall if needed
pip install streamlit --upgrade
```

### Port Already in Use
```bash
# Use a different port
streamlit run app.py --server.port 8502
```

### Import Errors
```bash
# Reinstall all dependencies
pip install -r requirements.txt --force-reinstall
```

### File Upload Issues
- Check file format (CSV, XLSX, XLS only)
- Verify file size (under 200MB)
- Ensure file is not corrupted
- Try a different browser

---

## 📚 Additional Resources

- **Full Documentation:** See [README_UI.md](README_UI.md)
- **Security Info:** See [security-docs/README.md](security-docs/README.md)
- **Library Details:** See [LIBRARIES_SUMMARY.md](LIBRARIES_SUMMARY.md)
- **Design Document:** See [AI_Audit_Platform_Design_Document_Full.pdf](AI_Audit_Platform_Design_Document_Full.pdf)

---

## 🎨 Features Overview

### ✅ Implemented Features
- ✅ Secure login system
- ✅ Interactive dashboard
- ✅ File upload (CSV, Excel)
- ✅ Data profiling
- ✅ Quality checks
- ✅ Reconciliation engine
- ✅ Report generation
- ✅ Excel export
- ✅ CSV export
- ✅ Interactive visualizations
- ✅ AI-powered insights

### 🔮 Coming Soon
- PDF report generation
- Database connectivity
- Advanced AI features
- Custom validation rules
- Multi-user collaboration
- API integrations

---

## 📞 Need Help?

1. Check the [README_UI.md](README_UI.md) for detailed documentation
2. Review the component source code in `components/` folder
3. Test with demo data first
4. Check terminal output for error messages

---

## 🏆 IBM Bob Dev Hackathon

This project demonstrates:
- ✅ AI-assisted development
- ✅ Modern web UI with Streamlit
- ✅ Automated data quality analysis
- ✅ Professional audit workflows
- ✅ Comprehensive documentation

---

**Ready to start auditing? Login and explore!** 🚀

**Application URL:** http://localhost:8501  
**Version:** 1.0.0  
**Status:** ✅ Production Ready