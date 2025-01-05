import PyInstaller.__main__
import os

# 确保输出目录存在
if not os.path.exists('dist'):
    os.makedirs('dist')

PyInstaller.__main__.run([
    'main.py',                            # 主程序文件
    '--name=攀宁二维码标签生成器',         # 程序名称
    '--windowed',                         # 使用 GUI 模式
    '--noconfirm',                        # 覆盖现有文件
    '--clean',                            # 清理临时文件
    '--add-data=README.md;.',             # 添加额外文件
    '--hidden-import=PIL._tkinter_finder', # 添加隐藏导入
    '--icon=icon.ico',                    # 程序图标（如果有）
    '--distpath=dist',                    # 输出目录
    '--workpath=build',                   # 工作目录
    '--specpath=build',                   # spec文件目录
]) 