from Newscrape import HistoryManager

def test_save_article():
    manager = HistoryManager("test_history.txt")

    manager.save_article(
        "テスト記事",
        "テスト要約"
    )

    with open(
        "test_history.txt",
        "r",
        encoding="utf-8"
    ) as f:
        content = f.read()

    assert "テスト記事" in content
    assert "テスト要約" in content