import os
import tempfile

# ここが一番大事な部分。`app`（→ `database.py`）を import する前に、
# 環境変数をテスト専用のSQLiteに向けておく。database.py はモジュール読み込みの
# 瞬間に DATABASE_URL を読んで engine を作るので、import した後から差し替えられない。
_test_db_fd, _test_db_path = tempfile.mkstemp(suffix=".db")
os.environ["DATABASE_URL"] = f"sqlite:///{_test_db_path}"

# テスト起動時に本物の ingest が走らないように。無ければ lifespan がスケジューラを起動する
os.environ["ENABLE_SCHEDULER"] = "0"

# app.py は起動時に GROQ_API_KEY の存在チェックをするだけ（無いと import が落ちる）。
# /news のテストは実際に Groq を呼ばないので、ダミーの値で通す。
os.environ.setdefault("GROQ_API_KEY", "test-dummy-key")

import pytest
from fastapi.testclient import TestClient
from app import app


@pytest.fixture
def client():
    """テスト用DBに繋がった状態の TestClient を返す fixture。

    引数に `client` と書くだけで、pytest がこれを実行して結果を渡してくれる。
    `with TestClient(app) as c` にしてるのは、app.py の lifespan
    （起動・終了時の処理）もちゃんと動かすため。
    """
    with TestClient(app) as c:
        yield c
