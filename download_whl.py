import os
import urllib.request
import zipfile
import ssl

# 创建 whl 目录
if not os.path.exists('whl'):
    os.makedirs('whl')

# 忽略SSL证书验证
ssl._create_default_https_context = ssl._create_unverified_context

# 下载文件列表
files = {
    'pip-21.1.1-py3-none-any.whl': 'https://files.pythonhosted.org/packages/05/b5/67f3a13d800c2b2eb521708d40ddc180963f75eca8f2896e3c9ae84dd2d3/pip-21.1.1-py3-none-any.whl',
    'setuptools-65.5.1-py3-none-any.whl': 'https://files.pythonhosted.org/packages/ac/aa/2f17c57fa1d07f9b8b85bdcb7f89a0b11840f06fa1d1f3b0faf0aa24f227/setuptools-65.5.1-py3-none-any.whl',
    'cx_Freeze-6.8.2-cp38-cp38-win32.whl': 'https://github.com/marcelotduarte/cx_Freeze/releases/download/6.8.2/cx_Freeze-6.8.2-cp38-cp38-win32.whl',
    'pandas-1.4.4-cp38-cp38-win32.whl': 'https://github.com/pandas-dev/pandas/releases/download/v1.4.4/pandas-1.4.4-cp38-cp38-win32.whl',
    'Pillow-9.5.0-cp38-cp38-win32.whl': 'https://github.com/python-pillow/Pillow/releases/download/9.5.0/Pillow-9.5.0-cp38-cp38-win32.whl',
    'qrcode-7.4.2-py3-none-any.whl': 'https://files.pythonhosted.org/packages/64/a8/6e5b75e30774f7c0d846c01f8c4f916f5dfda1a2973b3d37a4457fb5a6f2/qrcode-7.4.2-py3-none-any.whl'
}

def verify_whl(filename):
    try:
        with zipfile.ZipFile(filename) as z:
            return True
    except:
        return False

# 下载文件
for filename, url in files.items():
    filepath = os.path.join('whl', filename)
    print(f'Downloading {filename}...')
    
    try:
        # 添加请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        req = urllib.request.Request(url, headers=headers)
        
        # 下载文件
        with urllib.request.urlopen(req) as response, open(filepath, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
            
        if verify_whl(filepath):
            print(f'{filename} downloaded and verified successfully')
        else:
            print(f'Error: {filename} is corrupted')
            os.remove(filepath)
    except Exception as e:
        print(f'Error downloading {filename}: {str(e)}')

print('Download completed') 