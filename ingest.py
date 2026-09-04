from sqlalchemy import select
from database import SessionLocal
from models import Article
from Newscrape import NewsFetcher,AIAnalyzer
import os

rss_map = {
    "top-picks": "https://news.yahoo.co.jp/rss/topics/top-picks.xml",
    "business": "https://news.yahoo.co.jp/rss/topics/business.xml",
    "it": "https://news.yahoo.co.jp/rss/topics/it.xml",
    "domestic": "https://news.yahoo.co.jp/rss/topics/domestic.xml",
    "world": "https://news.yahoo.co.jp/rss/topics/world.xml",
    "entertainment": "https://news.yahoo.co.jp/rss/topics/entertainment.xml",
    "sports": "https://news.yahoo.co.jp/rss/topics/sports.xml",
    "science": "https://news.yahoo.co.jp/rss/topics/science.xml",
    "local": "https://news.yahoo.co.jp/rss/topics/local.xml",
}


def ingest():
    fetcher = NewsFetcher()
    added = 0
    seen = set()

    with SessionLocal() as session:
        for category, url in rss_map.items():
            root = fetcher.fetch_rss_root(url)
            if root is None:
                continue

            for item in root.findall(".//item"):
                title = item.find("title").text
                link = item.find("link").text

                if link in seen:
                    continue  # 重複するリンクはスキップ
                seen.add(link)

                # この link の記事が既にDBにあるか探す
                existing = session.scalar(
                    select(Article).where(Article.link == link)
                )
                if existing is not None:
                    continue  # あるので飛ばす

                # 無いので新しい行を用意
                session.add(Article(title=title, link=link, category=category))
                added += 1

        session.commit()  # ここで初めてDBに書き込まれる

    print(f"{added} 件追加した")

def generate_summaries():
    fetcher = NewsFetcher()
    analyzer = AIAnalyzer(api_key=os.environ.get("GROQ_API_KEY"))
    with SessionLocal() as session:
        stmt = select(Article).where(Article.summary.is_(None))
        rows = session.scalars(stmt).all()
        for article in rows:
            body_text = fetcher.scrape_article(article.link)
            if body_text is None:
                print(f"Failed to fetch article body for {article.link}")
                continue
            summary = analyzer.analyze(body_text)
            if summary.startswith("[Error]"):
                print(f"AI analysis failed for {article.link}: {summary}")
                continue

            article.body_text = body_text
            article.summary = summary
            session.commit()
            print(f"Generated summary for {article.link}")




if __name__ == "__main__":
    ingest()
    generate_summaries()
