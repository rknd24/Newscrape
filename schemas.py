"""APIのリクエスト / レスポンスのデータ形式（Pydanticモデル）をまとめる。

app.py のエンドポイント定義と、実際にやり取りするJSONの「契約」を分離しておく。
FastAPI はここの型から /docs（Swagger UI）も自動生成する。
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


# --- ニュース一覧 ---

class ArticleOut(BaseModel):
    # SQLAlchemy の Article オブジェクトをそのまま渡せるようにする
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    link: str
    category: str
    summary: str | None
    fetched_at: datetime


class NewsResponse(BaseModel):
    articles: list[ArticleOut]


# --- 記事のAI分析 ---

class AnalyzeRequest(BaseModel):
    link: str
    title: str


# --- Chat機能 ---

class ChatMessage(BaseModel):
    """会話の1行。過去・現在、user・assistant を問わず全て同じ形。"""
    role: str
    content: str


class ChatRequest(BaseModel):
    question: str
    articles_ids: list[int]
    history: list[ChatMessage] | None = None


class ChatResponse(BaseModel):
    answer: str
