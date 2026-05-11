@echo off
setlocal

if "%~1"=="" (
  echo Usage:
  echo   %~nx0 "input.pdf"
  echo   %~nx0 "input.pdf" -o "output.pdf" --overwrite
  echo.
  echo You can also drag an openable PDF onto this file.
  exit /b 1
)

python "%~dp0unlock_pdf.py" %*
