import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from Newscrape import NewsFetcher, AIAnalyzer, HistoryManager

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# 環境変数のチェックと各クラスの準備
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Environment variable 'GOOGLE_API_KEY' is not set.")

fetcher = NewsFetcher()
analyzer = AIAnalyzer(api_key=GOOGLE_API_KEY)
history_manager = HistoryManager()

rss_map = {
    "1": "https://news.yahoo.co.jp/rss/topics/top-picks.xml",
    "2": "https://news.yahoo.co.jp/rss/topics/business.xml",
    "3": "https://news.yahoo.co.jp/rss/topics/it.xml",
}

# リクエストのデータ形式を定義
class AnalyzeRequest(BaseModel):
    link: str
    title: str

# エンドポイント1: ニュース一覧を取得する
@app.get("/news/{category_id}")
def get_news(category_id: str):
    if category_id not in rss_map:
        raise HTTPException(status_code=404, detail="指定されたカテゴリが存在しません。")
    
    url = rss_map[category_id]
    root = fetcher.fetch_rss_root(url)
    if root is None:
        raise HTTPException(status_code=500, detail="RSSの取得に失敗しました。")
    
    all_items = root.findall('.//item')
    news_list = []
    for item in all_items:
        title = item.find("title").text
        link = item.find("link").text
        news_list.append({"title": title, "link": link})
    
    return {"articles": news_list[:10]}

# エンドポイント2: 記事をスクレイピングしてAI分析する
@app.post("/analyze")
def analyze_article(request: AnalyzeRequest):
    try:
        raw_text = fetcher.scrape_article(request.link)
        report = analyzer.analyze(raw_text)
        
        # 履歴にも保存しておく
        history_manager.save_article(request.title, report)
        
        return {
            "title": request.title,
            "report": report
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))