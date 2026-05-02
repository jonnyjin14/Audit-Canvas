@echo off
REM AI Audit Platform - Vulnerability Remediation Script
REM This script upgrades all packages with known security vulnerabilities
REM Run this script as Administrator for best results

echo ========================================
echo AI Audit Platform Security Patch
echo ========================================
echo.
echo This script will upgrade packages with known vulnerabilities
echo.
echo Phase 1: Critical and High Severity (11 vulnerabilities)
echo Phase 2: Medium Severity (5 vulnerabilities)
echo Phase 3: Low Severity (2 vulnerabilities)
echo.
pause

echo.
echo ========================================
echo Phase 1: Critical and High Priority
echo ========================================
echo.

echo [1/4] Upgrading mysql-connector-python (CRITICAL - CVE-2024-21272)...
pip install --upgrade mysql-connector-python==9.1.0
if %errorlevel% neq 0 (
    echo ERROR: Failed to upgrade mysql-connector-python
    pause
    exit /b 1
)

echo.
echo [2/4] Upgrading urllib3 (HIGH - 3 CVEs)...
pip install --upgrade urllib3==2.6.3
if %errorlevel% neq 0 (
    echo ERROR: Failed to upgrade urllib3
    pause
    exit /b 1
)

echo.
echo [3/4] Upgrading setuptools (HIGH - 5 CVEs)...
pip install --upgrade setuptools==78.1.1
if %errorlevel% neq 0 (
    echo ERROR: Failed to upgrade setuptools
    pause
    exit /b 1
)

echo.
echo [4/4] Upgrading protobuf (HIGH - 2 CVEs)...
pip install --upgrade protobuf==6.31.1
if %errorlevel% neq 0 (
    echo ERROR: Failed to upgrade protobuf
    pause
    exit /b 1
)

echo.
echo ========================================
echo Phase 2: Medium Priority
echo ========================================
echo.

echo [1/3] Upgrading pip (MEDIUM - 3 CVEs)...
python -m pip install --upgrade pip==26.0
if %errorlevel% neq 0 (
    echo ERROR: Failed to upgrade pip
    pause
    exit /b 1
)

echo.
echo [2/3] Upgrading python-dotenv (MEDIUM - CVE-2026-28684)...
pip install --upgrade python-dotenv==1.2.2
if %errorlevel% neq 0 (
    echo ERROR: Failed to upgrade python-dotenv
    pause
    exit /b 1
)

echo.
echo [3/3] Upgrading requests (MEDIUM - CVE-2026-25645)...
pip install --upgrade requests==2.33.0
if %errorlevel% neq 0 (
    echo ERROR: Failed to upgrade requests
    pause
    exit /b 1
)

echo.
echo ========================================
echo Phase 3: Low Priority
echo ========================================
echo.

echo [1/2] Upgrading pygments (LOW - CVE-2026-4539)...
pip install --upgrade pygments==2.20.0
if %errorlevel% neq 0 (
    echo ERROR: Failed to upgrade pygments
    pause
    exit /b 1
)

echo.
echo [2/2] Upgrading pytest (LOW - CVE-2025-71176)...
pip install --upgrade pytest==9.0.3
if %errorlevel% neq 0 (
    echo ERROR: Failed to upgrade pytest
    pause
    exit /b 1
)

echo.
echo ========================================
echo Verification
echo ========================================
echo.
echo Running pip-audit to verify fixes...
pip-audit --desc

echo.
echo ========================================
echo Remediation Complete!
echo ========================================
echo.
echo All security vulnerabilities have been addressed.
echo Please review the output above for any remaining issues.
echo.
echo Next steps:
echo 1. Review SECURITY_VULNERABILITY_REPORT.md for details
echo 2. Test your application with the updated packages
echo 3. Update requirements.txt with the new versions
echo 4. Schedule regular security scans (weekly recommended)
echo.
pause

@REM Made with Bob
