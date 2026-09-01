# Newscrape

情報のノイズ（不要な広告やGUIの装飾）を極限まで削減し、コマンドライン（CUI）上で主要なニュースを最速でパース・スクレイピングするPythonツール。

## 開発環境
- Python 3.12.7
- Git

## 起動方法

### バックエンド（FastAPI）
環境変数 `GOOGLE_API_KEY` を設定した上で実行:
```
python -m uvicorn app:app --reload --port 8000
```
※ `--reload` を付けないとコード変更が反映されないので注意

### フロントエンド（React + Vite）
```
cd newscrape-front
npm run dev
```