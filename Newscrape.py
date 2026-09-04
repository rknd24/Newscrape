import os
import urllib.request
import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup
import unicodedata
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich import box
import datetime
from groq import Groq

console = Console()

# --- Configuration ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")


# --- AI Analyzer Module ---
class AIAnalyzer:
    """Llama APIを利用したテキスト解析クラス"""

    def __init__(self, api_key: str):
        self.model = "qwen/qwen3.8-27b"
        self.client = Groq(api_key=api_key)

    def analyze(self, raw_text: str) -> str:
        """記事本文を解析し、要約を返す"""
        try:
            return self._call_llama(raw_text)
        except Exception as e:
            return f"[Error] Analysis failed: {e}"

    def _call_llama(self, raw_text: str) -> str:
        prompt = f"""
        以下のニュース記事を、一般の読者向けに短く要約してください。
        体言止めを使い、冗長な表現は避けること。
        出力は必ず次の3つの見出しで、各項目2文以内。

        ■ 経緯
        何が、どういう流れで起きたか。

        ■ ポイント
        専門用語や技術的な内容があれば、一般の人にわかる言葉で。

        ■ 影響
        私たちの生活や社会にどう関わるか。憶測は避け、記事から読み取れる範囲で。

        記事本文:
        {raw_text[:3000]}
        """

        response = self.client.chat.completions.create(
            model=self.model, messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content


# --- Scraper Module ---
class NewsFetcher:
    """RSSパースおよびWebスクレイピングを行うクラス"""

    def fetch_rss_root(self, url: str) -> ET.Element | None:
        try:
            with urllib.request.urlopen(url,timeout=10) as response:
                return ET.fromstring(response.read())
        except Exception as e:
            print(f"[Error] Failed to fetch RSS: {e}")
            return None

    def scrape_article(self, url: str) -> str | None:
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            res = requests.get(url, headers=headers,timeout=10)
            res.raise_for_status()
            res.encoding = res.apparent_encoding
        except requests.RequestException as e:
            print(f"[Error] Failed to fetch article:{e}")
            return None
        soup = BeautifulSoup(res.text, "html.parser")
        article_tag = soup.find("article")
        return article_tag.get_text(separator="\n",strip=True) if article_tag else soup.get_text()


class HistoryManager:
    """履歴ファイルの保存･管理を担当するクラス"""

    def __init__(self, filepath: str = "history.txt"):
        self.filepath = filepath

    def save_article(self, title: str, summary: str):
        """記事のタイトルと要約、取得時刻をファイルに追記する"""
        # 1. 現在の時刻を取得して指定のフォーマットにする
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        # 2. 書き込むテキスト（ログのフォーマット）を組み立てる
        log_text = f"[{now}]\nタイトル: {title}\n要約:\n{summary}\n" + "-" * 100 + "\n"

        # 3. ファイルを開いて、テキストを「追記（a）」する
        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(log_text)


# --- CLI Controller Module ---
class CLIController:
    """CLIのルーティングと表示制御を行うメインコントローラー"""

    def __init__(self, api_key: str):
        self.history_manager = HistoryManager()
        self.fetcher = NewsFetcher()
        self.analyzer = AIAnalyzer(api_key)
        self.rss_map = {
            "1": ("総合", "https://news.yahoo.co.jp/rss/topics/top-picks.xml"),
            "2": ("経済", "https://news.yahoo.co.jp/rss/topics/business.xml"),
            "3": ("IT・科学", "https://news.yahoo.co.jp/rss/topics/it.xml"),
        }

    def run(self):
        while True:
            print("\n" + "=" * 50)
            print(" Newscrape")
            print("=" * 50)
            for k, v in self.rss_map.items():
                print(f"[{k}] {v[0]}")

            raw_choice = input("\nSelect Category(q:終了):")
            cat_choice = unicodedata.normalize("NFKC", raw_choice).strip().lower()

            if cat_choice == "q":
                break
            if cat_choice not in self.rss_map:
                print("[Error] Invalid selection.")
                continue

            label, url = self.rss_map[cat_choice]
            print(f"\n>> {label} mode loading...")
            root = self.fetcher.fetch_rss_root(url)
            if root is not None:
                self.search_loop(root)

    def search_loop(self, root: ET.Element):
        while True:
            print("\n" + "-" * 40)
            keyword_raw = input(
                "Search Keyword [Enter: 最新情報 / b: 戻る / q: 終了]: "
            ).strip()
            keyword = unicodedata.normalize("NFKC", keyword_raw).strip().lower()

            if keyword == "q":
                exit()
            if keyword == "b":
                break
            
            all_items = root.findall('.//item')
            news_list = []
            for item in all_items:
                title = item.find("title").text
                link = item.find("link").text
                if not keyword or keyword in title.lower():
                    news_list.append({"title": title, "link": link})

            if not news_list:
                print(f"No articles found for '{keyword}'.")
                continue

            print(f"\n--- Article List ({keyword if keyword else 'Latest'}) ---")
            for i, news in enumerate(news_list[:10], 1):
                print(f"[{i}] {news['title']}")

            self.article_select_loop(news_list[:10])

    def article_select_loop(self, news_list: list):
        while True:
            raw_choice = input(
                f"\nSelect Article (1-{len(news_list)}) / [b: 戻る / q: 終了]: "
            )
            choice = unicodedata.normalize("NFKC", raw_choice).strip().lower()

            if choice == "q":
                exit()
            if choice == "b":
                break
            if not choice:
                continue

            if not choice.isdigit() or not (1 <= int(choice) <= len(news_list)):
                print("[Error] Invalid selection.")
                continue

            target = news_list[int(choice) - 1]
            print(f"\n>> Analyzing: {target['title']} ...")

            raw_text = self.fetcher.scrape_article(target["link"])
            if raw_text is None:
                print("記事取得に失敗しました。")
                continue
            report = self.analyzer.analyze(raw_text)

            md_text = Markdown(report)

            console.print(
                Panel(md_text, title="Analyze", border_style="cyan", box=box.ASCII)
            )
            print("=" * 50)
            print(f"URL: {target['link']}")
            print("=" * 50)

            while True:

                save_action = input(
                    "\nこの記事を保存しますか？\n[h: 保存 / Enter: 保存せず次に進む / q: 終了]"
                )
                action = unicodedata.normalize("NFKC", save_action).strip().lower()

                if action == "h":
                    clean_report = report.replace("*", "")
                    self.history_manager.save_article(target["title"], clean_report)
                    print(f"\n記事の履歴を{self.history_manager.filepath}に保存完了")
                    break
                elif action == "":
                    print("\n>>保存をスキップしました")
                    break
                elif action == "q":
                    exit()
                else:
                    print("[Error] 無効な入力です。")

            while True:
                raw_action = input("\n[b: 記事選択に戻る / s: 検索に戻る / q: 終了]: ")
                action = unicodedata.normalize("NFKC", raw_action).strip().lower()

                if action == "q":
                    exit()
                elif action == "b":
                    break
                elif action == "s":
                    return
                elif action == "":
                    continue
                else:
                    print("[Error] Invalid selection.")


if __name__ == "__main__":
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        raise ValueError("Environment variable 'GROQ_API_KEY' is not set.")
    app = CLIController(key)
    app.run()


