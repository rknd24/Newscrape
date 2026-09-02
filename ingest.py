from sqlalchemy import select
from database import SessionLocal
from models import Article
from Newscrape import NewsFetcher

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


if __name__ == "__main__":
    ingest()

