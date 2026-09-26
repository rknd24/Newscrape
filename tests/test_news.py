from database import SessionLocal
from models import Article


def test_news(client):
    with SessionLocal() as session:
        session.add(Article(title="近ちゃんです。",link="kondo.com",category="it"))
        session.commit()
    response = client.get("/news/all")
    assert response.status_code == 200
    data = response.json()
    titles = [a["title"] for a in data["articles"]]
    assert "近ちゃんです。" in titles


