@echo off
echo 正在安装依赖...
pip install -r requirements.txt

echo 正在创建可执行文件...
pyinstaller --name="攀宁二维码标签生成器" ^
            --windowed ^
            --noconfirm ^
            --clean ^
            --hidden-import=PIL._tkinter_finder ^
            main.py

echo 打包完成！
echo 可执行文件位于 dist/攀宁二维码标签生成器 目录
pause 