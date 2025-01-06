import sys
import os
from cx_Freeze import setup, Executable

# 创建一个空的license.txt文件
with open('license.txt', 'w') as f:
    f.write('')

# 获取Python安装路径
PYTHON_INSTALL_DIR = r"D:\Python\Python38-32"

# Win7 32位配置
build_exe_options = {
    "packages": ["os", "sys", "tkinter", "pandas", "PIL", "qrcode"],
    "includes": [
        "tkinter.ttk",
        "tkinter.messagebox",
        "tkinter.filedialog"
    ],
    "include_files": [
        ("app.ico", "app.ico"),
        ("license.txt", "license.txt"),
        ("template.xlsx", "template.xlsx"),
        ("config.json", "config.json"),
        (os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'), os.path.join('lib', 'tcl86t.dll')),
        (os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'), os.path.join('lib', 'tk86t.dll'))
    ],
    "excludes": ["unittest", "email", "html", "http", "xml", "pydoc"],
    "include_msvcr": True,
    "build_exe": os.path.join("build", "exe.win32-3.8-win7")
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
    'target_name': "攀宁二维码标签生成器_Win7_32位"
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
            "label_generator.py",
            base=base,
            target_name="攀宁二维码标签生成器.exe",
            icon="app.ico"
        )
    ]
) 