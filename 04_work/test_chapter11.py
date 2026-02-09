# Chapter 11単体テスト用スクリプト

import sys
import os
from pathlib import Path

# 元のスクリプトのパスを追加
sys.path.insert(0, r'c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\05_生成')

# 作業ディレクトリを変更
os.chdir(r'c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\05_生成')

# テスト用の一時ディレクトリを作成
test_dir = Path("../04_work/test_chapter11")
test_dir.mkdir(exist_ok=True)

# Chapter 11をコピー
import shutil
src = Path("../02_章別/15_第2部 第11章 インターフェース分離原則 (ISP) 不要な依存の排除とモジュール結合度の最小化_01.md")
dst = test_dir / src.name
shutil.copy(src, dst)

print(f"[TEST] テストファイル: {dst}")

# build_epubをインポートして設定を変更
import build_epub

# CHAPTER_DIRをテストディレクトリに設定
build_epub.CHAPTER_DIR = test_dir

print(f"[INFO] CHAPTER_DIR を {build_epub.CHAPTER_DIR} に設定")
print(f"[INFO] 対象ファイル数: {len(list(build_epub.CHAPTER_DIR.glob('*.md')))}")

# メイン処理を実行
try:
    build_epub.main()
    print("\n[SUCCESS] Chapter 11のテストが成功しました!")
except Exception as e:
    print(f"\n[ERROR] テスト失敗: {e}")
    import traceback
    traceback.print_exc()
