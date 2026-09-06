"""ローカルの SQLite (newscrape.db) から DATABASE_URL(Neon) へ articles を移行する一度きりのスクリプト。
link で重複を弾くので複数回実行しても安全。
"""
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

import database  # DATABASE_URL を読んで Neon の engine を作る
from models import Article

# 移行元は明示的に SQLite ファイルを指す
src_engine = create_engine(
    "sqlite:///./newscrape.db", connect_args={"check_same_thread": False}
)

added = 0
skipped = 0

with Session(src_engine) as src, Session(database.engine) as dst:
    rows = src.scalars(select(Article)).all()
    for r in rows:
        exists = dst.scalar(select(Article).where(Article.link == r.link))
        if exists is not None:
            skipped += 1
            continue
        # id はコピーしない。Neon 側で自動採番させる（あとで連番がずれないように）
        dst.add(
            Article(
                title=r.title,
                link=r.link,
                category=r.category,
                fetched_at=r.fetched_at,
                body_text=r.body_text,
                summary=r.summary,
            )
        )
        added += 1
    dst.commit()

print(f"移行完了: 追加 {added} 件 / スキップ（既存） {skipped} 件")
