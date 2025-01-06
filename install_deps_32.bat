@echo off
echo Installing dependencies for Python 3.8 32bit...

echo Setting up pip config...
D:\Python\Python38-32\python.exe -m pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
D:\Python\Python38-32\python.exe -m pip config set install.trusted-host mirrors.aliyun.com

echo Installing setuptools...
D:\Python\Python38-32\python.exe -m pip install setuptools==65.5.1

echo Installing cx_Freeze...
D:\Python\Python38-32\python.exe -m pip install cx_Freeze==6.8.2

echo Installing required packages...
D:\Python\Python38-32\python.exe -m pip install pandas==1.4.4 numpy==1.19.5 openpyxl==3.0.9
D:\Python\Python38-32\python.exe -m pip install Pillow==9.5.0 qrcode==7.4.2

echo Dependencies installation completed.
pause 