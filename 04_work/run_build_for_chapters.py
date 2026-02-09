# build_epub.pyを02_章別用に修正して実行

import sys
import os

# 元のスクリプトのパスを追加
sys.path.insert(0, r'c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\05_生成')

# 作業ディレクトリを変更
os.chdir(r'c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\05_生成')

# CHAPTER_DIRを02_章別に変更
import build_epub
from pathlib import Path

# 設定を上書き
build_epub.CHAPTER_DIR = Path("../02_章別")

print(f"[INFO] CHAPTER_DIR を {build_epub.CHAPTER_DIR} に設定")
print(f"[INFO] 対象ファイル数: {len(list(build_epub.CHAPTER_DIR.glob('*.md')))}")

# メイン処理を実行
build_epub.main()
