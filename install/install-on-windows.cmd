@echo off
echo "Symlinking library"
mklink /j C:\Python27\Lib\site-packages\aktos_dcs "%~dp0\aktos_dcs"
echo "installing dependencies"
C:\Python27\Scripts\pip install -r "%~dp0\requirements.txt"
echo.
echo Finished...
echo. 
pause
