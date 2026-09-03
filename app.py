import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from Newscrape import NewsFetcher, AIAnalyzer
from database import engine, Base
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

# リクエストのデータ形式を定義
class AnalyzeRequest(BaseModel):
    link: str
    title: str

# エンドポイント1: ニュース一覧を取得する
@app.get("/news/{category_id}",response_model=NewsResponse)
def get_news(category_id: str, q: str | None = None):
    with SessionLocal() as session:
        stmt = select(Article).where(Article.category == category_id)
        if q:
            stmt = stmt.where(Article.title.contains(q))
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
