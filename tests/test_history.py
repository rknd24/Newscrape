from Newscrape import HistoryManager


def test_save_article(tmp_path):
    
    test_file = tmp_path / "test_history.txt"
    
    manager = HistoryManager(str(test_file))

    manager.save_article("テスト記事", "テスト要約")

    with open(test_file, "r", encoding="utf-8") as f:
        content = f.read()

    assert "テスト記事" in content
    assert "テスト要約" in content
    
