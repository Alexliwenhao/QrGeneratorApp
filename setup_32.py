import sys
import os
from cx_Freeze import setup, Executable

# 创建一个空的license.txt文件
with open('license.txt', 'w') as f:
    f.write('')

# Win7 32位配置
build_exe_options = {
    "packages": [
        "pandas", 
        "PIL", 
        "qrcode", 
        "tkinter",
        "numpy",
        "openpyxl",
        "json",
        "datetime",
        "six",
        "appdirs",
        "packaging",
        "pyparsing"
    ],
    "includes": [
        "tkinter", 
        "tkinter.ttk",
        "tkinter.messagebox",
        "tkinter.filedialog",
        "PIL.Image",
        "PIL.ImageTk",
        "pandas.core",
        "pandas.io.excel"
    ],
    "excludes": ["test", "distutils"],
    "include_files": [
        ("app.ico", "app.ico"),
        ("license.txt", "license.txt"),
        ("template.xlsx", "template.xlsx"),
        ("config.json", "config.json")
    ],
    "include_msvcr": True,  # 包含Visual C++ 运行库
    "optimize": 2,  # 优化字节码
    "build_exe": "build/exe.win32-3.8-win7",  # 指定输出目录
    "replace_paths": [("*", "")],  # 移除路径信息
    "zip_include_packages": "*",  # 包含所有包
    "zip_exclude_packages": ""    # 不排除任何包
}

# 创建快捷方式
shortcut_table = [
    ("DesktopShortcut",        # Shortcut
     "DesktopFolder",          # Directory_
     "攀宁二维码标签生成器_Win7",  # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]攀宁二维码标签生成器.exe",   # Target
     None,                     # Arguments
     "攀宁二维码标签生成器 Win7版本", # Description
     "[TARGETDIR]app.ico",     # Icon
     0,                        # IconIndex
     None,                     # ShowCmd
     "TARGETDIR"               # WkDir
     )
]

msi_data = {
    "Shortcut": shortcut_table,
    "Directory": [
        ("ProgramMenuFolder", "TARGETDIR", "."),
        ("DesktopFolder", "TARGETDIR", ".")
    ]
}

bdist_msi_options = {
    'data': msi_data,
    'initial_target_dir': r'[ProgramFilesFolder]\攀宁二维码标签生成器_Win7',
    'upgrade_code': '{9F13ACDF-A3BE-11EE-A506-0242AC120003}',
    'add_to_path': False,
    'install_icon': "app.ico",
    'target_name': "攀宁二维码标签生成器_Win7_32位",  # 指定MSI文件名
    'all_users': True,  # 为所有用户安装
    'summary_data': {
        'author': '攀宁科技',
        'comments': 'Win7 32位版本',
        'keywords': 'QR Code Generator'
    }
}

# 确保使用Win32GUI
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="攀宁二维码标签生成器_Win7",
    version="1.0.0",
    description="攀宁二维码标签生成器 (Win7 32位版本)",
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options
    },
    executables=[
        Executable(
            "label_generator.py",  # 使用正确的入口文件名
            base=base,
            target_name="攀宁二维码标签生成器.exe",
            icon="app.ico",
            copyright="Copyright (C) 2024 攀宁科技"  # 添加版权信息
        )
    ]
) 