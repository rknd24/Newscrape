# Newscrape

広告や視覚的ノイズを排除し、主要ニュースを要約付きで最短で読むためのWebアプリ。

**ライブ:** https://newscrape-front.konriku-170824.workers.dev/

Yahoo! ニュースの各カテゴリRSSを定期的に取り込み、記事本文をAIで「経緯 / ポイント / 影響」の3段に要約する。ユーザーは一覧をスキャンし、気になった記事だけ要約を展開して、必要なら元記事へ飛ぶ。

もとはCLIツールとして作り、その後 FastAPI + React に再構築し、本番デプロイまで持っていった。

## スクリーンショット

<!-- TODO: 一覧画面 / 要約展開 / スマホ表示 のスクショを docs/ に置いて貼る -->

## 構成

```
ブラウザ
  │ HTTPS
Cloudflare Workers（静的アセット）        フロントのビルド済みファイル
  │ HTTP  (VITE_API_BASE で注入したURL)
Render 無料 Web Service                  app.py (FastAPI / uvicorn) が24時間稼働
  │ SQL  (DATABASE_URL)
Neon（サーバーレス Postgres, Singapore）  記事と要約の保存先

GitHub Actions cron（30分おき）           python ingest.py を別マシンで実行し Neon に書き込む
UptimeRobot（5分おき /health）            Render のスリープ防止
LLM: Groq / qwen/qwen3.8-27b            要約生成
```

すべて無料枠。フロントとバックは別デプロイで、`git push` すると Render と Cloudflare が自動で再デプロイする。

## 設計上の判断

### 要約はユーザーのリクエスト時ではなく、取り込み時に事前生成する

当初は「ボタンを押す → その場でスクレイピング → AIに投げる → 数秒待たせる」だった。APIのレイテンシが1〜15秒とムラがあり制御できないため、要約をユーザーの経路から外した。

`ingest.py` の `generate_summaries()` が取り込みのたびに要約も作って `summary` カラムを埋める。ユーザーがボタンを押した時点では常にキャッシュヒットで体感ゼロ秒。

- 体感速度: 数秒待ち → ほぼゼロ
- API消費: 同じ記事を何人が見ても要約の生成は1回だけ
- 障害耐性: LLM側が落ちていても既存の要約は読める

`POST /analyze` はフォールバックとして残してある。事前生成が間に合っていない記事は、その場で生成して保存する。

### LLMクライアントを1クラスに隔離

`Newscrape.py` の `AIAnalyzer` がLLM呼び出しの唯一の場所。Gemini（無料枠20リクエスト/日、有料は前払い）から Groq / Qwen へ乗り換えたとき、変更はこのクラスと環境変数名だけで済んだ。app.py と ingest.py のロジックは無変更。

### 取り込みをWebプロセスから分離

取り込みは元々アプリ内のスケジューラ（APScheduler）で回していた。それだとアプリが寝ると取り込みも止まる。GitHub Actions の cron に出したことで、APIがスリープしても取り込みは続く。`ENABLE_SCHEDULER` 環境変数で本番はオフ、ローカルはオン。

## 技術スタック

| 層 | 使用技術 |
|---|---|
| フロント | React 19 / TypeScript / Vite / MUI |
| API | FastAPI / SQLAlchemy 2.0 / Pydantic |
| DB | PostgreSQL（Neon）/ 開発は SQLite |
| 取り込み | requests + BeautifulSoup（スクレイピング）、標準ライブラリ（RSSパース） |
| LLM | Groq API（qwen/qwen3.8-27b） |
| インフラ | Cloudflare Workers / Render / GitHub Actions / UptimeRobot |

## ローカルで動かす

必要な環境変数:

- `GROQ_API_KEY` — Groq のAPIキー
- `DATABASE_URL` — 未設定ならローカルの SQLite (`sqlite:///./newscrape.db`) を使う

### バックエンド（FastAPI）

```
pip install -r requirements.txt
python -m uvicorn app:app --reload --port 8000
```

### フロントエンド（React + Vite）

```
cd newscrape-front
npm install
npm run dev
```

`vite.config.ts` の proxy が `/news` と `/analyze` を `localhost:8000` に転送する。

### 取り込み（RSS取得 + 要約生成）

```
python ingest.py
```

## 注意

個人の学習目的で作っている。Yahoo! ニュースのRSSと記事本文を扱うが、公開しているのは自作のAI要約と元記事へのリンクのみで、記事本文そのものは配信していない。
