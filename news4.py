import urllib.request
import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup
import unicodedata
import time  

from google import genai

# --- 【設定：AIの鍵】 ---
GOOGLE_API_KEY = "AIzaSyDFHpliWr62A5rdsuFvu4Nu5k-42xxhY20"
client = genai.Client(api_key=GOOGLE_API_KEY)

RSS_URL = 'https://news.yahoo.co.jp/rss/topics/top-picks.xml'

def main():
    print("\n" + "="*50)
    print("📰 InfoCLI Lv.6.1: The Intelligence System (Armored)")
    print("="*50)

    # --- 【Lv.6.2 情報源選択メニュー】 ---
    print("【解析ターゲットを選択してください】")
    print("[1] 総合トップニュース")
    print("[2] 経済・ビジネス")
    print("[3] IT・科学技術")
    
    cat_choice_raw = input("番号を選択 (1-3): ")
    cat_choice = unicodedata.normalize('NFKC', cat_choice_raw).strip() # 全角を半角に強制変換
    
    if cat_choice == '2':
        RSS_URL = 'https://news.yahoo.co.jp/rss/topics/business.xml'
        print("経済モードで起動します...")
    elif cat_choice == '3':
        RSS_URL = 'https://news.yahoo.co.jp/rss/topics/it.xml'
        print("IT・科学モードで起動します...")
    else:
        RSS_URL = 'https://news.yahoo.co.jp/rss/topics/top-picks.xml'
        print("総合モードで起動します...")
    # ------------------------------------

    try:
        with urllib.request.urlopen(RSS_URL) as response:
            xml_data = response.read()
        root = ET.fromstring(xml_data)
    except Exception as e:
        print(f"❌ RSS取得失敗: {e}")
        return

    while True:
        try:
            print("\n"+"-"*40)
            keyword_raw = input("検索キーワードを入力してください [qで終了]: ")
            keyword = unicodedata.normalize('NFKC', keyword_raw).strip()

            if keyword.lower() == 'q': break

            news_urls = []
            for item in root.findall('.//item'):
                t_elem = item.find('title')
                l_elem = item.find('link')
                if t_elem is None or l_elem is None: continue
                
                title = t_elem.text
                if keyword.lower() in title.lower():
                    news_urls.append(l_elem.text)
                    print(f"[{len(news_urls)}] {title}")

            if not news_urls:
                print(f"❌ 「{keyword}」なし。最新を表示します。")
                for item in root.findall('.//item')[:8]:
                    t_elem = item.find('title')
                    l_elem = item.find('link')
                    news_urls.append(l_elem.text)
                    print(f"[{len(news_urls)}] {t_elem.text}")

            print("-" * 40)
            choice = input(f"記事を選択 (1-{len(news_urls)}) / [rで再検索]: ")
            if choice.lower() == 'r': continue
            
            target_url = news_urls[int(choice) - 1]

            # --- スクレイピング ＆ AI解析 ---
            print(f"\nAIが記事を解析中... (数秒かかります)\n")
            
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            res = requests.get(target_url, headers=headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            article_tag = soup.find('article')
            raw_text = article_tag.get_text() if article_tag else soup.get_text()

            prompt = f"""
            以下のテキストは、ニュースサイトから抽出した生のデータです。
            不要な広告、アンケート、JavaScriptの警告などを完全に排除し、
            情報理工学部の学生が読むに値する「プロのニュースレポート」として要約してください。

            【制約】
            1. 最初に「3行でわかる要約」を書くこと。
            2. その下に、経済や技術的な「背景・影響」を箇条書きで書くこと。
            3. 専門用語は逃げずに使いつつ、簡潔にまとめること。

            記事原文:
            {raw_text[:5000]} 
            """

            # --- 【Lv.6.1 自動リトライ機能付きAI呼び出し】 ---
            max_retries = 3 # 最大3回まで粘る
            
            for attempt in range(max_retries):
                try:
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt
                    )
                    break # 成功したらこのループを抜ける！
                except Exception as api_error:
                    if "503" in str(api_error) and attempt < max_retries - 1:
                        wait_time = 2  # 2秒待機
                        print(f"⚠️ Googleサーバー混雑中。{wait_time}秒後に再挑戦します... ({attempt+1}/{max_retries})")
                        time.sleep(wait_time)
                    else:
                        raise api_error # 別のエラーか、3回やってもダメなら諦める
            # -----------------------------------------------

            print("="*50)
            print(response.text)
            print("="*50)
            print(f"\n🔗 元記事URL: {target_url}")

        except Exception as e:
            print(f"❌ エラー発生: {e}")

if __name__ == "__main__":
    main()