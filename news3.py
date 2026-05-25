import urllib.request
import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup
import unicodedata

RSS_URL = 'https://news.yahoo.co.jp/rss/topics/top-picks.xml'

def main():
    print("\n" + "="*50)
    print("📰 InfoCLI Lv.5.2: Precision Armored System")
    print("="*50)

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

            if keyword.lower() == 'q':
                print("終了します。")
                break

            news_urls = []

            # --- 検索実行（【重要】要約が無くても大谷さんを救う修正） ---
            for item in root.findall('.//item'):
                t_elem = item.find('title')
                l_elem = item.find('link')
                d_elem = item.find('description') # 要約はオプション扱いにする

                # タイトルとリンクさえあればニュースとして成立するので、d_elemのNoneチェックは外す
                if t_elem is None or l_elem is None:
                    continue

                title = t_elem.text
                link = l_elem.text
                # 要約がない場合は代替テキストを入れる（これでNoneTypeエラーを防ぐ）
                description = d_elem.text if d_elem is not None else "（要約データなし）"

                if keyword.lower() in title.lower():
                    news_urls.append(link)
                    print(f"[{len(news_urls)}] {title}")
                    print(f"    📝 {description}")

            # --- 検索ヒットなしの場合 ---
            if not news_urls:
                print(f"❌ 「{keyword}」は見つかりませんでした。代わりに最新を表示します。")
                for item in root.findall('.//item'):
                    t_elem = item.find('title')
                    l_elem = item.find('link')
                    if t_elem is None or l_elem is None: continue
                    
                    news_urls.append(l_elem.text)
                    print(f"[{len(news_urls)}] {t_elem.text}")
                    if len(news_urls) >= 8: break

            print("-" * 40)
            choice_raw = input(f"記事番号を選択 (1-{len(news_urls)}) /[rで再検索]: ")
            choice = unicodedata.normalize('NFKC', choice_raw).strip()
            
            if choice.lower() == 'r': continue

            idx = int(choice) - 1
            target_url = news_urls[idx]

            # --- スクレイピング実行 ---
            print(f"\n🌐 本文を抽出中...\n")
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
            res = requests.get(target_url, headers=headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # --- 【Lv.5.5：汎用スクレイピング（全ジャンル対応）】 ---
            print("="*50)
            
            # 1. ジャンルを問わず、ニュースの「主役」は <article> タグの中にいる
            article_tag = soup.find('article')
            
            if article_tag:
                # 2. 記事の中にある全ての段落（p）を一旦すべて拾う
                paragraphs = article_tag.find_all('p')
            else:
                # 保険：articleタグがない特殊なページ（号外など）の場合
                paragraphs = soup.find_all('p')
            
            for p in paragraphs:
                text = p.text.strip()
                
                # --- 【Lv.5.5：ノイズ・アサシン・フィルター】 ---
                if not text: continue
                
                # 1. 文字数制限を少し厳しめに（30文字未満は疑う）
                if len(text) < 30: continue 

                # 2. 「？（全角ハテナ）」で終わる文は、大抵アンケートか釣り見出しなので消す
                if text.endswith('？') or text.endswith('?'): continue
                
                # 3. ジャンルを問わず、ニュース本文に絶対に出ない言葉（ブラックリスト）
                ng_list = [
                    "世論調査", "アンケート", "JavaScript", "出典：", 
                    "何ですか", "詳しく知る", "統計に基づく", "提供基準"
                ]
                if any(word in text for word in ng_list):
                    continue
                
                # 4. 「関連ニュース」系の見出しによくあるパターンを弾く
                if "【" in text and "】" in text and len(text) < 50: continue

                # ----------------------------------------------
                
                print(text)
                print() # 1行空けて読みやすく
            print("="*50)

        except ValueError:
            print("⚠️ 数字か 'q'/'r' を入れてな！")
        except IndexError:
            print("⚠️ その番号はないで！")
        except Exception as e:
            print(f"❌ エラー発生: {e}")

if __name__ == "__main__":
    main()