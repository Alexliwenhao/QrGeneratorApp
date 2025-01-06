@echo off
echo Installing dependencies for Python 3.8 32bit...

echo Setting up pip config...
D:\Python\Python38-32\python.exe -m pip config set global.index-url http://mirrors.aliyun.com/pypi/simple/
D:\Python\Python38-32\python.exe -m pip config set install.trusted-host mirrors.aliyun.com

echo Installing basic packages...
D:\Python\Python38-32\python.exe -m pip install --trusted-host mirrors.aliyun.com --trusted-host pypi.org --trusted-host files.pythonhosted.org setuptools==65.5.1
D:\Python\Python38-32\python.exe -m pip install --trusted-host mirrors.aliyun.com --trusted-host pypi.org --trusted-host files.pythonhosted.org wheel>=0.38.4

echo Installing cx_Freeze...
D:\Python\Python38-32\python.exe -m pip uninstall -y cx_Freeze
D:\Python\Python38-32\python.exe -m pip install --trusted-host mirrors.aliyun.com --trusted-host pypi.org --trusted-host files.pythonhosted.org cx_Freeze==6.15.12

echo Installing required packages...
D:\Python\Python38-32\python.exe -m pip install --trusted-host mirrors.aliyun.com --trusted-host pypi.org --trusted-host files.pythonhosted.org pandas==1.4.4
D:\Python\Python38-32\python.exe -m pip install --trusted-host mirrors.aliyun.com --trusted-host pypi.org --trusted-host files.pythonhosted.org Pillow==9.5.0
D:\Python\Python38-32\python.exe -m pip install --trusted-host mirrors.aliyun.com --trusted-host pypi.org --trusted-host files.pythonhosted.org qrcode==7.4.2

echo Dependencies installation completed.
pause 