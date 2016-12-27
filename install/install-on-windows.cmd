@echo off
echo "Finding Python installation"
where py
IF %ERRORLEVEL% NEQ 0 GOTO :readpath
py -2.7 -c "import sys; print (sys.prefix);" > pythonpathtmp.txt
GOTO :readpath
:nopy
python -c "import sys; print (sys.prefix);" > pythonpathtmp.txt
:readpath
set /p PYTHON_PATH=<pythonpathtmp.txt
del pythonpathtmp.txt

echo "Symlinking library"
mklink /j %PYTHON_PATH%\Lib\site-packages\aktos_dcs "%~dp0\aktos_dcs"
echo "installing dependencies"
pip2.7 install -r "%~dp0\requirements.txt"
pip2.7 install "%~dp0\dep\%PROCESSOR_ARCHITECTURE%\*"
echo.
echo Finished...
echo. 
pause
