@echo off
echo Select build version:
echo 1. Standard Version (64-bit)
echo 2. Win7 32-bit Version
echo 3. Build Both Versions

set /p choice=Please enter your choice (1-3): 

if "%choice%"=="1" (
    echo Creating standard 64-bit version installer...
    python setup.py bdist_msi
) else if "%choice%"=="2" (
    echo Creating Win7 32-bit version installer...
    call install_deps_32.bat
    D:\Python\Python38-32\python.exe setup_32.py bdist_msi
) else if "%choice%"=="3" (
    echo Creating standard 64-bit version installer...
    python setup.py bdist_msi
    
    echo Creating Win7 32-bit version installer...
    call install_deps_32.bat
    D:\Python\Python38-32\python.exe setup_32.py bdist_msi
) else (
    echo Invalid choice!
)

echo Build completed!
pause 