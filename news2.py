import webbrowser
import urllib.request
import xml.etree.ElementTree as ET
import unicodedata

def sanitize_input(text):
    # 'NFKC' という設定で正規化すると、全角数字が半角数字に変換される
    # .strip() をつけることで、前後の余計なスペースも削ぎ落とす
    return unicodedata.normalize('NFKC', text).strip()

# ターゲットとなるRSS（Yahoo!ニュース）
RSS_URL = 'https://news.yahoo.co.jp/rss/topics/top-picks.xml'

def main():
    print("\n" + "="*50)
    print("📰 InfoCLI Lv.4: Advanced News Filter")
    print("="*50)

     #1．データの取得（ループごとに最新の情報を得る）
    with urllib.request.urlopen(RSS_URL) as response:
        xml_data = response.read()
        root = ET.fromstring(xml_data)
    
    #新しい実装部
    while True:
        try:

            print("\n"+"-"*30)

             # 【Lv.4】ユーザーから検索キーワードを受け取る
            keyword = input("抽出したいキーワードを入力してください [qで終了]: ")

            if keyword.lower() == "q":
                print("終了します。")
                break

            # 取得したデータを溜めるためのリスト
            news_urls = []

            #2 検索実行
            for item1 in root.findall('.//item'):
                title = item1.find('title').text
                link = item1.find('link').text
                # inの使い方
                if keyword.lower() in title.lower():
                    news_urls.append(link)
                    print(f"[{len(news_urls)}]{title}")

            #3 検索結果が空だった場合
            if not news_urls:
                print(f"「{keyword}」は見つかりませんでした。")
                print("代わりに最新のニュースを表示します。")

                for item2 in root.findall('.//item')[:8]:
                    title = item2.find('title').text
                    link = item2.find('link').text
                    news_urls.append(link)
                    print(f"[{len(news_urls)}]{title}")

            print("\n"+"-"*30)

             #
            choice_raw = input(f"見たい記事の番号を入力してください (1-{len(news_urls)}) /[rで再検索] ")
            choice = unicodedata.normalize('NFKC',choice_raw).strip()
            
            if choice.lower() == 'r':
                continue #ループの先頭にワープ
            else:

                # 入力された「文字」を「数字」に変換し、マシンの数え方（0番開始）に合わせる 
                idx = int(choice) - 1
            
            # リストから選ばれたURLを取り出し、ブラウザを叩き起こす
                target_url = news_urls[idx]
                print(f"\n🌐 ブラウザで開きます: {target_url}")
                webbrowser.open(target_url)

        except ValueError:
            print("⚠️ エラー: 数字か'q''/'r'を入力してください。")
        except IndexError:
            print("⚠️ エラー: 存在しない番号が選ばれました。")
        except Exception as e:
            print(f"❌ 予期せぬエラーが発生しました: {e}")
            break

if __name__ == "__main__":
    main()
 
       