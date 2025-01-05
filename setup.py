import sys
import os
from cx_Freeze import setup, Executable

# 创建一个空的license.txt文件
with open('license.txt', 'w') as f:
    f.write('')

# 依赖包
build_exe_options = {
    "packages": ["pandas", "PIL", "qrcode", "tkinter"],
    "includes": ["tkinter", "tkinter.ttk"],
    "include_files": [
        ("app.ico", "app.ico"),
        ("license.txt", "license.txt"),
    ],
}

# 创建快捷方式
shortcut_table = [
    # 桌面快捷方式
    ("DesktopShortcut",        # Shortcut
     "DesktopFolder",          # Directory_
     "攀宁二维码标签生成器",     # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]攀宁二维码标签生成器.exe",   # Target
     None,                     # Arguments
     "攀宁二维码标签生成器",     # Description
     None,                     # Hotkey
     None,                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     "TARGETDIR",              # WkDir
     ),
    
    # 开始菜单快捷方式
    ("ProgramMenuShortcut",    # Shortcut
     "ProgramMenuFolder",      # Directory_
     "攀宁二维码标签生成器",     # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]攀宁二维码标签生成器.exe",   # Target
     None,                     # Arguments
     "攀宁二维码标签生成器",     # Description
     None,                     # Hotkey
     None,                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     "TARGETDIR",              # WkDir
     )
]

# MSI数据
msi_data = {
    "Shortcut": shortcut_table
}

# MSI选项
bdist_msi_options = {
    'data': msi_data,
    'initial_target_dir': r'[ProgramFilesFolder]\攀宁二维码标签生成器',
    'upgrade_code': '{9F13ACDF-A3BE-11EE-A506-0242AC120002}',
    'add_to_path': False,
    'install_icon': "app.ico"
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="攀宁二维码标签生成器",
    version="1.0.0",
    description="攀宁二维码标签生成器",
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options
    },
    executables=[
        Executable(
            "main.py",
            base=base,
            target_name="攀宁二维码标签生成器.exe",
            icon="app.ico",
            shortcut_name="攀宁二维码标签生成器",
            shortcut_dir="DesktopFolder"
        )
    ]
) 