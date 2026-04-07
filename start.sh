#!/bin/bash

# バックエンド起動
cd backend
sudo apt install -y python3.12-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 init_db.py
uvicorn main:app --port 8000 --reload &

# フロントエンド起動
cd ..
npm install
npm run dev
