from datetime import datetime, timedelta, timezone
from sqlalchemy import select, delete
from database import SessionLocal
from models import Article
from Newscrape import NewsFetcher,AIAnalyzer
import os

# top-picks は他カテゴリの寄せ集めで、取り込むと同じ記事が先勝ちで top-picks 扱いになり
# 各カテゴリから消える。総合(=all)は app.py 側で全カテゴリ横断にしたので top-picks は取り込まない
rss_map = {
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
                title_el = item.find("title")
                link_el = item.find("link")
                # RSSが壊れていて title / link が欠けている item はスキップ（ここで死なせない）
                if title_el is None or link_el is None or not title_el.text or not link_el.text:
                    continue
                title = title_el.text
                link = link_el.text

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


def prune_old(days: int = 4):
    """一定日数より古い記事を削除する。

    Yahoo トピックスの記事は数日で鮮度が落ちる。ためこむと総合タブや
    チャットの context が古い記事で薄まり、DB も肥大化する。cron で毎回呼ぶ。
    """
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    with SessionLocal() as session:
        result = session.execute(
            delete(Article).where(Article.fetched_at < cutoff)
        )
        session.commit()
    print(f"{result.rowcount} 件削除した（{days}日より古い記事）")


if __name__ == "__main__":
    ingest()
    generate_summaries()
    prune_old()
