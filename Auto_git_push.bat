@echo off
REM 顯示輸入提示並接收 commit 訊息
set /p commitMsg="Enter your commit message: "

REM 執行 git 指令
git add .
git commit -m "%commitMsg%"
git push -u origin main

pause
