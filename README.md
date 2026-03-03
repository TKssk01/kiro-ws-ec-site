# EC サイト (Kiro Workshop 用)

Kiro Workshop で利用する EC サイトです。  
フロントエンド（React）とバックエンド（Python FastAPI）の 2 プロセス構成で、Spec 駆動開発を体験するための教材です。

## アーキテクチャ

```
┌──────────────┐    HTTP     ┌──────────────┐    SQL     ┌──────────┐
│  Frontend    │ ──────────→ │  Backend     │ ────────→ │  SQLite  │
│  React+Vite  │  :5173      │  FastAPI     │  :8000    │  (file)  │
│  (Node.js)   │ ←────────── │  (Python)    │ ←──────── │          │
└──────────────┘             └──────────────┘           └──────────┘
```

## 機能

- 📦 商品一覧表示
- 🛍️ ショッピングカート機能
- 💳 チェックアウト・注文機能
- 📡 フロント ↔ バックエンド API 連携
- 🗄️ SQLite によるデータ永続化

## セットアップ

### 必要要件

- Node.js (v18 以上)
- Python (v3.10 以上)

### 1. バックエンド

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python init_db.py
uvicorn main:app --port 8000 --reload
```

API ドキュメント: http://localhost:8000/docs

### 2. フロントエンド

```bash
# プロジェクトルートで実行
npm install
npm run dev
```

ブラウザで http://localhost:5173 を開いてアプリケーションを確認できます。

## プロジェクト構造

```
kiro-ws-ec-site/
├── src/                    # フロントエンド (React)
│   ├── components/         # React コンポーネント
│   │   ├── cart/           # カート関連
│   │   ├── checkout/       # チェックアウト関連
│   │   ├── common/         # 共通コンポーネント
│   │   ├── layout/         # レイアウト
│   │   └── product/        # 商品関連
│   ├── context/            # React Context
│   ├── data/               # 静的データ (参考用)
│   ├── hooks/              # カスタムフック
│   ├── pages/              # ページコンポーネント
│   └── utils/              # ユーティリティ (API クライアント含む)
├── backend/                # バックエンド (Python)
│   ├── main.py             # FastAPI アプリケーション
│   ├── init_db.py          # DB 初期化スクリプト
│   ├── products.db         # SQLite データベース
│   └── requirements.txt    # Python 依存関係
├── package.json
└── vite.config.js
```

## API エンドポイント

| メソッド | パス | 説明 |
|---------|------|------|
| GET | `/api/products` | 商品一覧取得 |
| GET | `/api/products/{id}` | 商品詳細取得 |
| POST | `/api/cart/validate` | カート内容の在庫検証 |
| POST | `/api/orders` | 注文作成 |
| GET | `/api/orders/{order_number}` | 注文詳細取得 |

## ワークショップについて

このプロジェクトは Kiro の **Spec 駆動開発** を体験するための教材です。  
ワークショップでは、Kiro の Spec Mode を使って新機能を追加する流れを体験します。
