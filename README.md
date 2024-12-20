# Elegant Logo Creator

DALLｰE 3とSVGを使用したエレガントなロゴ作成Webアプリケーション

## 機能

- DALL-E 3を使用した画像生成
- SVGテキストオーバーレイ
- テキストのカスタマイズ（フォント、サイズ、色、位置）
- 最終的なロゴのPNGダウンロード

## セットアップ

1. リポジトリをクローン:
```bash
git clone [your-repository-url]
cd elegant-logo-creator
```

2. 依存関係をインストール:
```bash
pip install -r requirements.txt
```

3. 環境変数の設定:
- `.env`ファイルを作成し、以下の内容を設定:
```
OPENAI_API_KEY=your_api_key_here
FLASK_SECRET_KEY=your_secret_key_here
```

4. アプリケーションの実行:
```bash
python main.py
```

## 使用方法

1. ブラウザで`http://localhost:5000`にアクセス
2. プロンプトを入力して画像を生成
3. テキストを追加してカスタマイズ
4. 完成したロゴをPNGとしてダウンロード

## 技術スタック

- Python/Flask
- OpenAI API (DALL-E 3)
- SVG.js
- Bootstrap 5
