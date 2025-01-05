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

# 创建开始菜单快捷方式
shortcut_table = [
    ("ProgramMenuShortcut",
     "ProgramMenuFolder",
     "攀宁二维码标签生成器",
     "TARGETDIR",
     "[TARGETDIR]攀宁二维码标签生成器.exe",
     None,
     "攀宁二维码标签生成器",
     "[TARGETDIR]攀宁二维码标签生成器.exe",
     0,
     None,
     None,
     "TARGETDIR"
     )
]

# 配置MSI安装程序
msi_data = {
    "Shortcut": shortcut_table
}

bdist_msi_options = {
    'data': msi_data,
    'initial_target_dir': r'[ProgramFilesFolder]\攀宁二维码标签生成器',
    'upgrade_code': '{9F13ACDF-A3BE-11EE-A506-0242AC120002}',
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
            icon="app.ico"
        )
    ]
) 