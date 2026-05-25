import webbrowser
import urllib.request
import xml.etree.ElementTree as ET

url = 'https://news.yahoo.co.jp/rss/topics/top-picks.xml'

try:

    
    print("\n" + "="*40)
    print("📰 InfoCLI: Loading Latest News...")
    print("="*40)

    # 【新機能】URLを記憶するための空のバケツ（リスト）
    news_urls = []

    with urllib.request.urlopen(url) as response:
        xml_data = response.read()
    
    root = ET.fromstring(xml_data)

    for i, item in enumerate(root.findall('.//item')[:5]):
        title = item.find('title').text
        link = item.find('link').text # URLを取得
        
        # 【新機能】取得したURLをリストに順番に追加していく
        news_urls.append(link)
        
        print(f"[{i+1}] {title}")
        
    print("="*40)
    
    # 【新機能】ユーザーからの入力を受け付ける
    choice = input("見たい記事の番号を入力してください (1-5) [qで終了]: ")
    
    if choice.lower() == 'q':
        print("終了します。")
    else:
        # 入力された数字を「インデックス（0番開始）」に変換してURLを取り出す
        idx = int(choice) - 1
        target_url = news_urls[idx]
        
        print(f"🌐 ブラウザで開きます: {target_url}")
        webbrowser.open(target_url,new = 2)

except Exception as e:
    print(f"❌ エラーが発生しました: {e}")