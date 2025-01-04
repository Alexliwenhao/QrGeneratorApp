import PyInstaller.__main__
import os

# 获取当前目录
current_dir = os.path.dirname(os.path.abspath(__file__))

PyInstaller.__main__.run([
    'label_generator.py',  # 主程序文件
    '--name=二维码生成器',  # 生成的exe名称
    '--windowed',  # 不显示控制台窗口
    '--onefile',  # 打包成单个exe文件
    '--icon=label.ico',  # 如果你有图标文件的话
    '--add-data=simsun.ttc;.',  # 添加宋体字体文件
    f'--distpath={os.path.join(current_dir, "dist")}',  # 输出目录
    '--clean',  # 清理临时文件
    '--noconfirm',  # 不确认覆盖
]) 