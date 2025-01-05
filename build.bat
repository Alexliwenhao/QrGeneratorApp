@echo off
echo 正在安装依赖...
pip install -r requirements.txt

echo 正在创建安装程序...
python setup.py bdist_msi

echo 打包完成！
pause 