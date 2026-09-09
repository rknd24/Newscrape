import os
from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from Newscrape import NewsFetcher, AIAnalyzer
from database import engine, Base
from sqlalchemy import select
from database import SessionLocal
from models import Article
from ingest import ingest, reset_broken_summaries, generate_summaries, prune_old
from schemas import NewsResponse, AnalyzeRequest, ChatRequest, ChatResponse

# データベースの初期化
Base.metadata.create_all(bind=engine)


def run_ingest_job():
    """RSS取り込み + 要約の事前生成をまとめて実行する定期ジョブ"""
    try:
        ingest()
        reset_broken_summaries()
        generate_summaries()
        prune_old()
    except Exception as e:
        print(f"[Error] 定期取り込みジョブが失敗しました: {e}")


scheduler = BackgroundScheduler()

# 本番(Render)では取り込みを GitHub Actions に任せるのでスケジューラはオフ。
# ローカルは既定でオン。ENABLE_SCHEDULER=0 で明示的に切れる。
ENABLE_SCHEDULER = os.environ.get("ENABLE_SCHEDULER", "1") == "1"


@asynccontextmanager
async def lifespan(app: FastAPI):
    if ENABLE_SCHEDULER:
        # 起動直後に1回、そのあと30分おきに実行。バックグラウンドスレッドで動くのでAPIの応答をブロックしない
        scheduler.add_job(run_ingest_job, "interval", minutes=30, next_run_time=datetime.now())
        scheduler.start()
    yield
    if scheduler.running:
        scheduler.shutdown()


app = FastAPI(lifespan=lifespan)

# 本番はフロントのドメインだけ許可。未設定なら開発用に全許可。
# 例: ALLOWED_ORIGINS="https://newscrape.pages.dev"
ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,  # Cookie/認証は使っていない
    allow_methods=["*"],
    allow_headers=["*"],
)

# スリープ防止の外部監視（UptimeRobot）が叩く。DBは触らない
@app.get("/health")
def health():
    return {"ok": True}


# 環境変数のチェックと各クラスの準備
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("Environment variable 'GROQ_API_KEY' is not set.")

fetcher = NewsFetcher()
analyzer = AIAnalyzer(api_key=GROQ_API_KEY)


# エンドポイント1: ニュース一覧を取得する
@app.get("/news/{category_id}",response_model=NewsResponse)
def get_news(category_id: str, q: str | None = None):
    with SessionLocal() as session:
        stmt = select(Article)
        # "all" のときはカテゴリで絞らない（総合 = 全カテゴリ横断）
        if category_id != "all":
            stmt = stmt.where(Article.category == category_id)
        if q:
            # タイトルだけでなく本文も対象にする（「大谷」は見出しに出るが「大谷翔平」は本文にしか出ない等）
            stmt = stmt.where(
                Article.title.contains(q) | Article.body_text.contains(q)
            )
        stmt = stmt.order_by(Article.fetched_at.desc()).limit(30)
        rows = session.scalars(stmt).all()
    return NewsResponse(articles=rows)


# エンドポイント2: 記事をスクレイピングしてAI分析する
@app.post("/analyze")
def analyze_article(article: AnalyzeRequest):
    with SessionLocal() as session:
        try:
            row = session.scalar(select(Article).where(Article.link == article.link))
            if row is None:
                raise HTTPException(status_code=404, detail="Article not found in the database.")
            if row.summary is not None:
                return {
                    "title": row.title,
                    "report": row.summary
                }
            else:
                # 記事本文をスクレイピング
                body_text = fetcher.scrape_article(article.link)
                if body_text is None:
                    raise HTTPException(status_code=404, detail="Failed to fetch article body.")
                
                # AI分析
                summary = analyzer.analyze(body_text)
                if summary.startswith("[Error]"):
                    raise HTTPException(status_code=502,detail="AI分析に失敗しました。")
                
                # データベースに保存
                row.body_text = body_text
                row.summary = summary
                session.commit()
                
                return {
                    "title": row.title,
                    "report": summary
                }
        
        except HTTPException:
            raise 
        except Exception as e:
            raise HTTPException(status_code=500,detail=str(e))



#エンドポイント3　:Chat機能を実装する
@app.post("/chat",response_model=ChatResponse)
def chat(chat_request: ChatRequest):
    question = chat_request.question
    article_id = chat_request.article_id
    history = chat_request.history

    with SessionLocal() as session:
        try:
            # フロントは「AIに聞く」で選んだ1記事の id を送ってくる。
            # その記事の本文を context にして深掘りに答える
            article = session.scalar(select(Article).where(Article.id == article_id))
            if article is None:
                raise HTTPException(status_code=404, detail="Article not found in the database.")
            context = f"記事タイトル: {article.title}\n記事本文: {article.body_text or article.summary or ''}"
            #AIに質問する
            answer = analyzer.chat(
                context,
                question,
                [{"role": h.role, "content": h.content} for h in history]
            )
            return {"answer":answer}
        except HTTPException:
            raise 
        except Exception as e:
            raise HTTPException(status_code=500,detail=str(e))

