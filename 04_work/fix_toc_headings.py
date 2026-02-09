# 02_導入ファイルの見出し階層修正スクリプト

import re

filepath = r'c:\Users\kumac\OneDrive\デスクトップ\antigravity\BookProject\02_章別\02_第1部 導入：基礎道具編の目的と学習ロードマップ.md'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 問題: ## で始まる見出しがh1の直下にあるため、TOC構造が壊れている
# 解決: 番号付きの ## 見出しを ### に変更する

# パターン1: ## 1. ... → ### 1. ...
# パターン2: ## 2. ... → ### 2. ...
# パターン3: ## 3. ... → ### 3. ...
# パターン4: ## 4. ... → ### 4. ...
# パターン5: ## 変更に強い構造という報酬 → ### 変更に強い構造という報酬

# 番号付き見出しを変換
content = re.sub(r'^## (\d+\.)', r'### \1', content, flags=re.MULTILINE)

# 特定の見出しも変換
content = re.sub(r'^## (変更に強い構造という報酬)', r'### \1', content, flags=re.MULTILINE)

with open(filepath, 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print("見出し階層を修正しました")
print("## → ### に変更した見出し:")
print("- ## 1. 基礎道具編の位置づけ")
print("- ## 2. 本書の構造における「技術・原則・目的」の対応")
print("- ## 3. 「責任・契約・依存」のフレームワークと第1部の技術")
print("- ## 4. 学習ロードマップ：螺旋的な技術習得")
print("- ## 変更に強い構造という報酬")
