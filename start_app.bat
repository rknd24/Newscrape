@echo off
chcp 65001 > nul
cd /d C:\Users\konri\Newscrape

:: 裏側のFastAPIサーバーを最小化状態で起動
start /min python -m uvicorn app:app

:: サーバーが立ち上がるまで2秒だけ待機
timeout /t 2 > nul

:: 表側の画面（ブラウザ）を開く
start index.html

exit