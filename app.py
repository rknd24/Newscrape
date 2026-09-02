import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from Newscrape import NewsFetcher, AIAnalyzer, HistoryManager
from database import engine, Base
import models
from sqlalchemy import select
from database import SessionLocal
from models import Article

# データベースの初期化
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ArticleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    link: str
    category: str
    summary: str | None

class NewsResponse(BaseModel):
    articles: list[ArticleOut]


# 環境変数のチェックと各クラスの準備
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Environment variable 'GOOGLE_API_KEY' is not set.")

fetcher = NewsFetcher()
analyzer = AIAnalyzer(api_key=GOOGLE_API_KEY)
history_manager = HistoryManager()

# リクエストのデータ形式を定義
class AnalyzeRequest(BaseModel):
    link: str
    title: str

# エンドポイント1: ニュース一覧を取得する
@app.get("/news/{category_id}",response_model=NewsResponse)
def get_news(category_id: str):
    with SessionLocal() as session:
        stmt = (
            select(Article)
            .where(Article.category == category_id)
            .order_by(Article.fetched_at.desc())
            .limit(30)
        )
        rows = session.scalars(stmt).all()
    return NewsResponse(articles=rows)


# エンドポイント2: 記事をスクレイピングしてAI分析する
@app.post("/analyze")
def analyze_article(article: AnalyzeRequest):
    try:
        body_text = fetcher.scrape_article(article.link)
        if body_text == None:
            raise HTTPException(status_code=404,detail="Item not found")
        report = analyzer.analyze(body_text)
            
            # 履歴にも保存しておく
        try:
            history_manager.save_article(article.title, report)
        except Exception:
            pass
            
        return {
            "title": article.title,
            "report": report
        }
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
