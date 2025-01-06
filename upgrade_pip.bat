@echo off
echo Upgrading pip...
cd whl
D:\Python\Python38-32\python.exe -m pip install --no-index --find-links=. pip-24.3.1-py3-none-any.whl
cd ..
echo Pip upgrade completed.
pause 