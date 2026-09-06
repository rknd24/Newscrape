import os

from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# 本番は環境変数 DATABASE_URL（Neon の Postgres）、無ければローカルの SQLite
# 環境変数UIへの貼り付けで改行や空白が混じることがあるので全部除去する（URLに空白は無いので安全）
raw_url = "".join(os.environ.get("DATABASE_URL", "sqlite:///./newscrape.db").split())

# 一部のホストは古い "postgres://" 形式で渡してくる。SQLAlchemy 2.0 は受け付けないので直す
if raw_url.startswith("postgres://"):
    raw_url = raw_url.replace("postgres://", "postgresql://", 1)

url = make_url(raw_url)
is_sqlite = url.get_backend_name() == "sqlite"

if is_sqlite:
    connect_args = {"check_same_thread": False}  # SQLite 専用
else:
    # ?sslmode=... &channel_binding=... のクエリを全部落とす。
    # 必要なオプションは connect_args で psycopg2 に直接渡す
    url = url.set(query={})
    connect_args = {"sslmode": "require"}

engine = create_engine(
    url,
    connect_args=connect_args,
    # Neon は無アクセスで停止する。復帰後の古い接続を掴まないよう、使う前に SELECT 1 で生存確認する
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass
